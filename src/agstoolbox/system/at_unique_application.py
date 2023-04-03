from __future__ import annotations

from PyQt6 import QtCore, QtWidgets, QtNetwork

from agstoolbox.system.at_runguard import RunGuard


class unique_application(QtWidgets.QApplication):
    _run_guard: RunGuard = None
    _socket: QtNetwork.QLocalSocket = None
    _key: str = None
    _listener: QtNetwork.QLocalServer = None

    another_instance = QtCore.pyqtSignal()
    is_unique: bool = False

    def __init__(self, title: str, argv: list[str]):
        QtWidgets.QApplication.__init__(self, argv)
        self._key = "18d1411b-54a1-46fc-bd14-1d38519e2c61" + title
        self.setApplicationName(title)
        self._run_guard = RunGuard(parent=self, key=self._key)

        if not self._run_guard.unique:
            self.is_unique = False
            _socket = QtNetwork.QLocalSocket()
            _socket.connectToServer(self._key)
            _socket.close()
            return
        else:
            self.is_unique = True
            self.listener = QtNetwork.QLocalServer(self)
            self.listener.setSocketOptions(QtNetwork.QLocalServer.SocketOption.WorldAccessOption)
            self.listener.newConnection.connect(self.another_instance)
            self.listener.listen(self._key)

