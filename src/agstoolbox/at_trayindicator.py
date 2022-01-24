from PyQt6 import QtWidgets, QtCore, QtGui


class AtTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        action_open_toolbox = QtGui.QAction('Open Toolbox', self)
        action_open_toolbox.triggered.connect(self.exit) # load main panel

        action_quit_toolbox = QtGui.QAction('Quit Toolbox', self)
        action_quit_toolbox.triggered.connect(self.exit)

        menu.addAction(action_open_toolbox)
        menu.addAction(action_quit_toolbox)
        self.setContextMenu(menu)

    def exit(self):
        QtCore.QCoreApplication.exit()
