from __future__ import annotations  # for python 3.8
from typing import Callable, Dict, DefaultDict
from PyQt6 import QtWidgets, QtGui, QtCore


class ExpandableSearchBar(QtWidgets.QLineEdit):
    topWidget: QtWidgets.QWidget = None
    unfocused_width = None
    original_font = None
    focus_functions: Dict[str, Callable[[], None]] = DefaultDict[str, Callable[[], None]]()
    context: Dict[int, str] = DefaultDict[int, str]()
    previous_tab_id: int = None
    searchChanged: QtCore.pyqtSignal = QtCore.pyqtSignal(str)

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
        self.textChanged.connect(self.searchChangedEmit)

    def initContext(self, init_ctx_id: int, id_count: int):
        for i in range(id_count):
            self.context[i] = ""
        self.previous_tab_id = init_ctx_id

    def searchChangedEmit(self, text):
        if self.hasFocus() and self.font() != self.original_font:
            self.setFont(self.original_font)
        self.searchChanged.emit(text)

    def context_changed(self, new_context, previous_context):
        if previous_context is not None:
            self.context[previous_context] = self.text()
        if new_context in self.context:
            self.setText(self.context[new_context])
        else:
            self.setText("")
        self.clearFocus()

    def parent_tab_changed(self, index: int):
        self.context_changed(index, self.previous_tab_id)
        self.previous_tab_id = index
        self.set_icon_font_if_needed(self.text())

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
