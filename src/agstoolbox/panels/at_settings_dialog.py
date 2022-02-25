from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QSizePolicy, QFormLayout, QHBoxLayout, \
    QVBoxLayout, QSpacerItem, QPushButton, QLabel, QLineEdit, QDialogButtonBox

from agstoolbox.core.settings import Settings, ConstSettings
from agstoolbox.wdgts.at_dirlist_wdgt import DirListWidget
from agstoolbox.wdgts.at_single_dir_wdgt import DirEditWidget


class SettingsDialog(QDialog):
    def __init__(self, parent: QtWidgets = None):
        QDialog.__init__(self, parent)
        self.setObjectName("SettingsDialog")
        self.resize(512, 400)
        self.setSizeGripEnabled(True)

        self.label_settings_intro = QLabel(self)
        self.label_settings_intro.setObjectName("label_settings_intro")

        self.base_install_dir_label = QLabel(self)
        self.base_install_dir_label.setObjectName("base_install_dir_label")

        self.install_dir_line_edit = DirEditWidget(
            parent=self,
            initial_dir=Settings().get_tools_install_dir(),
            default_dir=ConstSettings().DEFAULT_TOOLS_INSTALL_DIR)

        self.label_editors = QtWidgets.QLabel(self)
        self.label_editors.setWordWrap(True)
        self.label_editors.setObjectName("label_editors")

        self.external_editors_dir_search_list = DirListWidget(
            parent=self,
            default_dirs=ConstSettings().DEFAULT_EXT_EDITORS_SEARCH_DIRS,
            dirs=[])
        self.external_editors_dir_search_list.setObjectName("external_editors_dir_search_list")

        self.label_projects = QtWidgets.QLabel(self)
        self.label_projects.setWordWrap(True)
        self.label_projects.setObjectName("label_projects")

        self.project_dir_search_list = DirListWidget(
            parent=self,
            default_dirs=ConstSettings().DEFAULT_PROJECTS_SEARCH_DIRS,
            dirs=[])
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

        # manual editor search dirs
        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole,
                                  self.external_editors_dir_search_list)
        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_editors)

        # project search dirs
        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole,
                                  self.project_dir_search_list)
        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_projects)

        # install tools dir
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole,
                                  self.install_dir_line_edit)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole,
                                  self.base_install_dir_label)

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

        install_dir = Settings().get_tools_install_dir()
        self.install_dir_line_edit.setText(install_dir)

    def apply_from_dialog_to_settings(self):
        dirs = self.external_editors_dir_search_list.getDirs()
        Settings().set_manually_installed_editors_search_dirs(dirs)

        dirs = self.project_dir_search_list.getDirs()
        Settings().set_project_search_dirs(dirs)

        install_dir = self.install_dir_line_edit.text()
        if install_dir == ConstSettings().DEFAULT_TOOLS_INSTALL_DIR:
            return

        try:
            Settings().set_tools_install_dir(install_dir)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "tools installation dir not found and not set.")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.label_settings_intro.setText(
            _translate("SettingsDialog", "Adjust AGS Toolbox settings here."))
        self.base_install_dir_label.setText(_translate("SettingsDialog", "Base install dir"))
        self.label_editors.setText(
            _translate("SettingsDialog", "Externally installed AGS Editors search paths"))
        self.label_projects.setText(
            _translate("SettingsDialog", "AGS Game projects search paths"))
        self.install_dir_line_edit.retranslateUi()
        self.project_dir_search_list.retranslateUi()
        self.external_editors_dir_search_list.retranslateUi()

    def closeEvent(self, evnt):
        QDialog.closeEvent(self, evnt)

    def clicked_ok(self):
        self.apply_from_dialog_to_settings()
        self.accept()

    def clicked_cancel(self):
        self.reject()
