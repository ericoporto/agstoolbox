from __future__ import annotations  # for python 3.8
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget


def returned_folder_is_valid(folderpath: str) -> bool:
    return folderpath is not None and \
           Path(folderpath).exists() and \
           Path(folderpath).is_dir()


class DirListWidget(QWidget):
    proj_update_task = None

    def appendDir(self, d):
        itm = QtWidgets.QListWidgetItem(text=d, parent=self.list)
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
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

        if not returned_folder_is_valid(folderpath):
            return

        folderpath = str(Path(str(folderpath)).as_posix())
        self.appendDir(folderpath)

    def btn_edit_clicked(self):
        if self.list.count() == 0:
            return

        itm = self.getSelectedItem()
        folderpath = itm.text()
        if not returned_folder_is_valid(folderpath):
            folderpath = None

        folderpath = QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select Folder', directory=folderpath)

        if not returned_folder_is_valid(folderpath):
            return

        folderpath = str(Path(str(folderpath)).as_posix())
        itm.setText(folderpath)

    def btn_del_clicked(self):
        if self.list.count() == 0:
            return

        itm = self.getSelectedItem()
        self.list.removeItemWidget(itm)

    def __init__(self, dirs: list[str], parent: QWidget = None):
        QWidget.__init__(self, parent)

        self.setObjectName("dir_list_widget")
        self.resize(600, 600)

        self.list = QtWidgets.QListWidget(self)
        self.list.setObjectName("list")
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
        self.push_button_move_down = QtWidgets.QPushButton(self)
        self.push_button_move_down.setObjectName("push_button_move_down")

        # Do Layout
        spacer_item_fixed = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        spacer_item_expanding = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.list)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.addWidget(self.push_button_new)
        self.verticalLayout.addWidget(self.push_button_edit)
        self.verticalLayout.addWidget(self.push_button_del)
        self.verticalLayout.addItem(spacer_item_fixed)
        self.verticalLayout.addWidget(self.push_button_move_up)
        self.verticalLayout.addWidget(self.push_button_move_down)
        self.verticalLayout.addItem(spacer_item_expanding)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi()

        # Connect events
        self.push_button_new.clicked.connect(self.btn_new_clicked)
        self.push_button_del.clicked.connect(self.btn_del_clicked)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("dir_list_widget", "Directories"))
        self.push_button_new.setText(_translate("dir_list_widget", "New"))
        self.push_button_edit.setText(_translate("dir_list_widget", "Edit"))
        self.push_button_del.setText(_translate("dir_list_widget", "Delete"))
        self.push_button_move_up.setText(_translate("dir_list_widget", "Move Up"))
        self.push_button_move_down.setText(_translate("dir_list_widget", "Move Down"))


