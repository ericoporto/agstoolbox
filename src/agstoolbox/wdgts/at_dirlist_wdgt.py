from __future__ import annotations  # for python 3.8
from pathlib import Path

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QWidget, QFileDialog, QStyle, QFrame

from agstoolbox.core.settings.settings import ConstSettings
from agstoolbox.core.utils.file import dir_is_valid


class DirListWidget(QWidget):
    default_dirs_value = None

    def is_selection_valid(self) -> bool:
        if self.list.count() == 0:
            return False

        itm = self.getSelectedItem()
        if itm is None:
            return False
        row = self.list.row(itm)
        if row >= self.list.count():
            return False
        return True

    def appendDir(self, d):
        itm = QtWidgets.QListWidgetItem(d, parent=self.list)
        self.list.addItem(itm)

    def setDirs(self, dirs: list[str]):
        self.list.clear()
        for d in dirs:
            self.appendDir(d)

    def getSelectedItem(self) -> QtWidgets.QListWidgetItem:
        sel = self.list.selectedItems()

        i = self.list.count() - 1
        itm = self.list.item(i)
        if sel is not None and len(sel) > 0:
            itm = sel[0]

        return itm

    def getDirs(self) -> list[str]:
        dirs = []
        for i in range(self.list.count()):
            itm = self.list.item(i)
            d = itm.text()
            dirs.append(d)

        return dirs

    def btn_new_clicked(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, 'Select Folder',
            options=QFileDialog.Option.ShowDirsOnly,
            directory=ConstSettings().user_docs
        )

        if dir_path is None or len(dir_path) <= 1:
            return

        if not dir_is_valid(dir_path):
            return

        dir_path = str(Path(str(dir_path)).as_posix())

        self.appendDir(dir_path)

    def btn_edit_clicked(self):
        if self.list.count() == 0:
            return

        itm = self.getSelectedItem()
        dir_path = itm.text()
        if not dir_is_valid(dir_path):
            dir_path = ConstSettings().user_docs

        dir_path = QFileDialog.getExistingDirectory(
            self, 'Select Folder',
            options=QFileDialog.Option.ShowDirsOnly,
            directory=dir_path)

        if not dir_is_valid(dir_path):
            return

        dir_path = str(Path(str(dir_path)).as_posix())
        itm.setText(dir_path)

    def btn_del_clicked(self):
        if not self.is_selection_valid():
            return

        itm = self.getSelectedItem()
        row = self.list.row(itm)
        self.list.takeItem(row)
        del itm

    def btn_defaults_clicked(self):
        self.setDirs(self.default_dirs_value)

    def btn_move_up_clicked(self):
        if not self.is_selection_valid():
            return
        if self.list.count() <= 1:
            return

        itm = self.getSelectedItem()
        row = self.list.row(itm)
        if row > 0:
            self.list.takeItem(row)
            target_row = row - 1
            self.list.insertItem(target_row, itm)
            self.list.setCurrentRow(target_row)

    def btn_move_down_clicked(self):
        if not self.is_selection_valid():
            return
        if self.list.count() <= 1:
            return

        itm = self.getSelectedItem()
        row = self.list.row(itm)
        if row < self.list.count() - 1:
            self.list.takeItem(row)
            target_row = row + 1
            self.list.insertItem(target_row, itm)
            self.list.setCurrentRow(target_row)

    def __init__(self, dirs: list[str], default_dirs: list[str], parent: QWidget = None):
        QWidget.__init__(self, parent)

        self.setObjectName("dir_list_widget")

        self.default_dirs_value = default_dirs

        self.list = QtWidgets.QListWidget(self)
        self.list.setObjectName("list")
        self.list.setFrameStyle(QFrame.Shape.NoFrame)
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setDirs(dirs)

        self.push_button_new = QtWidgets.QPushButton(self)
        self.push_button_new.setObjectName("push_button_new")
        self.push_button_edit = QtWidgets.QPushButton(self)
        self.push_button_edit.setObjectName("push_button_edit")
        self.push_button_del = QtWidgets.QPushButton(self)
        self.push_button_del.setObjectName("push_button_del")

        self.push_button_move_up = QtWidgets.QPushButton(self)
        self.push_button_move_up.setObjectName("push_button_move_up")
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
        self.push_button_move_up.setIcon(icon)

        self.push_button_move_down = QtWidgets.QPushButton(self)
        self.push_button_move_down.setObjectName("push_button_move_down")
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown)
        self.push_button_move_down.setIcon(icon)

        self.push_button_defaults = QtWidgets.QPushButton(self)
        self.push_button_defaults.setObjectName("push_button_defaults")

        # Do Layout
        spacer_item_fixed = QtWidgets.QSpacerItem(
            20, 16, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        spacer_item_expanding = QtWidgets.QSpacerItem(
            20, 16, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.push_button_new)
        self.verticalLayout.addWidget(self.push_button_edit)
        self.verticalLayout.addWidget(self.push_button_del)
        self.verticalLayout.addItem(spacer_item_fixed)

        self.h_move_layout = QtWidgets.QHBoxLayout()
        self.h_move_layout.setObjectName("h_move_layout")
        self.h_move_layout.addWidget(self.push_button_move_up)
        self.h_move_layout.addWidget(self.push_button_move_down)

        self.verticalLayout.addLayout(self.h_move_layout)
        self.verticalLayout.addWidget(self.push_button_defaults)
        self.verticalLayout.addItem(spacer_item_expanding)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.list)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.setLayout(self.horizontalLayout)

        self.retranslateUi()

        # Connect events
        self.push_button_new.clicked.connect(self.btn_new_clicked)
        self.push_button_del.clicked.connect(self.btn_del_clicked)
        self.push_button_edit.clicked.connect(self.btn_edit_clicked)
        self.push_button_defaults.clicked.connect(self.btn_defaults_clicked)
        self.push_button_move_up.clicked.connect(self.btn_move_up_clicked)
        self.push_button_move_down.clicked.connect(self.btn_move_down_clicked)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        parent = "dir_list_widget"
        if self.parent() is not None:
            parent = self.parent().objectName()

        self.push_button_new.setText(_translate(parent, "New"))
        self.push_button_edit.setText(_translate(parent, "Edit"))
        self.push_button_del.setText(_translate(parent, "Delete"))
        self.push_button_defaults.setText(_translate(parent, "Set Defaults"))


