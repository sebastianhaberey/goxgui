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

        # set up ui
        self.__ui = Ui_Preferences()
        self.__ui.setupUi(self)

        # connect ui signals to logic
        self.__ui.lineEditKey.textChanged.connect(
            self.__slot_validate_credentials)
        self.__ui.lineEditSecret.textChanged.connect(
            self.__slot_validate_credentials)

        # initialize config parser
        self.configparser = RawConfigParser()

        # __load or (if non-existent) create config file
        if path.isfile(self.FILENAME):
            self.__load()
        else:
            self.__init_with_defaults()
            self.__save()

    # start slots

    def __slot_validate_credentials(self):

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

    # end slots

    # start private methods

    def __init_with_defaults(self):
        self.configparser.add_section(self.SECTION_GLOBAL)
        self.set('currency_a', 'BTC')
        self.set('currency_b', 'USD')
        self.set('key', '')
        self.set('secret', '')

    def __load_to_gui(self):
        self.__ui.lineEditKey.setText(self.get_key())
        self.__ui.lineEditSecret.setText(self.get_secret())
        self.__set_status('')

    def __save_from_gui(self):
        self.__set_key(str(self.__ui.lineEditKey.text()))
        self.__set_secret(str(self.__ui.lineEditSecret.text()))

    def __disable_ok(self, text):
        self.__ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.__set_status(text)

    def __enable_ok(self):
        self.__ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.__set_status('')

    def __save(self):
        '''
        Saves the config to the .ini file
        '''
        with open(self.FILENAME, 'wb') as configfile:
            self.configparser.write(configfile)

    def __load(self):
        '''
        Loads or reloads the config from the .ini file
        '''
        self.configparser.read(self.FILENAME)

    def __set_key(self, key):
        '''
        Writes the specified key to the configuration file.
        '''
        self.set('key', key)

    def __set_secret(self, secret):
        '''
        Writes the specified secret to the configuration file (encrypted).
        '''
        if secret != '':
            secret = utilities.encrypt(secret, Preferences.PASSPHRASE)
        self.set('secret', secret)

    def __set_status(self, text):
        self.__ui.labelStatus.setText(text)

    # end private methods

    # start public methods

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

    def get_key(self):
        '''
        Loads the key from the configuration file.
        '''
        return self.get('key')

    def get_secret(self):
        '''
        Loads the secret from the configuration file.
        '''
        secret = self.get('secret')
        if secret == '':
            return secret

        return utilities.decrypt(secret, Preferences.PASSPHRASE)

    def show(self):
        '''
        Shows the preference dialog.
        @return: True if the user accepted, false otherwise
        '''
        self.__load_to_gui()
        result = self.exec_()
        return result == QDialog.Accepted

    def apply(self):
        '''
        Applies the user changes.
        Changes made by the user during show()
        do not propagate until apply() is called.
        '''
        self.__save_from_gui()
        self.__save()

    # end public methods
