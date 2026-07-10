from __future__ import annotations  # for python 3.8

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout

from agstoolbox.core.ags.ags_export import export_script_module_from_project_to_file, \
    get_default_module_filename
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.get_script_module import get_list_of_script_modules, \
    exists_module_in_game_project


class ScriptsModuleDialog(QDialog):
    def __init__(self, parent: QtWidgets = None):
        QDialog.__init__(self, parent)

        self.setObjectName("ScriptsModuleDialog")
        self.resize(512, 400)
        self.setSizeGripEnabled(True)

        self.game_project: GameProject | None = None
        self.scripts_modules: list[str] | None = None
        self.selected_script_module: str | None = None

        self.label_scriptsmodule_intro = QLabel(self)
        self.label_scriptsmodule_intro.setObjectName("label_scriptsmodule_intro")
        self.label_scriptsmodule_intro.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.list_of_scripts_modules = QListWidget(self)
        self.list_of_scripts_modules.setObjectName("list_of_scripts_modules")

        self.label_selected_script_module = QLabel(self)
        self.label_selected_script_module.setObjectName("label_selected_script_module")
        self.label_selected_script_module.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.button_export_script_module = QPushButton(self)
        self.button_export_script_module.setObjectName("button_export_script_module")
        self.button_export_script_module.setEnabled(False)

        self.button_cancel = QPushButton(self)
        self.button_cancel.setObjectName("button_cancel")

        self.horizontalLayout_buttons = QHBoxLayout()
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.horizontalLayout_buttons.addStretch()
        self.horizontalLayout_buttons.addWidget(self.button_cancel)
        self.horizontalLayout_buttons.addWidget(self.button_export_script_module)

        self.verticalLayout_1 = QVBoxLayout(self)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.verticalLayout_1.addWidget(self.label_scriptsmodule_intro)
        self.verticalLayout_1.addWidget(self.list_of_scripts_modules)
        self.verticalLayout_1.addWidget(self.label_selected_script_module)
        self.verticalLayout_1.addLayout(self.horizontalLayout_buttons)

        self.retranslateUi()

        self.list_of_scripts_modules.currentItemChanged.connect(self.on_selected_script_module_changed)
        self.list_of_scripts_modules.itemDoubleClicked.connect(
            lambda _item: self.button_export_script_module_clicked())
        self.button_export_script_module.clicked.connect(self.button_export_script_module_clicked)
        self.button_cancel.clicked.connect(self.clicked_cancel)
        self.update_ui_button_and_label()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("ScriptsModuleDialog",
                                       "Select Script Module to export..."))
        self.label_scriptsmodule_intro.setText(_translate("ScriptsModuleDialog",
                                                          "Select a script module to export:"))
        self.button_export_script_module.setText(_translate("ScriptsModuleDialog",
                                                            "Export Script Module"))
        self.button_cancel.setText(_translate("ScriptsModuleDialog", "Cancel"))
        self.update_ui_button_and_label()

    def set_game_project(self, game_project: GameProject):
        self.game_project = game_project
        self.scripts_modules = get_list_of_script_modules(game_project)

        self.list_of_scripts_modules.clear()
        self.list_of_scripts_modules.addItems(self.scripts_modules)
        self.selected_script_module = None

        if len(self.scripts_modules) > 0:
            self.list_of_scripts_modules.setCurrentRow(0)

        self.update_ui_button_and_label()

    def on_selected_script_module_changed(self):
        current_item = self.list_of_scripts_modules.currentItem()
        self.selected_script_module = None if current_item is None else current_item.text()
        self.update_ui_button_and_label()

    def has_valid_selection(self) -> bool:
        has_valid_selection: bool = not (
            self.game_project is None or
            self.selected_script_module is None or
            self.selected_script_module == "" or
            self.selected_script_module == "None"
        )
        return has_valid_selection

    def update_ui_button_and_label(self):
        has_valid_selection: bool = self.has_valid_selection()
        self.button_export_script_module.setEnabled(has_valid_selection)

        _translate = QtCore.QCoreApplication.translate

        if not has_valid_selection:
            self.label_selected_script_module.setText("No Script Module selected")
        else:
            self.label_selected_script_module.setText(
                "Script Module: " + self.selected_script_module)

    def show_msg_box_info(self, text: str):
        QtWidgets.QMessageBox.information(self, "Export Script Module", text)

    def show_msg_box_error(self, text: str):
        QtWidgets.QMessageBox.critical(self, "Export Script Module", text)

    def show_save_file_dialog(self, default_filename: str) -> str | None:
        selected_filename, _selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Exported Script Module",
            default_filename,
            "Script Module (*.scm)"
        )

        if not selected_filename:
            return None

        if not selected_filename.lower().endswith(".scm"):
            selected_filename += ".scm"

        return selected_filename

    def export_selected_script_module_to_file(self, file_name: str) -> bool:
        mod_name: str = self.selected_script_module
        project: GameProject = self.game_project

        if not exists_module_in_game_project(project, mod_name):
            self.show_msg_box_error(
                'ERROR: Module "' + mod_name + '" doesn\'t exist in Game Project')
            return False

        try:
            export_script_module_from_project_to_file(project, mod_name, file_name)
        except Exception as exc:
            self.show_msg_box_error("ERROR: Failed to export script module:\n" + str(exc))
            return False

        return True

    def button_export_script_module_clicked(self):
        if self.game_project is None:
            self.show_msg_box_error("ERROR: No Game Project selected")
            return

        if not self.has_valid_selection():
            self.show_msg_box_error("ERROR: No Script Module selected")
            return

        default_filename = get_default_module_filename(
            self.game_project, self.selected_script_module)

        file_name = self.show_save_file_dialog(default_filename)
        if file_name is None:
            # user cancelled the dialog, no error should be raised
            return

        success = self.export_selected_script_module_to_file(file_name)
        if not success:
            return

        self.show_msg_box_info("Script module exported to:\n" + file_name)
        self.accept()

    def clicked_cancel(self):
        self.reject()
