from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon


class TrayIcon(QSystemTrayIcon):
    """System tray presence. Keeps the app alive and reachable when the window is hidden."""

    open_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, icon: QIcon, parent: QObject | None = None) -> None:
        super().__init__(icon, parent)
        self.setToolTip("Study Reminder")
        self._build_menu()
        self.activated.connect(self._handle_activation)

    def _build_menu(self) -> None:
        menu = QMenu()

        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.open_requested.emit)

        menu.addSeparator()

        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_requested.emit)

        self.setContextMenu(menu)

    def _handle_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.open_requested.emit()
