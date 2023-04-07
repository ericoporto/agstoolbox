from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QSize

from agstoolbox.core.settings.settings import ConstSettings
from agstoolbox.at_icons import icon_refresh, icon_settings, main_icon
from agstoolbox.panels.at_settings_dialog import SettingsDialog
from agstoolbox.wdgts.at_tree_projects_wdgt import ProjectsTree
from agstoolbox.wdgts.at_tree_tools_wdgt import ToolsTree


class MainWindow(QMainWindow):
    proj_update_task = None
    tool_update_task = None

    def __init__(self):
        QMainWindow.__init__(self)

        margin = 4

        self.setWindowTitle("AGS Toolbox")
        self.setObjectName("AgsToolbox")

        self.setWindowIcon(main_icon())

        self.setMinimumSize(QSize(ConstSettings().DEFAULT_MAIN_PANEL_WIDTH,
                                  ConstSettings().DEFAULT_MAIN_PANEL_HEIGHT))
        self.resize(QSize(ConstSettings().DEFAULT_MAIN_PANEL_WIDTH,
                          ConstSettings().DEFAULT_MAIN_PANEL_HEIGHT))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(margin, margin, margin, margin)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Tools
        self.tabTools = QtWidgets.QTabBar(self)
        self.tabTools.setObjectName("tabTools")
        self.tabTools.setDrawBase(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabTools)
        self.verticalLayout_2.setContentsMargins(margin, margin, margin, margin)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeTools = ToolsTree(parent=self)
        self.verticalLayout_2.addWidget(self.treeTools)
        self.tabWidget.addTab(self.tabTools, "")

        # Projects
        self.tabProjects = QtWidgets.QTabBar(self)
        self.tabProjects.setObjectName("tabProjects")
        self.tabProjects.setDrawBase(False)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabProjects)
        self.verticalLayout_3.setContentsMargins(margin, margin, margin, margin)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeProjects = ProjectsTree(parent=self, toolsTree=self.treeTools)
        self.verticalLayout_3.addWidget(self.treeProjects)
        self.tabWidget.addTab(self.tabProjects, "")

        # back to main window things
        self.verticalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.progressBar = QtWidgets.QProgressBar()
        self.statusbar.addPermanentWidget(self.progressBar)
        self.progressBar.hide()

        # toolbar
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")

        self.tabWidget.setCornerWidget(self.toolBar)
        # self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.actionSettings = QtGui.QAction(self)
        self.actionSettings.setIcon(icon_settings())
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.triggered.connect(self.settings_clicked)

        self.actionRefresh = QtGui.QAction(self)
        self.actionRefresh.setIcon(icon_refresh())
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRefresh.triggered.connect(self.refresh_clicked)

        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionRefresh)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)

        self.settings_panel = SettingsDialog(parent=self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AgsToolbox", "AGS ToolBox"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTools),
                                  _translate("AgsToolbox", "BlueCup Rack"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProjects),
                                  _translate("AgsToolbox", "Projects"))
        self.toolBar.setWindowTitle(_translate("AgsToolbox", "toolBar"))
        self.actionSettings.setText(_translate("AgsToolbox", "Settings"))
        self.actionSettings.setToolTip(_translate("AgsToolbox", "Configure AGS Toolbox"))
        self.actionRefresh.setText(_translate("AgsToolbox", "Refresh"))
        self.actionRefresh.setToolTip(_translate("AgsToolbox", "check for new things to add now"))

    def refresh_all(self):
        self.treeProjects.projects_schd_update()
        self.treeTools.tools_schd_update_downloads()
        self.treeTools.tools_schd_update_managed()
        self.treeTools.tools_schd_update_unmanaged()

    def refresh_clicked(self):
        self.refresh_all()

    def settings_clicked(self):
        self.settings_panel.show()
