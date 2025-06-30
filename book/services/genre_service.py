import uuid
from typing import Any, Dict, Optional

from django.forms import ValidationError

from book.entities.genre_entity import GenreEntity
from book.repositories.genre_repository import GenreAbstractRepository


class GenreService:
    def __init__(self, genre_repository: GenreAbstractRepository):
        self.genre_repository = genre_repository

    def get_genre(self, genre_id):
        """Legacy method for Django model data."""
        return self.genre_repository.get_genre_by_id(genre_id)

    def add_genre_to_book(self, book, genre_id):
        """Legacy method for Django model data."""
        return self.genre_repository.add_genre_to_book(book, genre_id)

    def get_genre_entity(self, genre_id: str) -> Optional[GenreEntity]:
        """
        Get a genre entity by ID.

        Args:
            genre_id: The genre ID as string

        Returns:
            GenreEntity or None if not found
        """
        try:
            genre_uuid = uuid.UUID(genre_id)
            return self.genre_repository.get_genre_entity_by_id(genre_uuid)
        except ValueError:
            raise ValidationError(f"Invalid genre ID format: {genre_id}")

    def save_genre(self, genre_entity: GenreEntity) -> GenreEntity:
        """
        Save a genre entity.

        Args:
            genre_entity: The genre entity to save

        Returns:
            The saved genre entity
        """
        try:
            return self.genre_repository.save_genre(genre_entity)
        except Exception as e:
            raise ValidationError(str(e))

    def get_genre_stats(self, genre_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for a genre.

        Args:
            genre_id: The genre ID as string

        Returns:
            Dictionary with genre statistics
        """
        try:
            genre = self.get_genre_entity(genre_id)
            if not genre:
                raise ValidationError(f"Genre with ID {genre_id} not found")

            return {
                "id": str(genre.id),
                "name": genre.name,
                "book_count": genre.get_book_count(),
                "is_popular": genre.is_popular(),
                "is_niche": genre.is_niche(),
                "is_fiction": genre.is_fiction(),
                "is_non_fiction": genre.is_non_fiction(),
                "category": genre.get_category(),
                "display_name": genre.get_display_name(),
                "book_ids": [str(book_id) for book_id in genre.book_ids],
            }
        except Exception as e:
            raise ValidationError(str(e))
