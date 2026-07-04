from __future__ import annotations

from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMenu,
    QVBoxLayout,
    QWidget,
)

from database.models import Topic

_ENTRY_ANIMATION_DURATION_MS = 320
_SHADOW_BLUR_RADIUS = 24


class TopicCard(QFrame):
    """A single card showing a topic's name, learning date, and next review date."""

    delete_requested = pyqtSignal(int)

    def __init__(self, topic: Topic, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._topic = topic
        self._entry_animation: QPropertyAnimation | None = None

        self.setObjectName("topicCard")
        self.setProperty("status", self._status_key())
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self._build_ui()
        self._apply_entry_effect()

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)

        name_label = QLabel(self._topic.topic_name)
        name_label.setObjectName("topicName")
        name_label.setWordWrap(True)

        meta_label = QLabel(self._meta_text())
        meta_label.setObjectName("topicMeta")

        text_layout.addWidget(name_label)
        text_layout.addWidget(meta_label)

        status_label = QLabel(self._status_text())
        status_label.setObjectName("statusBadge")
        status_label.setProperty("status", self._status_key())
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(text_layout, 1)
        layout.addWidget(status_label, 0, Qt.AlignmentFlag.AlignVCenter)

    def _meta_text(self) -> str:
        learned = self._topic.learning_date.strftime("%b %d, %Y")
        if self._topic.next_review_date is None:
            return f"Learned {learned}"
        next_review = self._topic.next_review_date.strftime("%b %d, %Y")
        return f"Learned {learned}  •  Next review {next_review}"

    def _status_text(self) -> str:
        if self._topic.is_completed:
            return "Completed"
        if self._topic.is_overdue:
            return "Overdue"
        if self._topic.is_due:
            return "Due today"
        days_remaining = (self._topic.next_review_date - self._topic.next_review_date.today()).days
        return f"In {days_remaining} day{'s' if days_remaining != 1 else ''}"

    def _status_key(self) -> str:
        if self._topic.is_completed:
            return "completed"
        if self._topic.is_overdue:
            return "overdue"
        if self._topic.is_due:
            return "due"
        return "scheduled"

    def _apply_entry_effect(self) -> None:
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(0, 0, 0, 140))
        shadow.setOffset(0, 4)
        shadow.setBlurRadius(0)
        self.setGraphicsEffect(shadow)

        animation = QPropertyAnimation(shadow, b"blurRadius", self)
        animation.setDuration(_ENTRY_ANIMATION_DURATION_MS)
        animation.setStartValue(0)
        animation.setEndValue(_SHADOW_BLUR_RADIUS)
        animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        self._entry_animation = animation

    def _show_context_menu(self, position) -> None:
        menu = QMenu(self)
        delete_action = menu.addAction("Delete Topic")
        chosen_action = menu.exec(self.mapToGlobal(position))
        if chosen_action == delete_action:
            self.delete_requested.emit(self._topic.id)

    @property
    def topic(self) -> Topic:
        return self._topic
