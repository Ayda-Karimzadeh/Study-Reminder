from __future__ import annotations

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

from core.notification_service import NotificationService
from database.repository import TopicRepository

CHECK_INTERVAL_MS = 60_000


class ReviewScheduler(QObject):
    """Periodically checks for due reviews and notifies the user.

    This class never advances a review stage itself -- that only happens
    when the user explicitly confirms a review in the UI. This guarantees a
    review can never be silently skipped: an unreviewed topic keeps
    triggering a fresh notification every day until it is actually marked
    as reviewed.

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
        pending_topics = self._repository.get_topics_pending_notification()
        if not pending_topics:
            return

        topic_names = [topic.topic_name for topic in pending_topics]
        for topic in pending_topics:
            self._repository.mark_notified(topic.id)

        self._notification_service.notify_due_topics(topic_names)
        self.topics_updated.emit()
