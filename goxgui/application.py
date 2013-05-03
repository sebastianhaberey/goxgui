'''

    Bitcoin trading tool for MtGox

    Copyright (c) 2013 Sebastian Haberey <sebastian@parango.de>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA 02110-1301, USA.

'''

import logging
import sys
import utilities

from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import SIGNAL
from view import View
from market import Market
from preferences import Preferences


class Application(QApplication):
    '''
    The main application class where the main objects
    are set up and connected with each other.
    '''

    def __init__(self, *args):

        QApplication.__init__(self, *args)

        # initialize logging
        logging.basicConfig(filename='log.txt', level=logging.INFO,
            format='%(asctime)s %(message)s')
        logging.info("Starting application.")

        # initialize user preferences
        preferences = Preferences()

        # initialize model
        market = Market(preferences)

        # initialize view
        self.view = View(preferences, market)

        self.connect(self, SIGNAL('lastWindowClosed()'), self.__quit)

    def __quit(self):
        self.view.stop()


if __name__ == '__main__':
    app = Application(sys.argv)
    app.setWindowIcon(QIcon(utilities.resource_path('bitcoin.png')))
    app.exec_()
