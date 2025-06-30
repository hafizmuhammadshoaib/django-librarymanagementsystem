import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List


@dataclass
class MemberEntity:
    """Pure Member entity with business rules and no external dependencies."""

    first_name: str
    last_name: str
    birth_date: date
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    borrowing_ids: List[uuid.UUID] = field(default_factory=list)

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_names()
        self._validate_birth_date()

    def _validate_names(self):
        """Validate member name business rules."""
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")

        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")

        if len(self.first_name) > 100:
            raise ValueError("First name cannot exceed 100 characters")

        if len(self.last_name) > 100:
            raise ValueError("Last name cannot exceed 100 characters")

        if len(self.first_name.strip()) < 2:
            raise ValueError("First name must be at least 2 characters long")

        if len(self.last_name.strip()) < 2:
            raise ValueError("Last name must be at least 2 characters long")

    def _validate_birth_date(self):
        """Validate birth date business rules."""
        if not self.birth_date:
            raise ValueError("Birth date cannot be empty")

        if self.birth_date > date.today():
            raise ValueError("Birth date cannot be in the future")

        # Members must be at least 5 years old
        today = date.today()
        age = (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

        if age < 5:
            raise ValueError("Member must be at least 5 years old")

        # Members cannot be born before 1900
        if self.birth_date < date(1900, 1, 1):
            raise ValueError("Birth date cannot be before 1900")

    def get_age(self) -> int:
        """Calculate the member's current age."""
        today = date.today()
        age = (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age

    def is_minor(self) -> bool:
        """Check if the member is a minor (under 18)."""
        return self.get_age() < 18

    def is_senior(self) -> bool:
        """Check if the member is a senior (65 or older)."""
        return self.get_age() >= 65

    def is_adult(self) -> bool:
        """Check if the member is an adult (18 or older)."""
        return self.get_age() >= 18

    def get_full_name(self) -> str:
        """Get the member's full name."""
        return f"{self.first_name.strip()} {self.last_name.strip()}"

    def get_initials(self) -> str:
        """Get the member's initials."""
        return f"{self.first_name[0]}.{self.last_name[0]}."

    def get_borrowing_count(self) -> int:
        """Get the number of current borrowings."""
        return len(self.borrowing_ids)

    def can_borrow_more_books(self, max_books: int = 5) -> bool:
        """Check if the member can borrow more books."""
        return self.get_borrowing_count() < max_books

    def is_active_borrower(self) -> bool:
        """Check if the member is an active borrower (has borrowed books)."""
        return self.get_borrowing_count() > 0

    def is_heavy_borrower(self) -> bool:
        """Check if the member is a heavy borrower (has borrowed more than 10 books)."""
        return self.get_borrowing_count() > 10

    def add_borrowing(self, borrowing_id: uuid.UUID):
        """Add a borrowing to this member."""
        if borrowing_id not in self.borrowing_ids:
            self.borrowing_ids.append(borrowing_id)

    def remove_borrowing(self, borrowing_id: uuid.UUID):
        """Remove a borrowing from this member."""
        if borrowing_id in self.borrowing_ids:
            self.borrowing_ids.remove(borrowing_id)

    def update_first_name(self, new_first_name: str):
        """Update the first name with validation."""
        old_first_name = self.first_name
        self.first_name = new_first_name
        try:
            self._validate_names()
            self.updated_at = datetime.now()
        except ValueError:
            self.first_name = old_first_name
            raise

    def update_last_name(self, new_last_name: str):
        """Update the last name with validation."""
        old_last_name = self.last_name
        self.last_name = new_last_name
        try:
            self._validate_names()
            self.updated_at = datetime.now()
        except ValueError:
            self.last_name = old_last_name
            raise

    def get_membership_duration_days(self) -> int:
        """Calculate how many days the member has been registered."""
        today = datetime.now().date()
        return (today - self.created_at.date()).days

    def is_long_term_member(self) -> bool:
        """Check if the member has been registered for more than 1 year."""
        return self.get_membership_duration_days() > 365

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.get_full_name(),
            "birth_date": self.birth_date.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "age": self.get_age(),
            "is_minor": self.is_minor(),
            "is_senior": self.is_senior(),
            "is_adult": self.is_adult(),
            "borrowing_ids": [str(borrowing_id) for borrowing_id in self.borrowing_ids],
            "borrowing_count": self.get_borrowing_count(),
            "can_borrow_more": self.can_borrow_more_books(),
            "is_active_borrower": self.is_active_borrower(),
            "is_heavy_borrower": self.is_heavy_borrower(),
            "membership_duration_days": self.get_membership_duration_days(),
            "is_long_term_member": self.is_long_term_member(),
        }
