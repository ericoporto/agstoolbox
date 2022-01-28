from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize

from agstoolbox.core.settings import ConstSettings
from agstoolbox.at_icons import icon_exit_as_pixmap, \
    icon_refresh_as_pixmap, icon_settings_as_pixmap


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(ConstSettings.DEFAULT_MAIN_PANEL_WIDTH,
                                  ConstSettings.DEFAULT_MAIN_PANEL_HEIGHT))
        self.setWindowTitle("Set Account")

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 302, 425))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # buttons
        self.pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout_2.addWidget(self.pushButton)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.actionSettings = QtGui.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(icon_settings_as_pixmap(), QtGui.QIcon.Mode.Normal,
                       QtGui.QIcon.State.Off)
        self.actionSettings.setIcon(icon)
        self.actionSettings.setObjectName("actionSettings")
        self.actionRefresh = QtGui.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(icon_refresh_as_pixmap(), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.actionRefresh.setIcon(icon1)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionQuit = QtGui.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(icon_exit_as_pixmap(), QtGui.QIcon.Mode.Normal,
                        QtGui.QIcon.State.Off)
        self.actionQuit.setIcon(icon2)
        self.actionQuit.setObjectName("actionQuit")
        self.actionEmpty = QtGui.QAction(self)
        self.actionEmpty.setObjectName("actionEmpty")
        self.toolBar.addAction(self.actionQuit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEmpty)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionRefresh)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.setToolTip(_translate("MainWindow", "Configure AGS Toolbox"))
        self.actionRefresh.setText(_translate("MainWindow", "Refresh"))
        self.actionRefresh.setToolTip(_translate("MainWindow", "check for new things to add now"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "Exit toolbox"))
        self.actionEmpty.setText(_translate("MainWindow", "                       "))

    def buttonClicked(self):
        print('Username: ' + self.username_field.text())
