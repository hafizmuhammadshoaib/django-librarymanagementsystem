import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


@dataclass
class BorrowingEntity:
    """Pure Borrowing entity with business rules and no external dependencies."""

    book_id: uuid.UUID
    member_id: uuid.UUID
    borrowing_date: date
    returning_date: Optional[date] = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_dates()

    def _validate_dates(self):
        """Validate borrowing and returning date business rules."""
        if not self.borrowing_date:
            raise ValueError("Borrowing date cannot be empty")

        if self.borrowing_date > date.today():
            raise ValueError("Borrowing date cannot be in the future")

        if self.returning_date:
            if self.returning_date < self.borrowing_date:
                raise ValueError("Returning date cannot be before borrowing date")

            if self.returning_date > date.today():
                raise ValueError("Returning date cannot be in the future")

    def is_returned(self) -> bool:
        """Check if the book has been returned."""
        return self.returning_date is not None

    def is_overdue(self) -> bool:
        """Check if the book is overdue."""
        if self.is_returned():
            return False

        max_borrowing_days = self._get_max_borrowing_days()
        due_date = self.borrowing_date + timedelta(days=max_borrowing_days)
        return date.today() > due_date

    def get_due_date(self) -> date:
        """Get the due date for returning the book."""
        max_borrowing_days = self._get_max_borrowing_days()
        return self.borrowing_date + timedelta(days=max_borrowing_days)

    def get_days_overdue(self) -> int:
        """Get the number of days the book is overdue."""
        if not self.is_overdue():
            return 0

        due_date = self.get_due_date()
        return (date.today() - due_date).days

    def get_borrowing_duration_days(self) -> int:
        """Get the total duration of the borrowing in days."""
        if self.returning_date is not None:
            end_date = self.returning_date
        else:
            end_date = date.today()
        return (end_date - self.borrowing_date).days

    def _get_max_borrowing_days(self) -> int:
        """Get the maximum number of days a book can be borrowed."""
        # Default borrowing period is 14 days
        return 14

    def return_book(self, return_date: Optional[date] = None):
        """Mark the book as returned."""
        if self.is_returned():
            raise ValueError("Book is already returned")

        if return_date is None:
            return_date = date.today()

        old_returning_date = self.returning_date
        self.returning_date = return_date

        try:
            self._validate_dates()
            self.updated_at = datetime.now()
        except ValueError:
            self.returning_date = old_returning_date
            raise

    def get_status(self) -> str:
        """Get the current status of the borrowing."""
        if self.is_returned():
            return "returned"
        elif self.is_overdue():
            return "overdue"
        else:
            return "borrowed"

    def get_fine_amount(self, daily_fine_rate: float = 1.0) -> float:
        """Calculate the fine amount for overdue books."""
        if not self.is_overdue():
            return 0.0

        days_overdue = self.get_days_overdue()
        return days_overdue * daily_fine_rate

    def is_long_term_borrowing(self) -> bool:
        """Check if this is a long-term borrowing (more than 30 days)."""
        return self.get_borrowing_duration_days() > 30

    def is_short_term_borrowing(self) -> bool:
        """Check if this is a short-term borrowing (7 days or less)."""
        return self.get_borrowing_duration_days() <= 7

    def can_be_renewed(self) -> bool:
        """Check if the borrowing can be renewed."""
        if self.is_returned():
            return False

        # Can only renew if not overdue and within first week
        if self.is_overdue():
            return False

        days_borrowed = self.get_borrowing_duration_days()
        return days_borrowed <= 7

    def renew_borrowing(self, renewal_days: int = 7):
        """Renew the borrowing for additional days."""
        if not self.can_be_renewed():
            raise ValueError("Borrowing cannot be renewed")

        # Extend the borrowing date by renewal_days
        self.borrowing_date = self.borrowing_date - timedelta(days=renewal_days)
        self.updated_at = datetime.now()

    def get_remaining_days(self) -> int:
        """Get the remaining days before the book is due."""
        if self.is_returned():
            return 0

        due_date = self.get_due_date()
        remaining = (due_date - date.today()).days
        return max(0, remaining)

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": str(self.id),
            "book_id": str(self.book_id),
            "member_id": str(self.member_id),
            "borrowing_date": self.borrowing_date.isoformat(),
            "returning_date": self.returning_date.isoformat()
            if self.returning_date
            else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_returned": self.is_returned(),
            "is_overdue": self.is_overdue(),
            "status": self.get_status(),
            "due_date": self.get_due_date().isoformat(),
            "days_overdue": self.get_days_overdue(),
            "borrowing_duration_days": self.get_borrowing_duration_days(),
            "remaining_days": self.get_remaining_days(),
            "fine_amount": self.get_fine_amount(),
            "can_be_renewed": self.can_be_renewed(),
            "is_long_term_borrowing": self.is_long_term_borrowing(),
            "is_short_term_borrowing": self.is_short_term_borrowing(),
        }
