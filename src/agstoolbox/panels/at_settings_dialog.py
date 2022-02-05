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

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setObjectName("pushButton_2")

        self.listWidget = DirListWidget(parent=self, dirs=[])
        self.listWidget.setObjectName("listWidget")

        self.label = QtWidgets.QLabel(self)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_3 = QHBoxLayout(self)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.addWidget(self.label_settings_intro)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole,
                                  self.baseInstallDirLabel)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.ItemRole.FieldRole,
                                  self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.listWidget)
        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole,
                                  self.horizontalLayout)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)
        self.verticalLayout_3.addLayout(self.formLayout)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                            QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacer_item)
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingsDialog", "SettingsDialog"))
        self.label_settings_intro.setText(
            _translate("SettingsDialog", "Adjust AGS Toolbox settings here."))
        self.baseInstallDirLabel.setText(_translate("SettingsDialog", "Base install dir"))
        self.pushButton.setText(_translate("SettingsDialog", "Edit"))
        self.pushButton_2.setText(_translate("SettingsDialog", "Set Defaults"))
        self.label.setText(
            _translate("SettingsDialog", "Externally installed AGS Editors search paths"))
