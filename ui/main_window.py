from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from core.notification_service import NotificationService
from database.repository import TopicRepository
from ui.add_topic_dialog import AddTopicDialog
from ui.topic_card import TopicCard
from ui.tray_icon import TrayIcon


class MainWindow(QMainWindow):
    """The single window of Study Reminder: title, add button, search box, and topic list."""

    def __init__(
        self,
        repository: TopicRepository,
        tray_icon: TrayIcon,
        notification_service: NotificationService,
    ) -> None:
        super().__init__()
        self._repository = repository
        self._tray_icon = tray_icon
        self._notification_service = notification_service
        self._has_shown_background_notice = False

        self.setWindowTitle("Study Reminder")
        self.setMinimumSize(560, 640)
        self.resize(600, 720)

        self._build_ui()
        self.refresh_topics()

    def _build_ui(self) -> None:
        container = QWidget()
        container.setObjectName("mainContainer")
        self.setCentralWidget(container)

        root_layout = QVBoxLayout(container)
        root_layout.setContentsMargins(28, 28, 28, 28)
        root_layout.setSpacing(20)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        title_label = QLabel("Study Reminder")
        title_label.setObjectName("headerTitle")

        subtitle_label = QLabel("Remember what you learn, on schedule.")
        subtitle_label.setObjectName("headerSubtitle")

        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)

        self._search_input = QLineEdit()
        self._search_input.setObjectName("searchInput")
        self._search_input.setPlaceholderText("Search topics...")
        self._search_input.textChanged.connect(self._on_search_changed)

        add_button = QPushButton("+  Add Topic")
        add_button.setObjectName("primaryButton")
        add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_button.clicked.connect(self._open_add_topic_dialog)

        controls_layout.addWidget(self._search_input, 1)
        controls_layout.addWidget(add_button, 0)

        self._list_container = QWidget()
        self._list_layout = QVBoxLayout(self._list_container)
        self._list_layout.setContentsMargins(0, 0, 4, 0)
        self._list_layout.setSpacing(12)
        self._list_layout.addStretch(1)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self._list_container)

        root_layout.addLayout(header_layout)
        root_layout.addLayout(controls_layout)
        root_layout.addWidget(scroll_area, 1)

    def _open_add_topic_dialog(self) -> None:
        dialog = AddTopicDialog(self)
        if dialog.exec() == AddTopicDialog.DialogCode.Accepted:
            self._repository.add_topic(dialog.topic_name)
            self.refresh_topics(self.current_search_text())

    def _on_search_changed(self, text: str) -> None:
        self.refresh_topics(search_query=text)

    def current_search_text(self) -> str:
        return self._search_input.text()

    def refresh_topics(self, search_query: str = "") -> None:
        while self._list_layout.count() > 1:
            item = self._list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        topics = (
            self._repository.search_topics(search_query)
            if search_query
            else self._repository.get_all_topics()
        )

        if not topics:
            empty_label = QLabel(
                'No topics yet. Click "Add Topic" to start learning with spaced repetition.'
            )
            empty_label.setObjectName("emptyStateLabel")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setWordWrap(True)
            self._list_layout.insertWidget(0, empty_label)
            return

        for topic in topics:
            card = TopicCard(topic, self._list_container)
            card.delete_requested.connect(self._handle_delete_topic)
            self._list_layout.insertWidget(self._list_layout.count() - 1, card)

    def _handle_delete_topic(self, topic_id: int) -> None:
        confirmation = QMessageBox.question(
            self,
            "Delete Topic",
            "Are you sure you want to delete this topic?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirmation == QMessageBox.StandardButton.Yes:
            self._repository.delete_topic(topic_id)
            self.refresh_topics(self.current_search_text())

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.hide()
        if not self._has_shown_background_notice:
            self._notification_service.notify_background_mode()
            self._has_shown_background_notice = True
