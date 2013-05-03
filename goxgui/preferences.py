import utilities

from ConfigParser import RawConfigParser
from os import path
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from ui.preferences_ import Ui_Preferences


class Preferences(QDialog):
    '''
    Represents the application preferences.
    '''

    PASSPHRASE = 'fffuuuuuuu'
    FILENAME = 'goxgui.ini'
    SECTION_GLOBAL = 'Global'

    def __init__(self):
        QDialog.__init__(self)

        # set up gui
        self.__ui = Ui_Preferences()
        self.__ui.setupUi(self)

        # connect signals
        self.__ui.lineEditKey.editingFinished.connect(
            self.__slot_validate_key_secret)
        self.__ui.lineEditSecret.editingFinished.connect(
            self.__slot_validate_key_secret)

        # initialize config parser
        self.configparser = RawConfigParser()

        # load or (on first use) create config file
        if path.isfile(self.FILENAME):
            self.load()
        else:
            self.__init_with_defaults()
            self.save()

    def __init_with_defaults(self):
        self.configparser.add_section(self.SECTION_GLOBAL)
        self.set('currency_a', 'BTC')
        self.set('currency_b', 'USD')
        self.set('key', '')
        self.set('secret', '')

    def __load_to_gui(self):
        self.__ui.lineEditKey.setText(self.get_key())
        self.__ui.lineEditSecret.setText(self.get_secret())

    def __slot_validate_key_secret(self):

        key = str(self.__ui.lineEditKey.text())
        secret = str(self.__ui.lineEditSecret.text())

        # empty credentials are allowed
        if key == '' and secret == '':
            self.__enable_ok()
            return

        try:
            utilities.assert_valid_key(key)
        except Exception as e:
            self.__disable_ok('Invalid key.'.format(str(e)))
            return

        try:
            utilities.assert_valid_secret(secret)
        except Exception as e:
            self.__disable_ok('Invalid secret.'.format(str(e)))
            return

        self.__enable_ok()

    def __disable_ok(self, text):
        self.__ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.__ui.labelStatus.setText(text)

    def __enable_ok(self):
        self.__ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.__ui.labelStatus.setText('')

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
        '''
        self.set('key', key)

    def get_key(self):
        '''
        Loads the key from the configuration file.
        '''
        return self.get('key')

    def set_secret(self, secret):
        '''
        Writes the specified secret to the configuration file (encrypted).
        '''
        secret = utilities.encrypt(secret, Preferences.PASSPHRASE)
        self.set('secret', secret)

    def get_secret(self):
        '''
        Loads the secret from the configuration file.
        '''
        secret = self.get('secret')
        if secret == '':
            return secret

        return utilities.decrypt(secret, Preferences.PASSPHRASE)

    def show(self):

        self.__load_to_gui()
        result = self.exec_()
        return result == QDialog.Accepted

    def apply(self):

        self.set_key(str(self.__ui.lineEditKey.text()))
        self.set_secret(str(self.__ui.lineEditSecret.text()))
        self.save()
