# -*- coding: utf-8 -*-
"""上方面板 — 二级树形列表（文件夹 → 脚本）"""
from PySide2 import QtWidgets, QtCore
from .. import config


class TreeView(QtWidgets.QTreeWidget):
    """树形列表：文件夹→脚本，右键菜单"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(1)
        self.setAnimated(1)
        self.setIndentation(0)
        self.setRootIsDecorated(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_menu)
        self.setStyleSheet(
            f"QTreeView::item {{"
            f"  background-color: {config.Top_Panel.Folder_Bg_Color};"
            f"  color: {config.Top_Panel.Folder_Selected_Text_Color};"
            f"  padding-left: {int(config.Top_Panel.Folder_Padding)}px;"
            f"  margin-bottom: {int(config.Top_Panel.Folder_Spacing)}px;"
            f"}}"
            f"QScrollBar:vertical {{"
            f"  background: {config.Top_Panel.Scroll_Bg_Color};"
            f"  width: {int(config.Top_Panel.Scroll_Width)}px;"
            f"}}"
            f"QScrollBar::handle:vertical {{"
            f"  background: {config.Top_Panel.Scroll_Handle_Color};"
            f"  min-height: {int(config.Top_Panel.Scroll_Handle_Min_Height)}px;"
            f"}}"
            f"QTreeView::item:selected {{"
            f"  background-color: {config.Top_Panel.Folder_Selected_Bg_Color};"
            f"  color: {config.Top_Panel.Folder_Selected_Text_Color};"
            f"}}"
            f"QTreeView::item:selected:!active {{"
            f"  background-color: {config.Top_Panel.Folder_Selected_Bg_Color};"
            f"  color: {config.Top_Panel.Folder_Selected_Text_Color};"
            f"}}"
            f"QTreeView {{ outline: none; }}"
            f"QTreeView::item:focus {{ outline: none; border: none; }}")
        # 防止跳
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Ignored)
        self.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item, col):
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())

    def _on_menu(self, pos):
        item = self.itemAt(pos)
        parent = item.parent() if item else None
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet(
            f"QMenu {{"
            f"  background-color: {config.Context_Menu.Bg_Color};"
            f"  color: {config.Context_Menu.Text_Color};"
            f"}}"
            f"QMenu::item:selected {{"
            f"  background-color: {config.Context_Menu.Hover_Bg_Color};"
            f"}}")

        if item is None:
            # 空白区域
            menu.addAction("新建文件夹", self._add_folder)
        elif parent is None:
            # 文件夹
            menu.addAction("重命名", lambda: self.editItem(item, 0))
            menu.addAction("删除", lambda: self._remove_item(item))
            menu.addSeparator()
            menu.addAction("新建脚本", lambda: self._add_child(item))
        else:
            # 脚本
            menu.addAction("重命名", lambda: self.editItem(item, 0))
            menu.addAction("删除", lambda: self._remove_item(item))
            menu.addSeparator()
            menu.addAction("转本地", lambda: None)
            menu.addAction("上传", lambda: None)
        menu.exec_(self.viewport().mapToGlobal(pos))

    def _add_folder(self):
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, "新文件夹")
        item.setFlags(
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsSelectable |
            QtCore.Qt.ItemIsEditable |
            QtCore.Qt.ItemIsDragEnabled)
        self._style_folder(item)
        self.addTopLevelItem(item)

    def _style_folder(self, item):
        h = int(config.Top_Panel.Folder_Height)
        s = int(config.Top_Panel.Folder_Spacing)
        item.setSizeHint(0, QtCore.QSize(0, h + s))
        font = item.font(0)
        font.setBold(True)
        font.setPixelSize(int(config.Top_Panel.Folder_Font_Size))
        item.setFont(0, font)

    def _add_child(self, parent):
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, "    " + "新脚本")
        item.setFlags(
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsSelectable |
            QtCore.Qt.ItemIsEditable)
        h = int(config.Top_Panel.Script_Height)
        item.setSizeHint(0, QtCore.QSize(0, h))
        font = item.font(0)
        font.setPixelSize(int(config.Top_Panel.Script_Font_Size))
        item.setFont(0, font)
        parent.addChild(item)
        parent.setExpanded(True)

    def _remove_item(self, item):
        parent = item.parent()
        if parent:
            parent.removeChild(item)
        else:
            idx = self.indexOfTopLevelItem(item)
            if idx >= 0:
                self.takeTopLevelItem(idx)


class Top_Panel(QtWidgets.QWidget):
    """上方面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setMinimumSize(0, 0)
        self.setStyleSheet(
            f"background-color: {config.Top_Panel.Bg_Color};")

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tree = TreeView()
        self.tree.setMinimumSize(0, 0)
        layout.addWidget(self.tree)
