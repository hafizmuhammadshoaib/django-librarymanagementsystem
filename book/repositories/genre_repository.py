import uuid
from abc import ABC, abstractmethod
from typing import Optional

from book.entities.genre_entity import GenreEntity
from book.models.genre import Genre


class GenreAbstractRepository(ABC):
    @abstractmethod
    def get_genre_by_id(self, genre_id):
        """Legacy method for Django model data."""
        raise NotImplementedError("This method should be overridden.")

    # @abstractmethod
    # def add_genre_to_book(self, book_entity, genre_id):
    #     """Add a genre to a book entity."""
    #     raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_genre_entity_by_id(self, genre_id: uuid.UUID) -> Optional[GenreEntity]:
        """Get a genre entity by ID."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def save_genre(self, genre_entity: GenreEntity) -> GenreEntity:
        """Save a genre entity to the repository."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def entity_to_model(self, entity: GenreEntity) -> Genre:
        """Convert entity to model."""
        raise NotImplementedError("This method should be overridden.")


class GenreRepository(GenreAbstractRepository):
    def __init__(self):
        self.genre_model = Genre

    def get_genre_by_id(self, genre_id):
        """Legacy method for Django model data."""
        return self.genre_model.objects.get(id=genre_id)

    # def add_genre_to_book(self, book_entity: BookEntity, genre_id: uuid.UUID):
    #     """Add a genre to a book entity."""
    #     # Add genre to the book entity
    #     book_entity.add_genre(genre_id)

    #     # Get the genre entity and add the book to it
    #     genre_entity = self.get_genre_entity_by_id(genre_id)
    #     if genre_entity:
    #         genre_entity.add_book(book_entity.id)
    #         # Save the updated genre entity
    #         self.save_genre(genre_entity)

    def get_genre_entity_by_id(self, genre_id: uuid.UUID) -> Optional[GenreEntity]:
        """Get a genre entity by ID."""
        try:
            genre_model = self.genre_model.objects.get(id=genre_id)
            return self._model_to_entity(genre_model)
        except self.genre_model.DoesNotExist:
            return None

    def save_genre(self, genre_entity: GenreEntity) -> GenreEntity:
        """Save a genre entity to the repository."""
        # Convert entity to Django model
        genre_model = self.genre_model(
            id=genre_entity.id,
            name=genre_entity.name,
            created_at=genre_entity.created_at,
            updated_at=genre_entity.updated_at,
        )
        genre_model.save()

        # Convert back to entity
        return self._model_to_entity(genre_model)

    def _model_to_entity(self, genre_model: Genre) -> GenreEntity:
        """Convert Django model to entity."""
        # Get book IDs from the related books
        book_ids = list(genre_model.books.values_list("id", flat=True))

        return GenreEntity(
            id=genre_model.id,
            name=genre_model.name,
            created_at=genre_model.created_at,
            updated_at=genre_model.updated_at,
            book_ids=book_ids,
        )

    def entity_to_model(self, entity: GenreEntity) -> Genre:
        """Convert Django model to entity."""
        # Get book IDs from the related books
        return self.genre_model.objects.get(id=entity.id)
