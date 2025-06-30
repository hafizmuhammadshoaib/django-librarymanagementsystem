import uuid
from abc import ABC, abstractmethod
from typing import Optional

from book.entities.publisher_entity import PublisherEntity
from book.models.publisher import Publisher


class PublisherAbstractRepository(ABC):
    @abstractmethod
    def get_publisher_by_id(self, publisher_id):
        """Legacy method for Django model data."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_publisher_entity_by_id(
        self, publisher_id: uuid.UUID
    ) -> Optional[PublisherEntity]:
        """Get a publisher entity by ID."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def save_publisher(self, publisher_entity: PublisherEntity) -> PublisherEntity:
        """Save a publisher entity to the repository."""
        raise NotImplementedError("This method should be overridden.")


class PublisherRepository(PublisherAbstractRepository):
    def __init__(self):
        self.publisher_model = Publisher

    def get_publisher_by_id(self, publisher_id):
        """Legacy method for Django model data."""
        return self.publisher_model.objects.get(id=publisher_id)

    def get_publisher_entity_by_id(
        self, publisher_id: uuid.UUID
    ) -> Optional[PublisherEntity]:
        """Get a publisher entity by ID."""
        try:
            publisher_model = self.publisher_model.objects.get(id=publisher_id)
            return self._model_to_entity(publisher_model)
        except self.publisher_model.DoesNotExist:
            return None

    def save_publisher(self, publisher_entity: PublisherEntity) -> PublisherEntity:
        """Save a publisher entity to the repository."""
        # Convert entity to Django model
        publisher_model = self.publisher_model(
            id=publisher_entity.id,
            name=publisher_entity.name,
            website=publisher_entity.website,
            created_at=publisher_entity.created_at,
            updated_at=publisher_entity.updated_at,
        )
        publisher_model.save()

        # Convert back to entity
        return self._model_to_entity(publisher_model)

    def _model_to_entity(self, publisher_model: Publisher) -> PublisherEntity:
        """Convert Django model to entity."""
        return PublisherEntity(
            id=publisher_model.id,
            name=publisher_model.name,
            website=publisher_model.website,
            created_at=publisher_model.created_at,
            updated_at=publisher_model.updated_at,
        )
