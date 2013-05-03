from ConfigParser import RawConfigParser
from os import path
import utilities


class Preferences():
    '''
    Represents the application preferences.
    '''

    PASSPHRASE = 'fffuuuuuuu'
    FILENAME = 'goxgui.ini'
    SECTION_GLOBAL = 'Global'

    def __init__(self):

        self.configparser = RawConfigParser()

        if path.isfile(self.FILENAME):
            self.load()
        else:
            self.__init()
            self.save()

    def __init(self):
        self.configparser.add_section(self.SECTION_GLOBAL)
        self.set('currency_a', 'BTC')
        self.set('currency_b', 'USD')
        self.set('key', '')
        self.set('secret', '')

    def save(self):
        '''
        Saves the config to the .ini file
        '''
        with open(self.FILENAME, 'wb') as configfile:
            self.configparser.write(configfile)

    def load(self):
        '''
        Loads or reloads the config from the .ini file
        '''
        self.configparser.read(self.FILENAME)

    def get(self, key):
        '''
        Retrieves a property from the global section
        '''
        return self.configparser.get(self.SECTION_GLOBAL, key)

    def set(self, key, value):
        '''
        Stores a property to the global section
        '''
        self.configparser.set(self.SECTION_GLOBAL, key, value)

    def set_key(self, key):
        '''
        Writes the specified key to the configuration file.
        @raise Exception: if key is invalid
        '''

        print "key: '" + key + "'"

        utilities.assert_valid_key(key)

        self.set('key', key)
        self.save()

    def get_key(self):
        '''
        Loads the key from the configuration file.
        @raise Exception: if key is invalid
        '''

        key = self.get('key')
        utilities.assert_valid_key(key)
        return key

    def set_secret(self, secret):
        '''
        Writes the specified secret to the configuration file (encrypted).
        @raise Exception: if secret is invalid
        '''

        if secret == '':
            raise Exception("empty secret")

        try:
            secret = utilities.encrypt(secret, Preferences.PASSPHRASE)
        except Exception:
            raise Exception("invalid secret")

        self.set('secret', secret)
        self.save()

    def get_secret(self):
        '''
        Loads the secret from the configuration file
        @raise Exception: if secret is invalid
        '''

        secret = self.get('secret')
        secret = utilities.decrypt(secret, Preferences.PASSPHRASE)

        return secret
