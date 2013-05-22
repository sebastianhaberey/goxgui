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

    ORDERS_COLUMN_PRICE = 0
    ORDERS_COLUMN_SIZE = 1
    ORDERS_COLUMN_QUOTE = 2
    ORDERS_COLUMN_TOTAL = 3
    ORDERS_COLUMN_TOTAL_QUOTE = 4

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
        self.__configparser = RawConfigParser({
            'grouping': '0.0',
            'currency_{}'.format(Preferences.CURRENCY_INDEX_BASE): 'BTC',
            'currency_{}'.format(Preferences.CURRENCY_INDEX_QUOTE): 'USD',
            'orders_column_{}'.format(Preferences.ORDERS_COLUMN_PRICE): 'True',
            'orders_column_{}'.format(Preferences.ORDERS_COLUMN_SIZE): 'True',
            'orders_column_{}'.format(Preferences.ORDERS_COLUMN_QUOTE): 'False', # @IgnorePep8
            'orders_column_{}'.format(Preferences.ORDERS_COLUMN_TOTAL): 'True',
            'orders_column_{}'.format(Preferences.ORDERS_COLUMN_TOTAL_QUOTE): 'False', # @IgnorePep8
            'key': '',
            'secret': '',
            'proposed_pips': '0'
        })

        # load config file (if exists)
        if path.isfile(self.__FILENAME):
            self.__load()

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

    def __get_fiat_currency_index(self, other):
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

    def __load_to_gui(self):
        self.__ui.doubleSpinBoxGrouping.setValue(self.get_grouping())
        self.__ui.lineEditKey.setText(self.get_key())
        self.__ui.lineEditSecret.setText(self.get_secret())
        quoteCurrency = self.get_currency(Preferences.CURRENCY_INDEX_QUOTE)
        index = self.__get_fiat_currency_index(quoteCurrency)
        self.__ui.comboBoxCurrency.setCurrentIndex(index)
        self.__set_status('')
        self.__ui.checkBoxPrice.setChecked(self.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_PRICE))
        self.__ui.checkBoxSize.setChecked(self.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_SIZE))
        self.__ui.checkBoxTotal.setChecked(self.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_TOTAL))
        self.__ui.checkBoxQuote.setChecked(self.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_QUOTE))
        self.__ui.checkBoxTotalQuote.setChecked(self.is_orders_column_enabled(
            Preferences.ORDERS_COLUMN_TOTAL_QUOTE))
        self.__ui.doubleSpinBoxOffset.setValue(self.get_proposed_pips())

    def __save_from_gui(self):
        self.set_grouping(self.__ui.doubleSpinBoxGrouping.value())
        self.__set_key(str(self.__ui.lineEditKey.text()))
        self.__set_secret(str(self.__ui.lineEditSecret.text()))
        quoteCurrency = Currency(str(self.__ui.comboBoxCurrency.currentText()))
        self.set_currency(Preferences.CURRENCY_INDEX_QUOTE, quoteCurrency)
        self.set_orders_column_enabled(Preferences.ORDERS_COLUMN_PRICE,
            self.__ui.checkBoxPrice.isChecked())
        self.set_orders_column_enabled(Preferences.ORDERS_COLUMN_SIZE,
            self.__ui.checkBoxSize.isChecked())
        self.set_orders_column_enabled(Preferences.ORDERS_COLUMN_TOTAL,
            self.__ui.checkBoxTotal.isChecked())
        self.set_orders_column_enabled(Preferences.ORDERS_COLUMN_QUOTE,
            self.__ui.checkBoxQuote.isChecked())
        self.set_orders_column_enabled(Preferences.ORDERS_COLUMN_TOTAL_QUOTE,
            self.__ui.checkBoxTotalQuote.isChecked())
        self.set_proposed_pips(self.__ui.doubleSpinBoxOffset.value())

    def __has_option(self, option):
        return self.__configparser.has_option(self.__SECTION_GLOBAL, option)

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
            self.__configparser.write(configfile)

    def __load(self):
        '''
        Loads or reloads the config from the .ini file
        '''
        self.__configparser.read(self.__FILENAME)

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
        self.__ui.labelColumns.setFont(fontB)
        self.__ui.labelGrouping.setFont(fontB)
        self.__ui.labelOffset.setFont(fontB)

    def __get(self, key):
        '''
        Retrieves a property from the global section
        '''
        return self.__configparser.get(self.__SECTION_GLOBAL, key)

    def __set(self, key, value):
        '''
        Stores a property to the global section
        '''
        self.__configparser.set(self.__SECTION_GLOBAL, key, value)

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
        self.__set('currency_{}'.format(index), currency.symbol)

    def get_currency(self, index):
        return Currency(self.__get('currency_{}'.format(index)))

    def set_orders_column_enabled(self, column, enabled):
        self.__set('orders_column_{}'.format(column), str(enabled))

    def is_orders_column_enabled(self, column):
        return self.__get('orders_column_{}'.format(column)) == 'True'

    def set_proposed_pips(self, pips):
        self.__set('proposed_pips', str(long(pips)))

    def get_proposed_pips(self):
        return long(self.__get('proposed_pips'))

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

    def get_grouping(self):
        '''
        Loads the grouping size from the configuration file.
        '''
        return float(self.__get('grouping'))

    def set_grouping(self, grouping):
        '''
        Saves the grouping size into the configuration file.
        '''
        return self.__set('grouping', grouping)

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
