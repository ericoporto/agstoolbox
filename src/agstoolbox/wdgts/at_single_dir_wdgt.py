from __future__ import annotations  # for python 3.8
from pathlib import Path

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QFileDialog, QLineEdit, QPushButton, QHBoxLayout

from agstoolbox.core.settings.settings import ConstSettings
from agstoolbox.core.utils.file import dir_is_valid


class DirEditWidget(QWidget):
    default_dir_value = None

    def __init__(self, initial_dir: str, default_dir: str, parent: QWidget = None):
        QWidget.__init__(self, parent)

        self.dir_line_edit = QLineEdit(self)
        self.dir_line_edit.setEnabled(False)
        self.dir_line_edit.setObjectName("dir_line_edit")

        self.dir_edit_button = QPushButton(self)
        self.dir_edit_button.setObjectName("dir_edit_button")

        self.dir_defaults_button = QPushButton(self)
        self.dir_defaults_button.setObjectName("dir_defaults_button")

        self.h_layout = QHBoxLayout(self)
        self.h_layout.setObjectName("h_layout")
        self.h_layout.addWidget(self.dir_line_edit)
        self.h_layout.addWidget(self.dir_edit_button)
        self.h_layout.addWidget(self.dir_defaults_button)
        self.setLayout(self.h_layout)

        self.dir_line_edit.setText(initial_dir)
        self.default_dir_value = default_dir

        self.retranslateUi()

        self.dir_edit_button.clicked.connect(self.btn_edit_clicked)
        self.dir_defaults_button.clicked.connect(self.btn_defaults_clicked)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        parent = ""
        if self.parent() is not None:
            parent = self.parent().objectName()

        self.dir_edit_button.setText(_translate(parent, "Edit"))
        self.dir_defaults_button.setText(_translate(parent, "Set Defaults"))

    def btn_edit_clicked(self):
        dir_path = self.dir_line_edit.text()
        if not dir_is_valid(dir_path):
            dir_path = ConstSettings().user_docs

        dir_path = QFileDialog.getExistingDirectory(
            self, 'Select Folder',
            options=QFileDialog.Option.ShowDirsOnly,
            directory=dir_path)

        if not dir_is_valid(dir_path):
            return

        dir_path = str(Path(str(dir_path)).as_posix())
        self.dir_line_edit.setText(dir_path)

    def btn_defaults_clicked(self):
        self.dir_line_edit.setText(self.default_dir_value)

    def setText(self, text: str):
        self.dir_line_edit.setText(text)

    def text(self) -> str:
        return self.dir_line_edit.text()
