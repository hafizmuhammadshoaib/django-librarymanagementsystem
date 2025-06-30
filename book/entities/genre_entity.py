import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class GenreEntity:
    """Pure Genre entity with business rules and no external dependencies."""

    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    book_ids: List[uuid.UUID] = field(default_factory=list)

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_name()

    def _validate_name(self):
        """Validate genre name business rules."""
        if not self.name or not self.name.strip():
            raise ValueError("Genre name cannot be empty")

        if len(self.name) > 100:
            raise ValueError("Genre name cannot exceed 100 characters")

        if len(self.name.strip()) < 2:
            raise ValueError("Genre name must be at least 2 characters long")

        # Check for common genre names to ensure consistency
        common_genres = [
            "fiction",
            "non-fiction",
            "mystery",
            "romance",
            "science fiction",
            "fantasy",
            "thriller",
            "horror",
            "biography",
            "autobiography",
            "history",
            "philosophy",
            "science",
            "technology",
            "cooking",
            "travel",
            "self-help",
            "business",
            "economics",
            "politics",
            "religion",
            "poetry",
            "drama",
            "comedy",
            "adventure",
            "western",
            "young adult",
            "children",
            "reference",
            "academic",
            "textbook",
        ]

        # Suggest common genres if the name is close
        if self.name.lower() not in [genre.lower() for genre in common_genres]:
            # This is just a warning, not an error - allowing custom genres
            pass

    def add_book(self, book_id: uuid.UUID):
        """Add a book to this genre."""
        if book_id not in self.book_ids:
            self.book_ids.append(book_id)

    def remove_book(self, book_id: uuid.UUID):
        """Remove a book from this genre."""
        if book_id in self.book_ids:
            self.book_ids.remove(book_id)

    def get_book_count(self) -> int:
        """Get the number of books in this genre."""
        return len(self.book_ids)

    def is_popular(self) -> bool:
        """Check if this genre is popular (has more than 10 books)."""
        return self.get_book_count() > 10

    def is_niche(self) -> bool:
        """Check if this genre is niche (has less than 5 books)."""
        return self.get_book_count() < 5

    def is_fiction(self) -> bool:
        """Check if this is a fiction genre."""
        fiction_genres = [
            "fiction",
            "mystery",
            "romance",
            "science fiction",
            "fantasy",
            "thriller",
            "horror",
            "adventure",
            "western",
            "young adult",
            "children",
            "drama",
            "comedy",
        ]
        return self.name.lower() in fiction_genres

    def is_non_fiction(self) -> bool:
        """Check if this is a non-fiction genre."""
        non_fiction_genres = [
            "non-fiction",
            "biography",
            "autobiography",
            "history",
            "philosophy",
            "science",
            "technology",
            "cooking",
            "travel",
            "self-help",
            "business",
            "economics",
            "politics",
            "religion",
            "reference",
            "academic",
            "textbook",
        ]
        return self.name.lower() in non_fiction_genres

    def update_name(self, new_name: str):
        """Update the genre name with validation."""
        old_name = self.name
        self.name = new_name
        try:
            self._validate_name()
            self.updated_at = datetime.now()
        except ValueError:
            self.name = old_name
            raise

    def get_display_name(self) -> str:
        """Get a formatted display name for the genre."""
        return self.name.strip().title()

    def get_category(self) -> str:
        """Get the category of the genre (fiction/non-fiction/other)."""
        if self.is_fiction():
            return "fiction"
        elif self.is_non_fiction():
            return "non-fiction"
        else:
            return "other"

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "book_ids": [str(book_id) for book_id in self.book_ids],
            "book_count": self.get_book_count(),
            "is_popular": self.is_popular(),
            "is_niche": self.is_niche(),
            "is_fiction": self.is_fiction(),
            "is_non_fiction": self.is_non_fiction(),
            "category": self.get_category(),
        }
