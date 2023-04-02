from PyQt6 import QtCore


class RunGuard:
    _shared: QtCore.QSharedMemory = None
    unique: bool = False

    def __init__(self, parent: QtCore.QObject, key: str):
        self._shared = QtCore.QSharedMemory(key, parent)
        self.unique = self._shared.create(512, QtCore.QSharedMemory.AccessMode.ReadWrite)

        if not self.unique:
            print('This app is already running!')
