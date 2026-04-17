# -*- coding: utf-8 -*-
from PySide2 import QtWidgets, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

class ABToolsWindow(MayaQWidgetDockableMixin, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ABToolsWindow, self).__init__(parent)
        self.setWindowTitle("AB Tools")
        self.setObjectName("ABToolsWorkspaceControl")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        label = QtWidgets.QLabel("AB Tools 插件面板 (从 UI 目录加载)")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        layout.addStretch()

# 提供一个统一的显示接口
def show_plugin_ui():
    workspace_control_name = "ABToolsWorkspaceControlWorkspaceControl"
    if QtWidgets.QWidget.findChild(QtWidgets.QWidget, workspace_control_name):
        import maya.cmds as cmds
        cmds.deleteUI(workspace_control_name)
    
    ui = ABToolsWindow()
    ui.show(dockable=True, area='left', floating=False)
    return ui