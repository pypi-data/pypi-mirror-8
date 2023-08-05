import datetime
import re
from urllib import quote_plus, urlencode
import urllib2
import uuid

import Crypto.Cipher

from webob import Request
from webob.exc import HTTPFound, HTTPUnauthorized

# TODO
# - implement session expiration
# - implement the 'Secure' cookie option
# - implement the 'HttpOnly' cookie option
# - implement 'include_ip'
# - implement 'renew'
# - WRITE TESTS
# - verify compatibility with uconn.edu or the rubycasserver

class NoDefault(object):
    pass
def make_plugin(cookie_name, secret,
                cas_login_url, cas_validate_url,
                cas_version=NoDefault,
                logout_url=NoDefault,
                cipher="AES", key_size=16,
                gateway=False, renew=False, secure=False, include_ip=True,
                hard_timeout=28800, fix_post='False'):
    if cas_version == NoDefault:
        cas_version = "1.0"
    fix_post = fix_post == 'True'
    return CASPlugin(cookie_name, secret,
                     cas_login_url,
                     cas_validate_url,
                     cas_version,
                     logout_url,
                     cipher,
                     key_size,
                     gateway,
                     renew,
                     secure,
                     include_ip,
                     hard_timeout,
                     fix_post)

class CASPlugin(object):
    
    def _pad_string(self, string, length):
        """ return `string' extended to a multiple of `length` """
        pad_length = length * ((len(string) / length) + 1)
        return string.ljust(pad_length)
    
    def _remove_padding(self, string):
        return string.rstrip()
    
    def _encrypt_identity(self, login, ip=None):
        padded_identity = self._pad_string(login, self.cipher.key_size)
        cipher = self.cipher.new(self.secret, self.cipher.MODE_ECB)
        cookie_value = cipher.encrypt(padded_identity).encode('base64')
        return cookie_value
        
    def _decrypt_identity(self, encoded_identity):
        encrypted = encoded_identity.decode('base64').rstrip()
        cipher = self.cipher.new(self.secret, self.cipher.MODE_ECB)
        decrypted = cipher.decrypt(encrypted)
        return self._remove_padding(decrypted)
    
    def __init__(self, cookie_name, secret,
                 cas_login_url, cas_validate_url, cas_version,
                 logout_url, cipher, key_size,
                 gateway, renew, secure, include_ip,
                 hard_timeout, fix_post):
        self.cas_login_url = cas_login_url
        self.cas_validate_url = cas_validate_url
        self.cas_version = cas_version
        self.cookie_name = cookie_name
        Cipher = __import__("Crypto.Cipher", locals(), globals(), [cipher])
        self.cipher = getattr(Cipher, cipher)
        self.cipher.key_size = key_size
        if self.cipher.key_size and \
                (len(secret) % self.cipher.key_size):
            raise TypeError("the %s cipher requires a secret size of %s" %\
                                (cipher, self.cipher.key_size))
        self.secret = secret
        self.cookie_path = "/"
        self.logout_url = logout_url
        self.gateway = gateway
        self.renew = renew
        self.secure = secure
        self.include_ip = include_ip
        self.hard_timeout = int(hard_timeout)
        
        self.urlopener = urllib2.urlopen
        self._fix_post = fix_post
        self._post_bodies = {}
    
    # IChallenger
    def challenge(self, environ, status, app_headers, forget_headers):
        request = Request(environ, charset="utf8")
        
        if "gatewayed" in request.GET:
            return HTTPUnauthorized()
        
        service_url = request.url
        
        if self.gateway:
            if "?" in service_url:
                service_url += "&gatewayed=true"
            else:
                service_url += "?gatewayed=true"
        
        if self._fix_post and re.match('post', request.method, re.I):
            uid = uuid.uuid4()
            if "?" in service_url:
                service_url += "&uid=" + str(uid)
            else:
                service_url += "?uid=" + str(uid)
            self._post_bodies[str(uid)] = (request.body,
                                           request.environ['CONTENT_TYPE'])
        
        challenge_url = \
            "%s?service=%s" % (self.cas_login_url, quote_plus(service_url))
        if self.gateway:
            challenge_url += "&gateway=true"
        challenge_url += "&renew=true"
        return HTTPFound(location=challenge_url)
    
    def _force_post(self, environ):
        request = Request(environ, charset="utf8")
        body, content_type = self._post_bodies.pop(request.GET['uid'])
        request.environ['REQUEST_METHOD'] = 'POST'
        request.environ['CONTENT_TYPE'] = content_type
        request.body = body
    
    def _login(self, environ):
        request = Request(environ, charset="utf8")
        userid = None
        if self.cookie_name in request.cookies:
            userid = \
                self._decrypt_identity(request.cookies[self.cookie_name])
        elif "ticket" in request.GET:
            queryvars = request.GET
            ticket = queryvars['ticket']
            del queryvars['ticket']
            qs = urlencode(queryvars.items())
            environ['QUERY_STRING'] = qs
            environ['webob._parsed_query_vars'] = (queryvars, qs)
            
            validation_response = \
                self.urlopener("%s?service=%s&ticket=%s" % \
                                   (self.cas_validate_url,
                                    quote_plus(request.url),
                                    ticket))
            if self.cas_version == "1.0":
                response = validation_response.read()[:-1]
                if "\n" in response:
                    result, username = response.split("\n")
                    if result == "yes":
                        userid = username
            elif self.cas_version == "2.0":
                userid = None
            
            if userid is None:
                environ['repoze.who.application'] = HTTPUnauthorized()
        
        if (self._fix_post and
            'uid' in request.GET and
            request.GET['uid'] in self._post_bodies):
            self._force_post(environ)
        
        return dict(login=userid)
    
    def _logout(self, environ):
        return None
    
    # IIdentifier
    def identify(self, environ):
        return self._login(environ)

    # The following methods were lifted from repoze.who.plugins.cookie
    # IIdentifier
    def forget(self, environ, identity):
        # return a expires Set-Cookie header
        expired = \
            ('%s=""; Path=%s; Expires=Sun, 10-May-1971 11:59:00 GMT' % \
                 (self.cookie_name, self.cookie_path))
        return [('Set-Cookie', expired)]
    
    # IIdentifier
    def remember(self, environ, identity):
        cookie_value = \
            self._encrypt_identity(identity['login']).strip()
        cookies = Request(environ, charset="utf8").cookies
        gmtnow = datetime.datetime.utcnow()
        expiration = (gmtnow +
                      datetime.timedelta(seconds=int(self.hard_timeout)))
        formatted_expiration = expiration.strftime("%a, %d-%B-%Y %H:%M:%S GMT")
        existing = cookies.get(self.cookie_name)
        if existing != cookie_value:
            # return a Set-Cookie header
            set_cookie = ('%s=%s; Path=%s; Expires=%s' %
                          (self.cookie_name,
                           cookie_value,
                           self.cookie_path,
                           formatted_expiration,
                           ))
            return [('Set-Cookie', set_cookie)]
    
    #IAuthenticator
    def authenticate(self, environ, identity):
        return identity.get("login")
