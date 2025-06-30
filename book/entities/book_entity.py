import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


@dataclass
class BookEntity:
    """Pure Book entity with business rules and no external dependencies."""

    title: str
    description: str
    published_date: date
    isbn: str
    author_id: uuid.UUID
    publisher_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    genre_id: uuid.UUID | None = None

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_title()
        self._validate_isbn()
        self._validate_published_date()
        self._validate_description()

    def _validate_title(self):
        """Validate book title business rules."""
        if not self.title or not self.title.strip():
            raise ValueError("Book title cannot be empty")

        if len(self.title) > 100:
            raise ValueError("Book title cannot exceed 100 characters")

        if len(self.title.strip()) < 2:
            raise ValueError("Book title must be at least 2 characters long")

    def _validate_isbn(self):
        """Validate ISBN business rules."""
        if not self.isbn:
            raise ValueError("ISBN cannot be empty")

        # Ensure isbn is a string
        if not isinstance(self.isbn, str):
            raise ValueError("ISBN must be a string")

        if not self.isbn.strip():
            raise ValueError("ISBN cannot be empty")

        # Remove hyphens and spaces for validation
        clean_isbn = self.isbn

        if len(clean_isbn) not in [10, 13]:
            raise ValueError("ISBN must be either 10 or 13 digits")

        if not clean_isbn.isdigit():
            raise ValueError("ISBN must contain only digits")

    def _validate_published_date(self):
        """Validate published date business rules."""
        if not self.published_date:
            raise ValueError("Published date cannot be empty")

        if self.published_date > date.today():
            raise ValueError("Published date cannot be in the future")

        # Books cannot be published before 1450 (invention of printing press)
        if self.published_date < date(1450, 1, 1):
            raise ValueError("Published date cannot be before 1450")

    def _validate_description(self):
        """Validate description business rules."""
        if not self.description or not self.description.strip():
            raise ValueError("Book description cannot be empty")

        if len(self.description.strip()) < 10:
            raise ValueError("Book description must be at least 10 characters long")

    def add_genre(self, genre_id: uuid.UUID):
        """Add a genre to the book."""
        self.genre_id = genre_id

    def is_available_for_borrowing(self) -> bool:
        """Check if the book is available for borrowing."""
        # This is a business rule - in a real system, you'd check borrowing status
        # For now, we'll assume all books are available
        return True

    def get_age_in_years(self) -> int:
        """Calculate the age of the book in years."""
        today = date.today()
        return today.year - self.published_date.year

    def is_classic(self) -> bool:
        """Determine if the book is considered a classic (older than 50 years)."""
        return self.get_age_in_years() >= 50

    def update_title(self, new_title: str):
        """Update the book title with validation."""
        old_title = self.title
        self.title = new_title
        try:
            self._validate_title()
            self.updated_at = datetime.now()
        except ValueError:
            self.title = old_title
            raise

    def update_description(self, new_description: str):
        """Update the book description with validation."""
        old_description = self.description
        self.description = new_description
        try:
            self._validate_description()
            self.updated_at = datetime.now()
        except ValueError:
            self.description = old_description
            raise

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "published_date": self.published_date.isoformat(),
            "isbn": self.isbn,
            "author_id": str(self.author_id),
            "publisher_id": str(self.publisher_id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "genre_id": str(self.genre_id),
        }
