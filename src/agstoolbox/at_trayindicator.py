from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QSystemTrayIcon

from at_mainpanel import MainWindow
from agstoolbox.configs import double_click_interval


class AtTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.window = MainWindow()
        menu = QtWidgets.QMenu(parent)

        self.activated.connect(self.onTrayIconActivated)

        action_open_toolbox = QtGui.QAction('Open Toolbox', self)
        action_open_toolbox.triggered.connect(self.open_toolbox)  # load main panel

        action_quit_toolbox = QtGui.QAction('Quit Toolbox', self)
        action_quit_toolbox.triggered.connect(self.exit)

        menu.addAction(action_open_toolbox)
        menu.addAction(action_quit_toolbox)
        self.setContextMenu(menu)

        self.disambiguateTimer = QTimer(self)
        self.disambiguateTimer.setSingleShot(True)
        self.disambiguateTimer.timeout.connect(self.disambiguateTimerTimeout)

    def exit(self):
        QtCore.QCoreApplication.exit()

    def open_toolbox(self):
        self.window.show()

    def single_clicked(self):
        self.open_toolbox()

    def double_clicked(self):
        self.open_toolbox()

    def onTrayIconActivated(self, reason):
        global double_click_interval
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.disambiguateTimer.start(double_click_interval)
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.disambiguateTimer.stop()
            self.double_clicked()

    def disambiguateTimerTimeout(self):
        self.single_clicked()
