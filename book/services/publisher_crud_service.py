import uuid
from typing import Any, Dict, Optional

from django.forms import ValidationError

from book.entities.publisher_entity import PublisherEntity
from book.repositories.publisher_repository import PublisherAbstractRepository


class PublisherCRUDService:
    def __init__(self, publisher_repository: PublisherAbstractRepository):
        self.publisher_repository = publisher_repository

    def get_publisher(self, publisher_id):
        """Legacy method for Django model data."""
        return self.publisher_repository.get_publisher_by_id(publisher_id)

    def get_publisher_entity(self, publisher_id: str) -> Optional[PublisherEntity]:
        """
        Get a publisher entity by ID.

        Args:
            publisher_id: The publisher ID as string

        Returns:
            PublisherEntity or None if not found
        """
        try:
            publisher_uuid = uuid.UUID(publisher_id)
            return self.publisher_repository.get_publisher_entity_by_id(publisher_uuid)
        except ValueError:
            raise ValidationError(f"Invalid publisher ID format: {publisher_id}")

    def save_publisher(self, publisher_entity: PublisherEntity) -> PublisherEntity:
        """
        Save a publisher entity.

        Args:
            publisher_entity: The publisher entity to save

        Returns:
            The saved publisher entity
        """
        try:
            return self.publisher_repository.save_publisher(publisher_entity)
        except Exception as e:
            raise ValidationError(str(e))

    def get_publisher_stats(self, publisher_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for a publisher.

        Args:
            publisher_id: The publisher ID as string

        Returns:
            Dictionary with publisher statistics
        """
        try:
            publisher = self.get_publisher_entity(publisher_id)
            if not publisher:
                raise ValidationError(f"Publisher with ID {publisher_id} not found")

            return {
                "id": str(publisher.id),
                "name": publisher.name,
                "website": publisher.website,
                "domain": publisher.get_domain(),
                "is_major_publisher": publisher.is_major_publisher(),
                "is_university_press": publisher.is_university_press(),
                "is_independent_publisher": publisher.is_independent_publisher(),
                "display_name": publisher.get_display_name(),
            }
        except Exception as e:
            raise ValidationError(str(e))
