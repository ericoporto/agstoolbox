from PyQt6 import QtCore


class RunGuard:
    _shared: QtCore.QSharedMemory = None
    unique: bool = False

    def __init__(self, parent: QtCore.QObject, key: str):
        self._shared = QtCore.QSharedMemory(key, parent)

        # If we can attach, another instance is running
        # This is safe on macOS and still works on Windows
        # Should work on Linux too, but haven't tested yet
        if self._shared.attach():
            print('This app is already running!')
            self.unique = False
            return

        self.unique = self._shared.create(512, QtCore.QSharedMemory.AccessMode.ReadWrite)

        if not self.unique:
            print('ERROR: Failed to create shared memory: ' + self._shared.errorString())
