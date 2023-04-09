from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QDialog, QSizePolicy, QFormLayout, QHBoxLayout, QVBoxLayout, \
    QSpacerItem, QLabel, QDialogButtonBox

from agstoolbox.core.settings.settings import Settings, ConstSettings
from agstoolbox.wdgts.at_dirlist_wdgt import DirListWidget
from agstoolbox.wdgts.at_single_dir_wdgt import DirEditWidget
from agstoolbox.wdgts_utils.get_self_path import get_app_path
from agstoolbox import __version__


class SettingsDialog(QDialog):
    def __init__(self, parent: QtWidgets = None):
        QDialog.__init__(self, parent)
        self.setObjectName("SettingsDialog")
        self.resize(512, 400)
        self.setSizeGripEnabled(True)

        self.label_settings_intro = QLabel(self)
        self.label_settings_intro.setObjectName("label_settings_intro")
        self.label_settings_intro.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.run_at_startup_label = QLabel(self)
        self.run_at_startup_label.setObjectName("run_at_startup_label")
        self.run_at_startup_checkbox = QtWidgets.QCheckBox(self)
        self.run_at_startup_checkbox.setObjectName("run_at_startup_checkbox")

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

        # run at startup
        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole,
                                  self.run_at_startup_checkbox)
        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.run_at_startup_label)

        # manual editor search dirs
        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole,
                                  self.external_editors_dir_search_list)
        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_editors)

        # project search dirs
        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole,
                                  self.project_dir_search_list)
        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_projects)

        # install tools dir
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole,
                                  self.install_dir_line_edit)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole,
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
        Settings().set_app_path(get_app_path())

        run_at_startup = Settings().get_run_when_os_starts()
        self.run_at_startup_checkbox.setChecked(run_at_startup)

        dirs = Settings().get_manually_installed_editors_search_dirs()
        self.external_editors_dir_search_list.setDirs(dirs)

        dirs = Settings().get_project_search_dirs()
        self.project_dir_search_list.setDirs(dirs)

        install_dir = Settings().get_tools_install_dir()
        self.install_dir_line_edit.setText(install_dir)

    def apply_from_dialog_to_settings(self):
        Settings().set_app_path(get_app_path())

        run_at_startup = self.run_at_startup_checkbox.isChecked()
        Settings().set_run_when_os_starts(run_at_startup)

        dirs = self.external_editors_dir_search_list.getDirs()
        Settings().set_manually_installed_editors_search_dirs(dirs)

        dirs = self.project_dir_search_list.getDirs()
        Settings().set_project_search_dirs(dirs)

        install_dir = self.install_dir_line_edit.text()
        try:
            Settings().set_tools_install_dir(install_dir)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "tools installation dir not found and not set.")

        try:
            Settings().save()
        except OSError:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "failed to save settings.")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self.label_settings_intro.setText(
            "AGS Toolbox " + __version__ + ". " +
            _translate("SettingsDialog", "Adjust settings here."))
        self.run_at_startup_label.setText(
            _translate("SettingsDialog",
                       "Run on OS startup (experimental)"))
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
        self.accept()

    def clicked_cancel(self):
        self.reject()

    def accept(self) -> None:
        self.apply_from_dialog_to_settings()
        self.apply_from_settings_to_dialog()
        QDialog.accept(self)

    def reject(self) -> None:
        self.apply_from_settings_to_dialog()
        QDialog.reject(self)
