from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialogButtonBox, QSizePolicy, QFormLayout, QHBoxLayout, QVBoxLayout, \
    QSpacerItem, QPushButton, QLabel, QLineEdit, QDialogButtonBox

from agstoolbox.wdgts.at_dirlist_wdgt import DirListWidget


class Ui_SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setObjectName("SettingsDialog")
        self.resize(480, 400)
        self.setSizeGripEnabled(True)

        self.label_settings_intro = QLabel(self)
        self.label_settings_intro.setObjectName("label_settings_intro")

        self.baseInstallDirLabel = QLabel(self)
        self.baseInstallDirLabel.setObjectName("baseInstallDirLabel")

        self.install_dir_line_edit = QLineEdit(self)
        self.install_dir_line_edit.setEnabled(False)
        self.install_dir_line_edit.setObjectName("install_dir_line_edit")

        self.install_dir_edit_button = QPushButton(self)
        self.install_dir_edit_button.setObjectName("install_dir_edit_button")

        self.install_dir_defaults_button = QPushButton(self)
        self.install_dir_defaults_button.setObjectName("install_dir_defaults_button")

        self.external_editors_dir_search_list = DirListWidget(parent=self, dirs=[])
        self.external_editors_dir_search_list.setObjectName("external_editors_dir_search_list")

        self.label = QtWidgets.QLabel(self)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.button_box.setObjectName("buttonBox")

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_3 = QHBoxLayout(self)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.addWidget(self.label_settings_intro)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole,
                                  self.baseInstallDirLabel)

        self.h_layout_install_dir = QHBoxLayout()
        self.h_layout_install_dir.setObjectName("horizontalLayout_2")
        self.h_layout_install_dir.addWidget(self.install_dir_line_edit)
        self.h_layout_install_dir.addWidget(self.install_dir_edit_button)
        self.h_layout_install_dir.addWidget(self.install_dir_defaults_button)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.ItemRole.FieldRole,
                                  self.h_layout_install_dir)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.external_editors_dir_search_list)
        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole,
                                  self.horizontalLayout)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)
        self.verticalLayout_3.addLayout(self.formLayout)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                            QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacer_item)
        self.verticalLayout_3.addWidget(self.button_box)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.button_box.accepted.connect(self.clicked_ok)
        self.button_box.rejected.connect(self.clicked_cancel)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingsDialog", "SettingsDialog"))
        self.label_settings_intro.setText(
            _translate("SettingsDialog", "Adjust AGS Toolbox settings here."))
        self.baseInstallDirLabel.setText(_translate("SettingsDialog", "Base install dir"))
        self.install_dir_edit_button.setText(_translate("SettingsDialog", "Edit"))
        self.install_dir_defaults_button.setText(_translate("SettingsDialog", "Set Defaults"))
        self.label.setText(
            _translate("SettingsDialog", "Externally installed AGS Editors search paths"))

    def clicked_ok(self):
        self.accept()

    def clicked_cancel(self):
        self.reject()
