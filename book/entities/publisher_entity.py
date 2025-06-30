import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse


@dataclass
class PublisherEntity:
    """Pure Publisher entity with business rules and no external dependencies."""

    name: str
    website: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_name()
        self._validate_website()

    def _validate_name(self):
        """Validate publisher name business rules."""
        if not self.name or not self.name.strip():
            raise ValueError("Publisher name cannot be empty")

        if len(self.name) > 100:
            raise ValueError("Publisher name cannot exceed 100 characters")

        if len(self.name.strip()) < 2:
            raise ValueError("Publisher name must be at least 2 characters long")

    def _validate_website(self):
        """Validate website URL business rules."""
        if not self.website or not self.website.strip():
            raise ValueError("Website URL cannot be empty")

        try:
            parsed_url = urlparse(self.website)
            if not parsed_url.scheme or not parsed_url.netloc:
                raise ValueError("Invalid website URL format")

            if parsed_url.scheme not in ["http", "https"]:
                raise ValueError("Website URL must use HTTP or HTTPS protocol")
        except Exception:
            raise ValueError("Invalid website URL format")

    def is_major_publisher(self) -> bool:
        """Check if this is a major publisher based on name patterns."""
        major_publishers = [
            "penguin",
            "random house",
            "harper collins",
            "simon & schuster",
            "macmillan",
            "hachette",
            "scholastic",
            "disney",
            "wiley",
            "springer",
            "elsevier",
            "oxford university press",
            "cambridge university press",
        ]

        return any(publisher in self.name.lower() for publisher in major_publishers)

    def is_university_press(self) -> bool:
        """Check if this is a university press."""
        return (
            "university press" in self.name.lower()
            or "university of" in self.name.lower()
        )

    def is_independent_publisher(self) -> bool:
        """Check if this is an independent publisher."""
        return not self.is_major_publisher() and not self.is_university_press()

    def get_domain(self) -> str:
        """Extract the domain from the website URL."""
        try:
            parsed_url = urlparse(self.website)
            return parsed_url.netloc
        except Exception:
            return ""

    def update_name(self, new_name: str):
        """Update the publisher name with validation."""
        old_name = self.name
        self.name = new_name
        try:
            self._validate_name()
            self.updated_at = datetime.now()
        except ValueError:
            self.name = old_name
            raise

    def update_website(self, new_website: str):
        """Update the website URL with validation."""
        old_website = self.website
        self.website = new_website
        try:
            self._validate_website()
            self.updated_at = datetime.now()
        except ValueError:
            self.website = old_website
            raise

    def get_display_name(self) -> str:
        """Get a formatted display name for the publisher."""
        return self.name.strip()

    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "website": self.website,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "domain": self.get_domain(),
            "is_major_publisher": self.is_major_publisher(),
            "is_university_press": self.is_university_press(),
            "is_independent_publisher": self.is_independent_publisher(),
        }
