from __future__ import annotations

from PyQt6.QtWidgets import QSystemTrayIcon

NOTIFICATION_DURATION_MS = 10_000


class NotificationService:
    """Delivers native desktop notifications through the system tray icon."""

    def __init__(self, tray_icon: QSystemTrayIcon) -> None:
        self._tray_icon = tray_icon

    def notify_due_topics(self, topic_names: list[str]) -> None:
        if not topic_names:
            return
        title = "Study Reminder"
        message = self._build_message(topic_names)
        self._tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            NOTIFICATION_DURATION_MS,
        )

    @staticmethod
    def _build_message(topic_names: list[str]) -> str:
        if len(topic_names) == 1:
            return f"Time to review: {topic_names[0]}"
        bullet_list = "\n".join(f"• {name}" for name in topic_names)
        return f"You have {len(topic_names)} topics to review today:\n{bullet_list}"

    def notify_background_mode(self) -> None:
        self._tray_icon.showMessage(
            "Study Reminder",
            "Still running in the background. Your reviews are being tracked.",
            QSystemTrayIcon.MessageIcon.Information,
            4000,
        )
