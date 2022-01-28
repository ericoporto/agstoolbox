from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize

from agstoolbox.core.settings import ConstSettings
from agstoolbox.at_icons import icon_exit, icon_refresh, icon_settings
from agstoolbox.wdgts.at_tree_item_project import TreeItemProject
from agstoolbox.at_tasks import do_update_projects, do_update_tools
from agstoolbox.wdgts.at_tree_item_tool import TreeItemTool


class MainWindow(QMainWindow):
    proj_update_task = None
    tool_update_task = None

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(ConstSettings.DEFAULT_MAIN_PANEL_WIDTH,
                                  ConstSettings.DEFAULT_MAIN_PANEL_HEIGHT))
        self.setWindowTitle("AGS Toolbox")
        self.setObjectName("AgsToolbox")
        self.resize(QSize(ConstSettings.DEFAULT_MAIN_PANEL_WIDTH,
                          ConstSettings.DEFAULT_MAIN_PANEL_HEIGHT))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        # Tools
        self.tabTools = QtWidgets.QWidget()
        self.tabTools.setObjectName("tabTools")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabTools)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeTools = QtWidgets.QTreeWidget(self.tabTools)
        self.treeTools.setHeaderHidden(True)
        self.treeTools.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.treeTools.setObjectName("treeTools")
        self.verticalLayout_2.addWidget(self.treeTools)
        self.tabWidget.addTab(self.tabTools, "")

        # Projects
        self.tabProjects = QtWidgets.QWidget()
        self.tabProjects.setObjectName("tabProjects")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabProjects)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.treeProjects = QtWidgets.QTreeWidget(self.tabProjects)
        self.treeProjects.setHeaderHidden(True)
        self.treeProjects.setObjectName("treeProjects")
        self.verticalLayout_3.addWidget(self.treeProjects)
        self.tabWidget.addTab(self.tabProjects, "")

        # back to main window things
        self.verticalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.actionSettings = QtGui.QAction(self)
        self.actionSettings.setIcon(icon_settings())
        self.actionSettings.setObjectName("actionSettings")

        self.actionRefresh = QtGui.QAction(self)
        self.actionRefresh.setIcon(icon_refresh())
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionRefresh.triggered.connect(self.refresh_clicked)

        self.actionQuit = QtGui.QAction(self)
        self.actionQuit.setIcon(icon_exit())
        self.actionQuit.setObjectName("actionQuit")

        self.toolBar.addAction(self.actionQuit)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)
        self.toolBar.addAction(self.actionRefresh)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("AgsToolbox", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabTools),
                                  _translate("AgsToolbox", "Tools"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabProjects),
                                  _translate("AgsToolbox", "Projects"))
        self.toolBar.setWindowTitle(_translate("AgsToolbox", "toolBar"))
        self.actionSettings.setText(_translate("AgsToolbox", "Settings"))
        self.actionSettings.setToolTip(_translate("AgsToolbox", "Configure AGS Toolbox"))
        self.actionRefresh.setText(_translate("AgsToolbox", "Refresh"))
        self.actionRefresh.setToolTip(_translate("AgsToolbox", "check for new things to add now"))
        self.actionQuit.setText(_translate("AgsToolbox", "Quit"))
        self.actionQuit.setToolTip(_translate("AgsToolbox", "Exit toolbox"))

    def refresh_all(self):
        self.projects_schd_update()
        self.tools_schd_update()

    def refresh_clicked(self):
        self.refresh_all()

    # AGS Projects stuff
    def projects_schd_update(self):
        if self.proj_update_task is not None:
            return

        self.proj_update_task = do_update_projects(self.projects_update, self.projects_update_ended)

    def projects_update(self):
        self.treeProjects.clear()
        projs = self.proj_update_task.proj_list

        for p in projs:
            itm = TreeItemProject(ags_game_project=p)
            self.treeProjects.addTopLevelItem(itm)
            itm.updateInTree()

        self.projects_update_ended()

    def projects_update_ended(self):
        self.proj_update_task = None

    # Tool stuff
    def tools_schd_update(self):
        if self.tool_update_task is not None:
            return

        self.tool_update_task = do_update_tools(self.tools_update, self.tools_update_ended)

    def tools_update(self):
        self.treeTools.clear()
        tools = self.tool_update_task.tools_list
        items = []
        for t in tools:
            itm = TreeItemTool(t)
            items.append(itm)

        self.treeTools.addTopLevelItems(items)
        self.tools_update_ended()

    def tools_update_ended(self):
        self.tool_update_task = None
