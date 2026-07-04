from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon

from core.notification_service import NotificationService
from core.scheduler import ReviewScheduler
from database.database import Database
from database.repository import TopicRepository
from ui.icon_factory import create_app_icon
from ui.main_window import MainWindow
from ui.theme import DARK_STYLESHEET
from ui.tray_icon import TrayIcon

APP_DATA_DIR = Path.home() / ".study_reminder"
DATABASE_PATH = APP_DATA_DIR / "study_reminder.db"


def _set_windows_app_id() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("StudyReminder.DesktopApp")
    except (ImportError, AttributeError, OSError):
        pass


def main() -> None:
    _set_windows_app_id()

    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Study Reminder")
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(DARK_STYLESHEET)

    app_icon = create_app_icon()
    app.setWindowIcon(app_icon)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(
            None,
            "Study Reminder",
            "A system tray is required to run Study Reminder in the background, "
            "but none was found on this system.",
        )
        sys.exit(1)

    database = Database(DATABASE_PATH)
    repository = TopicRepository(database)

    tray_icon = TrayIcon(app_icon)
    notification_service = NotificationService(tray_icon)
    scheduler = ReviewScheduler(repository, notification_service)

    main_window = MainWindow(repository, tray_icon, notification_service)

    def handle_open() -> None:
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()

    def handle_exit() -> None:
        scheduler.stop()
        database.close()
        tray_icon.hide()
        app.quit()

    def handle_topics_updated() -> None:
        main_window.refresh_topics(main_window.current_search_text())

    tray_icon.open_requested.connect(handle_open)
    tray_icon.exit_requested.connect(handle_exit)
    scheduler.topics_updated.connect(handle_topics_updated)

    tray_icon.show()
    main_window.show()
    scheduler.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
