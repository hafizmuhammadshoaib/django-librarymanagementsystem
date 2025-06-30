import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from member.entities.borrowing_entity import BorrowingEntity
from member.models.borrowing_history import BorrowingHistory


class BorrowingAbstractRepository(ABC):
    @abstractmethod
    def get_borrowings_by_member(self, member_id):
        """Legacy method for Django model data."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_active_borrowings_by_member(self, member_id):
        """Legacy method for Django model data."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_borrowing_count_by_member(self, member_id):
        """Legacy method for Django model data."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def save_borrowing(self, borrowing_entity: BorrowingEntity) -> BorrowingEntity:
        """Save a borrowing entity to the repository."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_active_borrowings_by_member_entity(
        self, member_id: uuid.UUID
    ) -> List[BorrowingEntity]:
        """Get all active borrowings for a member entity."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_active_borrowings_by_book_entity(
        self, book_id: uuid.UUID
    ) -> List[BorrowingEntity]:
        """Get all active borrowings for a book entity."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_borrowing_ids_by_member(self, member_id: uuid.UUID) -> List[uuid.UUID]:
        """Get all borrowing IDs for a member."""
        raise NotImplementedError("This method should be overridden.")


class BorrowingRepository(BorrowingAbstractRepository):
    def __init__(self):
        self.borrowing_model = BorrowingHistory

    def get_borrowings_by_member(self, member_id):
        """Legacy method for Django model data."""
        return self.borrowing_model.objects.filter(member_id=member_id)

    def get_active_borrowings_by_member(self, member_id):
        """Legacy method for Django model data."""
        return self.borrowing_model.objects.filter(
            member_id=member_id, returning_date__isnull=True
        )

    def get_borrowing_count_by_member(self, member_id):
        """Legacy method for Django model data."""
        return self.borrowing_model.objects.filter(member_id=member_id).count()

    def save_borrowing(self, borrowing_entity: BorrowingEntity) -> BorrowingEntity:
        """Save a borrowing entity to the repository."""
        # Convert entity to Django model
        borrowing_model = self.borrowing_model(
            id=borrowing_entity.id,
            book_id=borrowing_entity.book_id,
            member_id=borrowing_entity.member_id,
            borrowing_date=borrowing_entity.borrowing_date,
            returning_date=borrowing_entity.returning_date,
            created_at=borrowing_entity.created_at,
            updated_at=borrowing_entity.updated_at,
        )
        borrowing_model.save()

        # Convert back to entity
        return self._model_to_entity(borrowing_model)

    def get_active_borrowings_by_member_entity(
        self, member_id: uuid.UUID
    ) -> List[BorrowingEntity]:
        """Get all active borrowings for a member entity."""
        borrowing_models = self.borrowing_model.objects.filter(
            member_id=member_id, returning_date__isnull=True
        )
        return [
            self._model_to_entity(borrowing_model)
            for borrowing_model in borrowing_models
        ]

    def get_active_borrowings_by_book_entity(
        self, book_id: uuid.UUID
    ) -> List[BorrowingEntity]:
        """Get all active borrowings for a book entity."""
        borrowing_models = self.borrowing_model.objects.filter(
            book_id=book_id, returning_date__isnull=True
        )
        return [
            self._model_to_entity(borrowing_model)
            for borrowing_model in borrowing_models
        ]

    def get_borrowing_ids_by_member(self, member_id: uuid.UUID) -> List[uuid.UUID]:
        """Get all borrowing IDs for a member."""
        return list(
            self.borrowing_model.objects.filter(member_id=member_id).values_list(
                "id", flat=True
            )
        )

    def _model_to_entity(self, borrowing_model: BorrowingHistory) -> BorrowingEntity:
        """Convert Django model to entity."""
        return BorrowingEntity(
            id=borrowing_model.id,
            book_id=borrowing_model.book.id,
            member_id=borrowing_model.member.id,
            borrowing_date=borrowing_model.borrowing_date,
            returning_date=borrowing_model.returning_date,
            created_at=borrowing_model.created_at,
            updated_at=borrowing_model.updated_at,
        )
