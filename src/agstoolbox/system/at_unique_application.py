from PyQt6 import QtWidgets

from agstoolbox.system.at_runguard import RunGuard


class unique_application(QtWidgets.QApplication):
    _run_guard: RunGuard = None

    def __init__(self, title: str, argv: list[str]):
        QtWidgets.QApplication.__init__(self, argv)
        self.setApplicationName(title)
        self._run_guard = RunGuard(parent=self, key="18d1411b-54a1-46fc-bd14-1d38519e2c61" + title)

        if not self._run_guard.unique:
            exit()
