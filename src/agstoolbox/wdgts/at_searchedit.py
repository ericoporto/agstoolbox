from __future__ import annotations # for python 3.8
from typing import Callable, Dict, DefaultDict
from PyQt6 import QtWidgets, QtGui, QtCore


class ExpandableSearchBar(QtWidgets.QLineEdit):
    topWidget: QtWidgets.QWidget = None
    unfocused_width = None
    original_font = None
    focus_functions = dict()

    def __init__(self, parent: QtWidgets.QWidget = None,
                 top_widget: QtWidgets.QWidget = None):
        super(ExpandableSearchBar, self).__init__(parent)

        self.readyToEdit = None
        self.original_font = self.font()
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                                 QtWidgets.QSizePolicy.Policy.Fixed))

        self.setClearButtonEnabled(False)
        self.setPlaceholderText("🔍")
        self.setContentsMargins(1, 1, 1, 1)
        self.topWidget = top_widget
        self.unfocused_width = 26
        self.setMaximumWidth(self.unfocused_width)
        self.setMaximumHeight(self.height() - 8)
        self.setMinimumHeight(self.height() - 8)
        self.set_icon_font_if_needed(self.text())
        self.setToolTip("Ctrl+S to select. Type to filter projects or tools")

        shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(self.setFocus)

    def set_parent_focus_functions(self,
                                   f_focus_in: Callable[[QtWidgets.QWidget], None],
                                   f_focus_out: Callable[[QtWidgets.QWidget], None]):

        self.focus_functions['in'] = f_focus_in
        self.focus_functions['out'] = f_focus_out

    def set_icon_font_if_needed(self, txt: str):
        if txt is None or len(txt) == 0:
            fnt = QtGui.QFont("Beedii", 10)
            self.setFont(fnt)
        else:
            self.setFont(self.original_font)

    def tab_parent_changed(self):
        pass

    def mousePressEvent(self, e, Parent=None):
        super(ExpandableSearchBar, self).mousePressEvent(e)
        self.selectAll()

    def focusInEvent(self, event):
        # do custom stuff
        self.selectAll()
        self.setFont(self.original_font)
        self.setPlaceholderText("Search...")
        self.setMaximumWidth(90)
        self.focus_functions['in']()
        super(ExpandableSearchBar, self).focusInEvent(event)
        self.selectAll()

    def focusOutEvent(self, event):
        self.set_icon_font_if_needed(self.text())
        self.setPlaceholderText("🔍")
        self.setMaximumWidth(self.unfocused_width)
        self.focus_functions['out']()
        super(ExpandableSearchBar, self).focusOutEvent(event)
