from __future__ import annotations

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from core.notification_service import NotificationService
from database.repository import TopicRepository

CHECK_INTERVAL_MS = 60_000


class ReviewScheduler(QObject):
    """Periodically checks for due reviews, notifies the user, and advances stages.

    This class has no knowledge of any UI widget. It only depends on the
    repository and the notification service, which keeps the scheduling
    logic fully testable and reusable.
    """

    topics_updated = pyqtSignal()

    def __init__(self, repository: TopicRepository, notification_service: NotificationService) -> None:
        super().__init__()
        self._repository = repository
        self._notification_service = notification_service
        self._timer = QTimer(self)
        self._timer.setInterval(CHECK_INTERVAL_MS)
        self._timer.timeout.connect(self.check_due_reviews)

    def start(self) -> None:
        self.check_due_reviews()
        self._timer.start()

    def stop(self) -> None:
        self._timer.stop()

    def check_due_reviews(self) -> None:
        due_topics = self._repository.get_due_topics()
        if not due_topics:
            return

        topic_names = [topic.topic_name for topic in due_topics]
        for topic in due_topics:
            self._repository.advance_review_stage(topic)

        self._notification_service.notify_due_topics(topic_names)
        self.topics_updated.emit()
