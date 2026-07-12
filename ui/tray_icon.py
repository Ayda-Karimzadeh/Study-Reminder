from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon


class TrayIcon(QSystemTrayIcon):
    """System tray presence. Keeps the app alive and reachable when the window is hidden."""

    open_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    startup_toggled = pyqtSignal(bool)

    def __init__(
        self,
        icon: QIcon,
        parent: QObject | None = None,
        show_startup_option: bool = True,
    ) -> None:
        super().__init__(icon, parent)
        self.setToolTip("Study Reminder")
        self._startup_action = None
        self._build_menu(show_startup_option)
        self.activated.connect(self._handle_activation)

    def _build_menu(self, show_startup_option: bool) -> None:
        menu = QMenu()

        open_action = menu.addAction("Open")
        open_action.triggered.connect(self.open_requested.emit)

        if show_startup_option:
            menu.addSeparator()
            self._startup_action = menu.addAction("Start with Windows")
            self._startup_action.setCheckable(True)
            self._startup_action.toggled.connect(self.startup_toggled.emit)

        menu.addSeparator()

        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_requested.emit)

        self.setContextMenu(menu)

    def set_startup_checked(self, checked: bool) -> None:
        if self._startup_action is None:
            return
        self._startup_action.blockSignals(True)
        self._startup_action.setChecked(checked)
        self._startup_action.blockSignals(False)

    def _handle_activation(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.open_requested.emit()
