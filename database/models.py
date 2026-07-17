from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

# Spaced repetition schedule. The first review is always this many days
# after the learning date. Every review after that is this many days after
# the *previous review was actually confirmed* -- not after the original
# learning date -- so reviewing late never compresses the following
# reviews into an immediate backlog.
REVIEW_INTERVALS_DAYS: tuple[int, ...] = (1, 3, 7, 21, 30, 60, 120, 240, 365)


@dataclass(slots=True)
class Topic:
    """Represents a single learned topic and its spaced repetition state."""

    id: int
    topic_name: str
    learning_date: date
    current_review_stage: int
    next_review_date: Optional[date]
    last_notified_date: Optional[date] = None

    @property
    def is_completed(self) -> bool:
        return self.next_review_date is None

    @property
    def is_overdue(self) -> bool:
        if self.next_review_date is None:
            return False
        return self.next_review_date < date.today()

    @property
    def is_due(self) -> bool:
        if self.next_review_date is None:
            return False
        return self.next_review_date <= date.today()

    @staticmethod
    def compute_next_review_date(base_date: date, stage: int) -> Optional[date]:
        """Returns the review date for a given stage, or None once all stages are complete.

        `base_date` is the learning date when computing the very first
        review, and the date of the just-confirmed review for every stage
        after that.
        """
        if stage < 0 or stage >= len(REVIEW_INTERVALS_DAYS):
            return None
        return base_date + timedelta(days=REVIEW_INTERVALS_DAYS[stage])
