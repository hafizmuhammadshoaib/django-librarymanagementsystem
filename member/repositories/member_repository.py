import uuid
from abc import ABC, abstractmethod
from typing import Optional

from django.db.models import Count

from member.entities.member_entity import MemberEntity
from member.models.borrowing_history import BorrowingHistory
from member.models.member import Member


class MemberAbstractRepository(ABC):
    @abstractmethod
    def get_member_by_id(self, member_id: uuid.UUID) -> Optional[MemberEntity]:
        """Get a member entity by ID."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def save_member(self, member_entity: MemberEntity) -> MemberEntity:
        """Save a member entity to the repository."""
        raise NotImplementedError("This method should be overridden.")


class MemberRepository(MemberAbstractRepository):
    def __init__(self):
        self.member_model = Member

    def get_member_by_id(self, member_id: uuid.UUID) -> Optional[MemberEntity]:
        """Get a member entity by ID with borrowing IDs in a single query."""
        try:
            # Use prefetch_related to get member and borrowing IDs in one query
            member_model = self.member_model.objects.prefetch_related(
                "borrowinghistory_set"
            ).get(id=member_id)

            # Extract borrowing IDs from the prefetched related objects
            borrowing_ids = [
                borrowing.id
                for borrowing in member_model.borrowinghistory_set.all()  # type: ignore
            ]

            return self._model_to_entity(member_model, borrowing_ids)
        except self.member_model.DoesNotExist:
            return None

    def get_member_with_borrowing_count(
        self, member_id: uuid.UUID
    ) -> Optional[MemberEntity]:
        """Get a member entity by ID with borrowing count using annotate (more efficient)."""
        try:
            # Use annotate to get member and borrowing count in one query
            member_model = self.member_model.objects.annotate(
                borrowing_count=Count("borrowinghistory")
            ).get(id=member_id)

            # For this method, we'll use empty list since we only have count
            # You could modify this based on your needs
            borrowing_ids = []

            return self._model_to_entity(member_model, borrowing_ids)
        except self.member_model.DoesNotExist:
            return None

    def save_member(self, member_entity: MemberEntity) -> MemberEntity:
        """Save a member entity to the repository."""
        # Convert entity to Django model
        member_model = self.member_model(
            id=member_entity.id,
            first_name=member_entity.first_name,
            last_name=member_entity.last_name,
            birth_date=member_entity.birth_date,
            created_at=member_entity.created_at,
            updated_at=member_entity.updated_at,
        )
        member_model.save()

        # Convert back to entity (with empty borrowing_ids for new members)
        return self._model_to_entity(member_model, [])

    def _model_to_entity(
        self, member_model: Member, borrowing_ids: list[uuid.UUID]
    ) -> MemberEntity:
        """Convert Django model to entity."""
        return MemberEntity(
            id=member_model.id,
            first_name=member_model.first_name,
            last_name=member_model.last_name,
            birth_date=member_model.birth_date,
            created_at=member_model.created_at,
            updated_at=member_model.updated_at,
            borrowing_ids=borrowing_ids,
        )
