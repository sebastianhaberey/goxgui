# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/user/git/goxgui/goxgui/ui/main_window.ui'
#
# Created: Fri May 17 16:48:44 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(956, 858)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.widgetMain = QtGui.QWidget(MainWindow)
        self.widgetMain.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetMain.sizePolicy().hasHeightForWidth())
        self.widgetMain.setSizePolicy(sizePolicy)
        self.widgetMain.setObjectName(_fromUtf8("widgetMain"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widgetMain)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBoxAccount = QtGui.QGroupBox(self.widgetMain)
        self.groupBoxAccount.setFlat(True)
        self.groupBoxAccount.setObjectName(_fromUtf8("groupBoxAccount"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBoxAccount)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonWalletA = QtGui.QPushButton(self.groupBoxAccount)
        self.pushButtonWalletA.setEnabled(False)
        self.pushButtonWalletA.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButtonWalletA.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonWalletA.setObjectName(_fromUtf8("pushButtonWalletA"))
        self.horizontalLayout_2.addWidget(self.pushButtonWalletA)
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.labelOrderlag = QtGui.QLabel(self.groupBoxAccount)
        self.labelOrderlag.setText(_fromUtf8(""))
        self.labelOrderlag.setObjectName(_fromUtf8("labelOrderlag"))
        self.horizontalLayout_2.addWidget(self.labelOrderlag)
        spacerItem1 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonWalletB = QtGui.QPushButton(self.groupBoxAccount)
        self.pushButtonWalletB.setEnabled(False)
        self.pushButtonWalletB.setMinimumSize(QtCore.QSize(200, 0))
        self.pushButtonWalletB.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonWalletB.setObjectName(_fromUtf8("pushButtonWalletB"))
        self.horizontalLayout_2.addWidget(self.pushButtonWalletB)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBoxAccount)
        self.groupBoxTrading = QtGui.QGroupBox(self.widgetMain)
        self.groupBoxTrading.setFlat(True)
        self.groupBoxTrading.setCheckable(False)
        self.groupBoxTrading.setObjectName(_fromUtf8("groupBoxTrading"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBoxTrading)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowserStatus = QtGui.QTextBrowser(self.groupBoxTrading)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserStatus.sizePolicy().hasHeightForWidth())
        self.textBrowserStatus.setSizePolicy(sizePolicy)
        self.textBrowserStatus.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        self.textBrowserStatus.setFont(font)
        self.textBrowserStatus.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textBrowserStatus.setToolTip(_fromUtf8(""))
        self.textBrowserStatus.setFrameShape(QtGui.QFrame.WinPanel)
        self.textBrowserStatus.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowserStatus.setOpenLinks(False)
        self.textBrowserStatus.setObjectName(_fromUtf8("textBrowserStatus"))
        self.verticalLayout.addWidget(self.textBrowserStatus)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.radioButtonBuy = QtGui.QRadioButton(self.groupBoxTrading)
        self.radioButtonBuy.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButtonBuy.setChecked(True)
        self.radioButtonBuy.setObjectName(_fromUtf8("radioButtonBuy"))
        self.horizontalLayout_4.addWidget(self.radioButtonBuy)
        self.radioButtonSell = QtGui.QRadioButton(self.groupBoxTrading)
        self.radioButtonSell.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.radioButtonSell.setChecked(False)
        self.radioButtonSell.setObjectName(_fromUtf8("radioButtonSell"))
        self.horizontalLayout_4.addWidget(self.radioButtonSell)
        self.pushButtonSize = QtGui.QPushButton(self.groupBoxTrading)
        self.pushButtonSize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonSize.setObjectName(_fromUtf8("pushButtonSize"))
        self.horizontalLayout_4.addWidget(self.pushButtonSize)
        self.doubleSpinBoxSize = QtGui.QDoubleSpinBox(self.groupBoxTrading)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxSize.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxSize.setSizePolicy(sizePolicy)
        self.doubleSpinBoxSize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.doubleSpinBoxSize.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSize.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.doubleSpinBoxSize.setDecimals(8)
        self.doubleSpinBoxSize.setMaximum(999999999.0)
        self.doubleSpinBoxSize.setObjectName(_fromUtf8("doubleSpinBoxSize"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxSize)
        self.pushButtonPrice = QtGui.QPushButton(self.groupBoxTrading)
        self.pushButtonPrice.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonPrice.setObjectName(_fromUtf8("pushButtonPrice"))
        self.horizontalLayout_4.addWidget(self.pushButtonPrice)
        self.doubleSpinBoxPrice = QtGui.QDoubleSpinBox(self.groupBoxTrading)
        self.doubleSpinBoxPrice.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxPrice.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxPrice.setSizePolicy(sizePolicy)
        self.doubleSpinBoxPrice.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.doubleSpinBoxPrice.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxPrice.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.doubleSpinBoxPrice.setDecimals(5)
        self.doubleSpinBoxPrice.setMaximum(999999999.0)
        self.doubleSpinBoxPrice.setSingleStep(1.0)
        self.doubleSpinBoxPrice.setObjectName(_fromUtf8("doubleSpinBoxPrice"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxPrice)
        self.pushButtonTotal = QtGui.QPushButton(self.groupBoxTrading)
        self.pushButtonTotal.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonTotal.setObjectName(_fromUtf8("pushButtonTotal"))
        self.horizontalLayout_4.addWidget(self.pushButtonTotal)
        self.doubleSpinBoxTotal = QtGui.QDoubleSpinBox(self.groupBoxTrading)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxTotal.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxTotal.setSizePolicy(sizePolicy)
        self.doubleSpinBoxTotal.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.doubleSpinBoxTotal.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxTotal.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.doubleSpinBoxTotal.setDecimals(5)
        self.doubleSpinBoxTotal.setMaximum(999999999.0)
        self.doubleSpinBoxTotal.setSingleStep(1.0)
        self.doubleSpinBoxTotal.setObjectName(_fromUtf8("doubleSpinBoxTotal"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxTotal)
        self.pushButtonGo = QtGui.QPushButton(self.groupBoxTrading)
        self.pushButtonGo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonGo.setToolTip(_fromUtf8(""))
        self.pushButtonGo.setObjectName(_fromUtf8("pushButtonGo"))
        self.horizontalLayout_4.addWidget(self.pushButtonGo)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.lineEditOrder = QtGui.QLineEdit(self.groupBoxTrading)
        self.lineEditOrder.setObjectName(_fromUtf8("lineEditOrder"))
        self.horizontalLayout_8.addWidget(self.lineEditOrder)
        self.pushButtonCancel = QtGui.QPushButton(self.groupBoxTrading)
        self.pushButtonCancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout_8.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.verticalLayout_2.addWidget(self.groupBoxTrading)
        self.groupBoxOrder = QtGui.QGroupBox(self.widgetMain)
        self.groupBoxOrder.setFlat(True)
        self.groupBoxOrder.setObjectName(_fromUtf8("groupBoxOrder"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBoxOrder)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label = QtGui.QLabel(self.groupBoxOrder)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_6.addWidget(self.label)
        self.labelBid = QtGui.QLabel(self.groupBoxOrder)
        self.labelBid.setText(_fromUtf8(""))
        self.labelBid.setObjectName(_fromUtf8("labelBid"))
        self.horizontalLayout_6.addWidget(self.labelBid)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_2 = QtGui.QLabel(self.groupBoxOrder)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_7.addWidget(self.label_2)
        self.labelAsk = QtGui.QLabel(self.groupBoxOrder)
        self.labelAsk.setText(_fromUtf8(""))
        self.labelAsk.setObjectName(_fromUtf8("labelAsk"))
        self.horizontalLayout_7.addWidget(self.labelAsk)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tableBid = QtGui.QTableView(self.groupBoxOrder)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableBid.sizePolicy().hasHeightForWidth())
        self.tableBid.setSizePolicy(sizePolicy)
        self.tableBid.setMinimumSize(QtCore.QSize(420, 300))
        self.tableBid.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tableBid.setFrameShape(QtGui.QFrame.WinPanel)
        self.tableBid.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableBid.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableBid.setProperty("showDropIndicator", False)
        self.tableBid.setAlternatingRowColors(True)
        self.tableBid.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableBid.setGridStyle(QtCore.Qt.DotLine)
        self.tableBid.setWordWrap(False)
        self.tableBid.setCornerButtonEnabled(False)
        self.tableBid.setObjectName(_fromUtf8("tableBid"))
        self.tableBid.horizontalHeader().setCascadingSectionResizes(True)
        self.tableBid.horizontalHeader().setStretchLastSection(False)
        self.tableBid.verticalHeader().setVisible(False)
        self.tableBid.verticalHeader().setDefaultSectionSize(20)
        self.tableBid.verticalHeader().setMinimumSectionSize(20)
        self.horizontalLayout_3.addWidget(self.tableBid)
        self.tableAsk = QtGui.QTableView(self.groupBoxOrder)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableAsk.sizePolicy().hasHeightForWidth())
        self.tableAsk.setSizePolicy(sizePolicy)
        self.tableAsk.setMinimumSize(QtCore.QSize(420, 300))
        self.tableAsk.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tableAsk.setAutoFillBackground(True)
        self.tableAsk.setFrameShape(QtGui.QFrame.WinPanel)
        self.tableAsk.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableAsk.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableAsk.setProperty("showDropIndicator", False)
        self.tableAsk.setAlternatingRowColors(True)
        self.tableAsk.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableAsk.setGridStyle(QtCore.Qt.DotLine)
        self.tableAsk.setWordWrap(False)
        self.tableAsk.setCornerButtonEnabled(False)
        self.tableAsk.setObjectName(_fromUtf8("tableAsk"))
        self.tableAsk.verticalHeader().setVisible(False)
        self.tableAsk.verticalHeader().setDefaultSectionSize(20)
        self.tableAsk.verticalHeader().setMinimumSectionSize(20)
        self.horizontalLayout_3.addWidget(self.tableAsk)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBoxOrder)
        self.groupBoxLog = QtGui.QGroupBox(self.widgetMain)
        self.groupBoxLog.setFlat(True)
        self.groupBoxLog.setObjectName(_fromUtf8("groupBoxLog"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBoxLog)
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.checkBoxLogTicker = QtGui.QCheckBox(self.groupBoxLog)
        self.checkBoxLogTicker.setChecked(True)
        self.checkBoxLogTicker.setObjectName(_fromUtf8("checkBoxLogTicker"))
        self.verticalLayout_4.addWidget(self.checkBoxLogTicker)
        self.checkBoxLogSystem = QtGui.QCheckBox(self.groupBoxLog)
        self.checkBoxLogSystem.setChecked(True)
        self.checkBoxLogSystem.setObjectName(_fromUtf8("checkBoxLogSystem"))
        self.verticalLayout_4.addWidget(self.checkBoxLogSystem)
        self.checkBoxLogDepth = QtGui.QCheckBox(self.groupBoxLog)
        self.checkBoxLogDepth.setChecked(True)
        self.checkBoxLogDepth.setObjectName(_fromUtf8("checkBoxLogDepth"))
        self.verticalLayout_4.addWidget(self.checkBoxLogDepth)
        self.checkBoxLogTrade = QtGui.QCheckBox(self.groupBoxLog)
        self.checkBoxLogTrade.setChecked(True)
        self.checkBoxLogTrade.setObjectName(_fromUtf8("checkBoxLogTrade"))
        self.verticalLayout_4.addWidget(self.checkBoxLogTrade)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.textBrowserLog = QtGui.QTextBrowser(self.groupBoxLog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserLog.sizePolicy().hasHeightForWidth())
        self.textBrowserLog.setSizePolicy(sizePolicy)
        self.textBrowserLog.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        self.textBrowserLog.setFont(font)
        self.textBrowserLog.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textBrowserLog.setFrameShape(QtGui.QFrame.WinPanel)
        self.textBrowserLog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textBrowserLog.setObjectName(_fromUtf8("textBrowserLog"))
        self.horizontalLayout_5.addWidget(self.textBrowserLog)
        self.verticalLayout_2.addWidget(self.groupBoxLog)
        MainWindow.setCentralWidget(self.widgetMain)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 956, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuOptions = QtGui.QMenu(self.menuBar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.actionPreferences_2 = QtGui.QAction(MainWindow)
        self.actionPreferences_2.setObjectName(_fromUtf8("actionPreferences_2"))
        self.menuOptions.addAction(self.actionPreferences_2)
        self.menuBar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.doubleSpinBoxSize, self.doubleSpinBoxPrice)
        MainWindow.setTabOrder(self.doubleSpinBoxPrice, self.doubleSpinBoxTotal)
        MainWindow.setTabOrder(self.doubleSpinBoxTotal, self.lineEditOrder)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "goxgui", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxAccount.setTitle(QtGui.QApplication.translate("MainWindow", "Account", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonWalletA.setToolTip(QtGui.QApplication.translate("MainWindow", "Push to use this value", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonWalletA.setText(QtGui.QApplication.translate("MainWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOrderlag.setToolTip(QtGui.QApplication.translate("MainWindow", "MtGox trading lag (how long it takes for an order to be executed)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonWalletB.setToolTip(QtGui.QApplication.translate("MainWindow", "Push to use this value", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonWalletB.setText(QtGui.QApplication.translate("MainWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxTrading.setTitle(QtGui.QApplication.translate("MainWindow", "Trading", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonBuy.setText(QtGui.QApplication.translate("MainWindow", "Buy", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonSell.setText(QtGui.QApplication.translate("MainWindow", "Sell", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSize.setToolTip(QtGui.QApplication.translate("MainWindow", "Recalculate size", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSize.setText(QtGui.QApplication.translate("MainWindow", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.doubleSpinBoxSize.setToolTip(QtGui.QApplication.translate("MainWindow", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPrice.setToolTip(QtGui.QApplication.translate("MainWindow", "Suggest price", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPrice.setText(QtGui.QApplication.translate("MainWindow", "Price", None, QtGui.QApplication.UnicodeUTF8))
        self.doubleSpinBoxPrice.setToolTip(QtGui.QApplication.translate("MainWindow", "Price", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTotal.setToolTip(QtGui.QApplication.translate("MainWindow", "Recalculate total trade worth", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonTotal.setText(QtGui.QApplication.translate("MainWindow", "Total", None, QtGui.QApplication.UnicodeUTF8))
        self.doubleSpinBoxTotal.setToolTip(QtGui.QApplication.translate("MainWindow", "Total trade worth", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonGo.setText(QtGui.QApplication.translate("MainWindow", "Go!", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOrder.setToolTip(QtGui.QApplication.translate("MainWindow", "Paste order ID here or click link above", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditOrder.setPlaceholderText(QtGui.QApplication.translate("MainWindow", "Order ID", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setToolTip(QtGui.QApplication.translate("MainWindow", "Cancels the order with the specified ID", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel Order", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxOrder.setTitle(QtGui.QApplication.translate("MainWindow", "Order Book", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Bid:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Ask:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxLog.setTitle(QtGui.QApplication.translate("MainWindow", "Application Log", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxLogTicker.setText(QtGui.QApplication.translate("MainWindow", "Ticker", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxLogSystem.setText(QtGui.QApplication.translate("MainWindow", "Trade", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxLogDepth.setText(QtGui.QApplication.translate("MainWindow", "Depth", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxLogTrade.setText(QtGui.QApplication.translate("MainWindow", "System", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowserLog.setToolTip(QtGui.QApplication.translate("MainWindow", "Technical output", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences_2.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))

