import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class AuthorEntity:
    """Pure Author entity with business rules and no external dependencies."""

    name: str
    birth_date: date
    death_date: Optional[date] = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_name()
        self._validate_birth_date()
        self._validate_death_date()

    def _validate_name(self):
        """Validate author name business rules."""
        if not self.name or not self.name.strip():
            raise ValueError("Author name cannot be empty")

        if len(self.name) > 100:
            raise ValueError("Author name cannot exceed 100 characters")

        if len(self.name.strip()) < 2:
            raise ValueError("Author name must be at least 2 characters long")

    def _validate_birth_date(self):
        """Validate birth date business rules."""
        if not self.birth_date:
            raise ValueError("Birth date cannot be empty")

        if self.birth_date > date.today():
            raise ValueError("Birth date cannot be in the future")

        # Authors cannot be born before 1000 AD
        if self.birth_date < date(1000, 1, 1):
            raise ValueError("Birth date cannot be before 1000 AD")

    def _validate_death_date(self):
        """Validate death date business rules."""
        if self.death_date:
            if self.death_date < self.birth_date:
                raise ValueError("Death date cannot be before birth date")

            if self.death_date > date.today():
                raise ValueError("Death date cannot be in the future")

    def is_alive(self) -> bool:
        """Check if the author is alive."""
        return self.death_date is None

    def get_age(self) -> Optional[int]:
        """Calculate the author's age or age at death."""
        if self.is_alive():
            today = date.today()
            return today.year - self.birth_date.year
        else:
            if self.death_date is not None:
                return self.death_date.year - self.birth_date.year
            return None

    def is_contemporary(self) -> bool:
        """Check if the author is contemporary (born in the last 100 years)."""
        today = date.today()
        return (today.year - self.birth_date.year) <= 100

    def is_classic_author(self) -> bool:
        """Check if the author is considered a classic author (born before 1900)."""
        return self.birth_date.year < 1900

    def update_name(self, new_name: str):
        """Update the author name with validation."""
        old_name = self.name
        self.name = new_name
        try:
            self._validate_name()
            self.updated_at = datetime.now()
        except ValueError:
            self.name = old_name
            raise

    def set_death_date(self, death_date: date):
        """Set the death date with validation."""
        old_death_date = self.death_date
        self.death_date = death_date
        try:
            self._validate_death_date()
            self.updated_at = datetime.now()
        except ValueError:
            self.death_date = old_death_date
            raise

    def get_full_name(self) -> str:
        """Get the full name of the author."""
        return self.name.strip()

    def get_initials(self) -> str:
        """Get the author's initials."""
        name_parts = self.name.strip().split()
        if len(name_parts) >= 2:
            return f"{name_parts[0][0]}.{name_parts[-1][0]}."
        return self.name[0] + "."

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "birth_date": self.birth_date.isoformat(),
            "death_date": self.death_date.isoformat() if self.death_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_alive": self.is_alive(),
            "age": self.get_age(),
        }
