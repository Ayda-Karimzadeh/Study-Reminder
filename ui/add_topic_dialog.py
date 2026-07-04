from __future__ import annotations

from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import (
    QDialog,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

_FADE_IN_DURATION_MS = 220


class AddTopicDialog(QDialog):
    """Modal dialog for capturing a new topic name. Nothing else is asked of the user."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Add Topic")
        self.setModal(True)
        self.setFixedSize(420, 210)
        self._topic_name = ""
        self._fade_animation: QPropertyAnimation | None = None

        self._build_ui()
        self._animate_in()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 24)
        layout.setSpacing(16)

        title_label = QLabel("What did you learn?")
        title_label.setObjectName("dialogTitle")

        subtitle_label = QLabel("Enter a short, clear topic name.")
        subtitle_label.setObjectName("dialogSubtitle")

        self._name_input = QLineEdit()
        self._name_input.setObjectName("topicInput")
        self._name_input.setPlaceholderText("e.g. Binary Search")
        self._name_input.returnPressed.connect(self._handle_accept)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)
        button_row.addStretch(1)

        cancel_button = QPushButton("Cancel")
        cancel_button.setObjectName("secondaryButton")
        cancel_button.clicked.connect(self.reject)

        add_button = QPushButton("Add Topic")
        add_button.setObjectName("primaryButton")
        add_button.setDefault(True)
        add_button.clicked.connect(self._handle_accept)

        button_row.addWidget(cancel_button)
        button_row.addWidget(add_button)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(self._name_input)
        layout.addStretch(1)
        layout.addLayout(button_row)

        self._name_input.setFocus()

    def _handle_accept(self) -> None:
        name = self._name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Missing Topic", "Please enter a topic name.")
            return
        self._topic_name = name
        self.accept()

    def _animate_in(self) -> None:
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(_FADE_IN_DURATION_MS)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        self._fade_animation = animation

    @property
    def topic_name(self) -> str:
        return self._topic_name
