from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QSizePolicy, QFormLayout, QHBoxLayout, \
    QVBoxLayout, QSpacerItem, QPushButton, QLabel, QLineEdit, QDialogButtonBox

from agstoolbox.core.settings import Settings
from agstoolbox.wdgts.at_dirlist_wdgt import DirListWidget


class Ui_SettingsDialog(QDialog):
    def __init__(self, parent: QtWidgets = None):
        QDialog.__init__(self, parent)
        self.setObjectName("SettingsDialog")
        self.resize(512, 400)
        self.setSizeGripEnabled(True)

        self.label_settings_intro = QLabel(self)
        self.label_settings_intro.setObjectName("label_settings_intro")

        self.base_install_dir_label = QLabel(self)
        self.base_install_dir_label.setObjectName("base_install_dir_label")

        self.install_dir_line_edit = QLineEdit(self)
        self.install_dir_line_edit.setEnabled(False)
        self.install_dir_line_edit.setObjectName("install_dir_line_edit")

        self.install_dir_edit_button = QPushButton(self)
        self.install_dir_edit_button.setObjectName("install_dir_edit_button")

        self.install_dir_defaults_button = QPushButton(self)
        self.install_dir_defaults_button.setObjectName("install_dir_defaults_button")

        self.label_editors = QtWidgets.QLabel(self)
        self.label_editors.setWordWrap(True)
        self.label_editors.setObjectName("label_editors")

        self.external_editors_dir_search_list = DirListWidget(parent=self, dirs=[])
        self.external_editors_dir_search_list.setObjectName("external_editors_dir_search_list")

        self.label_projects = QtWidgets.QLabel(self)
        self.label_projects.setWordWrap(True)
        self.label_projects.setObjectName("label_projects")

        self.project_dir_search_list = DirListWidget(parent=self, dirs=[])
        self.project_dir_search_list.setObjectName("project_dir_search_list")

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
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole,
                                  self.base_install_dir_label)

        self.h_layout_install_dir = QHBoxLayout()
        self.h_layout_install_dir.setObjectName("horizontalLayout_2")
        self.h_layout_install_dir.addWidget(self.install_dir_line_edit)
        self.h_layout_install_dir.addWidget(self.install_dir_edit_button)
        self.h_layout_install_dir.addWidget(self.install_dir_defaults_button)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.ItemRole.FieldRole,
                                  self.h_layout_install_dir)

        # manual editor search dirs
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.external_editors_dir_search_list)
        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole,
                                  self.horizontalLayout)
        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_editors)

        # project search dirs
        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.horizontalLayout2.addWidget(self.project_dir_search_list)
        self.formLayout.setLayout(2, QFormLayout.ItemRole.FieldRole,
                                  self.horizontalLayout2)
        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_projects)

        self.verticalLayout_3.addLayout(self.formLayout)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacer_item)
        self.verticalLayout_3.addWidget(self.button_box)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.apply_from_settings_to_dialog()
        self.button_box.accepted.connect(self.clicked_ok)
        self.button_box.rejected.connect(self.clicked_cancel)


    def apply_from_settings_to_dialog(self):
        dirs = Settings().get_manually_installed_editors_search_dirs()
        self.external_editors_dir_search_list.setDirs(dirs)

        dirs = Settings().get_project_search_dirs()
        self.project_dir_search_list.setDirs(dirs)

        self.install_dir_line_edit.setText(Settings().get_tools_install_dir())

    def apply_from_dialog_to_settings(self):
        dirs = self.external_editors_dir_search_list.getDirs()
        Settings().set_manually_installed_editors_search_dirs(dirs)

        dirs = self.project_dir_search_list.getDirs()
        Settings().set_project_search_dirs(dirs)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingsDialog", "SettingsDialog"))
        self.label_settings_intro.setText(
            _translate("SettingsDialog", "Adjust AGS Toolbox settings here."))
        self.base_install_dir_label.setText(_translate("SettingsDialog", "Base install dir"))
        self.install_dir_edit_button.setText(_translate("SettingsDialog", "Edit"))
        self.install_dir_defaults_button.setText(_translate("SettingsDialog", "Set Defaults"))
        self.label_editors.setText(
            _translate("SettingsDialog", "Externally installed AGS Editors search paths"))
        self.label_projects.setText(
            _translate("SettingsDialog", "AGS Game Projects search paths"))

    def closeEvent(self, evnt):
        QDialog.closeEvent(self, evnt)

    def clicked_ok(self):
        self.apply_from_dialog_to_settings()
        self.accept()

    def clicked_cancel(self):
        self.reject()
