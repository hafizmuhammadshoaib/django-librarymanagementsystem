import uuid
from abc import ABC, abstractmethod
from typing import Optional

from book.entities.author_entity import AuthorEntity
from book.models.author import Author


class AuthorAbstractRepository(ABC):
    @abstractmethod
    def get_author_by_id(self, author_id):
        """Legacy method for Django model data."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_author_entity_by_id(self, author_id: uuid.UUID) -> Optional[AuthorEntity]:
        """Get an author entity by ID."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def save_author(self, author_entity: AuthorEntity) -> AuthorEntity:
        """Save an author entity to the repository."""
        raise NotImplementedError("This method should be overridden.")


class AuthorRepository(AuthorAbstractRepository):
    def __init__(self):
        self.author_model = Author

    def get_author_by_id(self, author_id):
        """Legacy method for Django model data."""
        return self.author_model.objects.get(id=author_id)

    def get_author_entity_by_id(self, author_id: uuid.UUID) -> Optional[AuthorEntity]:
        """Get an author entity by ID."""
        try:
            author_model = self.author_model.objects.get(id=author_id)
            return self._model_to_entity(author_model)
        except self.author_model.DoesNotExist:
            return None

    def save_author(self, author_entity: AuthorEntity) -> AuthorEntity:
        """Save an author entity to the repository."""
        # Convert entity to Django model
        author_model = self.author_model(
            id=author_entity.id,
            name=author_entity.name,
            birth_date=author_entity.birth_date,
            death_date=author_entity.death_date,
            created_at=author_entity.created_at,
            updated_at=author_entity.updated_at,
        )
        author_model.save()

        # Convert back to entity
        return self._model_to_entity(author_model)

    def _model_to_entity(self, author_model: Author) -> AuthorEntity:
        """Convert Django model to entity."""
        return AuthorEntity(
            id=author_model.id,
            name=author_model.name,
            birth_date=author_model.birth_date,
            death_date=author_model.death_date,
            created_at=author_model.created_at,
            updated_at=author_model.updated_at,
        )
