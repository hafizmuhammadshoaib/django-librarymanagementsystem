import uuid
from typing import Any, Dict, Optional

from django.forms import ValidationError

from book.entities.author_entity import AuthorEntity
from book.repositories.author_repository import AuthorAbstractRepository


class AuthorCRUDService:
    def __init__(self, author_repository: AuthorAbstractRepository):
        self.author_repository = author_repository

    def get_author(self, author_id):
        """Legacy method for Django model data."""
        return self.author_repository.get_author_by_id(author_id)

    def get_author_entity(self, author_id: str) -> Optional[AuthorEntity]:
        """
        Get an author entity by ID.

        Args:
            author_id: The author ID as string

        Returns:
            AuthorEntity or None if not found
        """
        try:
            author_uuid = uuid.UUID(author_id)
            return self.author_repository.get_author_entity_by_id(author_uuid)
        except ValueError:
            raise ValidationError(f"Invalid author ID format: {author_id}")

    def save_author(self, author_entity: AuthorEntity) -> AuthorEntity:
        """
        Save an author entity.

        Args:
            author_entity: The author entity to save

        Returns:
            The saved author entity
        """
        try:
            return self.author_repository.save_author(author_entity)
        except Exception as e:
            raise ValidationError(str(e))

    def get_author_stats(self, author_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for an author.

        Args:
            author_id: The author ID as string

        Returns:
            Dictionary with author statistics
        """
        try:
            author = self.get_author_entity(author_id)
            if not author:
                raise ValidationError(f"Author with ID {author_id} not found")

            return {
                "id": str(author.id),
                "name": author.name,
                "birth_date": author.birth_date.isoformat(),
                "death_date": author.death_date.isoformat()
                if author.death_date
                else None,
                "is_alive": author.is_alive(),
                "age": author.get_age(),
                "is_contemporary": author.is_contemporary(),
                "is_classic_author": author.is_classic_author(),
                "full_name": author.get_full_name(),
                "initials": author.get_initials(),
            }
        except Exception as e:
            raise ValidationError(str(e))
