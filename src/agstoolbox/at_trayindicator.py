from sys import exit
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QSystemTrayIcon

from agstoolbox.panels.at_mainpanel import MainWindow
from agstoolbox.at_icons import main_icon
from agstoolbox.core.settings.settings import ConstSettings
from agstoolbox import __title__
from agstoolbox.core.utils.math import clamp
from agstoolbox.system.at_unique_application import unique_application


class AtTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.window = MainWindow()
        self.window.refresh_all()
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
        tray_icon_rect = self.geometry()
        window_pos = QtCore.QRect()
        window_pos.setSize(QtCore.QSize(
            ConstSettings().DEFAULT_MAIN_PANEL_WIDTH,
            ConstSettings().DEFAULT_MAIN_PANEL_HEIGHT
        ))

        available_geometry = QtGui.QGuiApplication.primaryScreen().availableGeometry()

        pos_x = clamp(tray_icon_rect.x(),
                      available_geometry.x() + 48,
                      available_geometry.width() - available_geometry.x() -
                      window_pos.width() - 48)
        pos_y = clamp(tray_icon_rect.y(),
                      available_geometry.y() + 48,
                      available_geometry.height() - available_geometry.y() -
                      window_pos.height() - 48)

        window_pos.setX(pos_x)
        window_pos.setY(pos_y)
        self.window.setGeometry(window_pos)
        self.window.setWindowState(
            self.window.windowState() &
            ~QtCore.Qt.WindowState.WindowMinimized | QtCore.Qt.WindowState.WindowActive)
        self.window.raise_()
        self.window.show()
        self.window.activateWindow()

    def single_clicked(self):
        self.open_toolbox()

    def double_clicked(self):
        self.open_toolbox()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.disambiguateTimer.start(ConstSettings().double_click_interval)
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.disambiguateTimer.stop()
            self.double_clicked()

    def disambiguateTimerTimeout(self):
        self.single_clicked()


class UniqueWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        QtWidgets.QApplication.instance().another_instance.connect(self.another_instance)

    def another_instance(self):
        self.findChild(AtTrayIcon, __title__).open_toolbox()


def run_tray_indicator(ap_args):
    app = unique_application(__title__, ap_args)
    if not app.is_unique:
        app.exit()
        exit(1)

    # this prevents the tray to close if the main panel is closed,
    # we only exit when quit is explicitly clicked
    app.setQuitOnLastWindowClosed(False)
    ConstSettings().double_click_interval = app.doubleClickInterval()

    w = UniqueWidget()
    tray_icon = AtTrayIcon(main_icon(), w)
    tray_icon.setObjectName(__title__)
    tray_icon.show()
    exit(app.exec())
