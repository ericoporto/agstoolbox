from __future__ import annotations  # for python 3.8

from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import QMenu


def DefaultMenuQAction(menu: QMenu, action_text: str) -> QAction:
    action = menu.addAction(action_text)
    font: QFont = action.font()
    font.setBold(True)
    action.setFont(font)
    menu.addSeparator()
    return action
