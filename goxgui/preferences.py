import utilities

from ConfigParser import RawConfigParser
from os import path
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QDialogButtonBox
from ui.preferences_ import Ui_Preferences
from PyQt4 import QtGui
from currency import Currency


class Preferences(QDialog):
    '''
    Represents the application preferences.
    '''

    CURRENCY_INDEX_BASE = 1
    CURRENCY_INDEX_QUOTE = 2

    __PASSPHRASE = 'fffuuuuuuu'
    __FILENAME = 'goxgui.ini'
    __SECTION_GLOBAL = 'Global'

    def __init__(self):
        QDialog.__init__(self)

        # set up ui
        self.__ui = Ui_Preferences()
        self.__ui.setupUi(self)

        # improve ui on mac
        if utilities.platform_is_mac():
            self.__adjust_for_mac()

        # connect ui signals to logic
        self.__ui.lineEditKey.textChanged.connect(
            self.__slot_validate_credentials)
        self.__ui.lineEditSecret.textChanged.connect(
            self.__slot_validate_credentials)

        # initialize config parser
        self.configparser = RawConfigParser()

        # __load or (if non-existent) create config file
        if path.isfile(self.__FILENAME):
            self.__load()
        else:
            self.__init_with_defaults()
            self.__save()

        self.set_fiat_currencies([])

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

    def get_fiat_currency_index(self, other):
        '''
        Returns the index of the given currency in the
        fiat currency list.
        '''
        index = 0
        for currency in self.__fiat_currencies:
            if currency == other:
                return index
            index += 1
        raise Exception('Currency {} not found.'.format(other.symbol))

    def __init_with_defaults(self):
        self.configparser.add_section(self.__SECTION_GLOBAL)
        self.set_currency(Preferences.CURRENCY_INDEX_BASE, Currency('BTC'))
        self.set_currency(Preferences.CURRENCY_INDEX_QUOTE, Currency('USD'))
        self.__set_key('')
        self.__set_secret('')

    def __load_to_gui(self):
        self.__ui.lineEditKey.setText(self.get_key())
        self.__ui.lineEditSecret.setText(self.get_secret())
        quoteCurrency = self.get_currency(Preferences.CURRENCY_INDEX_QUOTE)
        index = self.get_fiat_currency_index(quoteCurrency)
        self.__ui.comboBoxCurrency.setCurrentIndex(index)
        self.__set_status('')

    def __save_from_gui(self):
        self.__set_key(str(self.__ui.lineEditKey.text()))
        self.__set_secret(str(self.__ui.lineEditSecret.text()))
        quoteCurrency = Currency(str(self.__ui.comboBoxCurrency.currentText()))
        self.set_currency(Preferences.CURRENCY_INDEX_QUOTE, quoteCurrency)

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
        with open(self.__FILENAME, 'wb') as configfile:
            self.configparser.write(configfile)

    def __load(self):
        '''
        Loads or reloads the config from the .ini file
        '''
        self.configparser.read(self.__FILENAME)

    def __set_key(self, key):
        '''
        Writes the specified key to the configuration file.
        '''
        self.__set('key', key)

    def __set_secret(self, secret):
        '''
        Writes the specified secret to the configuration file (encrypted).
        '''
        if secret != '':
            secret = utilities.encrypt(secret, Preferences.__PASSPHRASE)
        self.__set('secret', secret)

    def __set_status(self, text):
        self.__ui.labelStatus.setText(text)

    def __adjust_for_mac(self):
        '''
        Fixes some stuff that looks good on windows but bad on mac.
        '''
        # the default fixed fontA is unreadable on mac, so replace it
        fontA = QtGui.QFont('Monaco', 11)
        self.__ui.lineEditPassword.setFont(fontA)
        self.__ui.lineEditKey.setFont(fontA)
        self.__ui.lineEditSecret.setFont(fontA)

        # the default label font is too big on mac
        fontB = QtGui.QFont('Lucida Grande', 11)
        self.__ui.labelPassword.setFont(fontB)
        self.__ui.labelKeySecret.setFont(fontB)
        self.__ui.labelCurrency.setFont(fontB)

    def __get(self, key):
        '''
        Retrieves a property from the global section
        '''
        return self.configparser.get(self.__SECTION_GLOBAL, key)

    def __set(self, key, value):
        '''
        Stores a property to the global section
        '''
        self.configparser.set(self.__SECTION_GLOBAL, key, value)

    # end private methods

    # start public methods

    def set_fiat_currencies(self, currencies):
        '''
        Sets the fiat currencies available in the preferences dialog.
        '''
        self.__fiat_currencies = currencies

        self.__ui.comboBoxCurrency.clear()
        index = 0
        for x in self.__fiat_currencies:
            self.__ui.comboBoxCurrency.insertItem(index, x.symbol)
            index += 1

    def set_currency(self, index, currency):
        return self.__set('currency_{}'.format(index), currency.symbol)

    def get_currency(self, index):
        return Currency(self.__get('currency_{}'.format(index)))

    def get_key(self):
        '''
        Loads the key from the configuration file.
        '''
        return self.__get('key')

    def get_secret(self):
        '''
        Loads the secret from the configuration file.
        '''
        secret = self.__get('secret')
        if secret == '':
            return secret

        return utilities.decrypt(secret, Preferences.__PASSPHRASE)

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
