
from webdav.exceptions import *
from webdav.urn import Urn
from os.path import exists

class ConnectionSettings:

    def is_valid(self):
        pass

    def valid(self):

        try:
            self.is_valid()
        except OptionNotValid:
            return False
        else:
            return True

class WebDAVSettings(ConnectionSettings):

    ns = "webdav:"
    prefix = "webdav_"
    required_keys = {'hostname'}
    optional_keys = {'login', 'password', 'root', 'cert_path', 'key_path'}

    def __init__(self, options):

        self.options = dict()

        keys = self.required_keys.union(self.optional_keys)
        for key in keys:
            value = options.get(key, '')
            self.options[key] = value
            self.__dict__[key] = value

        self.root = Urn(self.root).quote() if self.root else ''
        self.root = self.root.rstrip(Urn.separate)

    def is_valid(self):

        for required_key in self.required_keys:
            value = self.options.get(required_key)
            if not value:
                raise OptionNotValid(name=required_key, value=value)

        if self.cert_path and not exists(self.cert_path):
            raise OptionNotValid(name="cert_path", value=self.cert_path, ns=self.ns)

        if self.key_path and not exists(self.key_path):
            raise OptionNotValid(name="key_path", value=self.key_path, ns=self.ns)

        if self.key_path and not self.cert_path:
            raise OptionNotValid(name="cert_path", value=self.cert_path, ns=self.ns)

        if self.password and not self.login:
            raise OptionNotValid(name="login", value=self.login, ns=self.ns)


class ProxySettings(ConnectionSettings):

    ns = "proxy:"
    prefix = "proxy_"
    required_keys = {'hostname'}
    optional_keys = {'login', 'password'}

    def __init__(self, options):

        self.options = dict()

        keys = self.required_keys.union(self.optional_keys)
        for key in keys:
            value = options.get(key, '')
            self.options[key] = value
            self.__dict__[key] = value

    def is_valid(self):

        for required_key in self.required_keys:
            value = self.options.get(required_key)
            if not value:
                raise OptionNotValid(name=required_key, value=value)

        if self.password and not self.login:
            raise OptionNotValid(name="login", value=self.login, ns=self.ns)