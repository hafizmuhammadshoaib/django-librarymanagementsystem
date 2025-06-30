import uuid
from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict, Optional

from book.entities.book_entity import BookEntity
from book.repositories.book_repository import BookAbstractRepository
from member.entities.borrowing_entity import BorrowingEntity
from member.entities.member_entity import MemberEntity
from member.repositories.borrowing_repository import BorrowingAbstractRepository
from member.repositories.member_repository import MemberAbstractRepository


class MemberRepositoryInterface(ABC):
    """Abstract interface for member repository."""

    @abstractmethod
    def get_member_by_id(self, member_id: uuid.UUID) -> Optional[MemberEntity]:
        """Get a member by ID."""
        pass

    @abstractmethod
    def save_member(self, member_entity: MemberEntity) -> MemberEntity:
        """Save a member entity to the repository."""
        pass


class BorrowingRepositoryInterface(ABC):
    """Abstract interface for borrowing repository."""

    @abstractmethod
    def save_borrowing(self, borrowing_entity: BorrowingEntity) -> BorrowingEntity:
        """Save a borrowing entity to the repository."""
        pass

    @abstractmethod
    def get_active_borrowings_by_member(
        self, member_id: uuid.UUID
    ) -> list[BorrowingEntity]:
        """Get all active borrowings for a member."""
        pass

    @abstractmethod
    def get_active_borrowings_by_book(
        self, book_id: uuid.UUID
    ) -> list[BorrowingEntity]:
        """Get all active borrowings for a book."""
        pass


class BookRepositoryInterface(ABC):
    """Abstract interface for book repository."""

    @abstractmethod
    def get_book_by_id(self, book_id: uuid.UUID) -> Optional[BookEntity]:
        """Get a book by ID."""
        pass


class BorrowBookUseCase:
    """Use case for borrowing a book."""

    def __init__(
        self,
        member_repository: MemberAbstractRepository,
        borrowing_repository: BorrowingAbstractRepository,
        book_repository: BookAbstractRepository,
    ):
        self.member_repository = member_repository
        self.borrowing_repository = borrowing_repository
        self.book_repository = book_repository

    def execute(self, borrowing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the borrow book use case.

        Args:
            borrowing_data: Dictionary containing borrowing information
                - member_id: str
                - book_id: str
                - borrowing_date: date (optional, defaults to today)

        Returns:
            Dictionary with borrowing details

        Raises:
            ValueError: If validation fails
            RuntimeError: If required entities don't exist or business rules are violated
        """
        # Validate input data
        self._validate_input_data(borrowing_data)

        # Parse UUIDs
        member_id = uuid.UUID(borrowing_data["member_id"])
        book_id = uuid.UUID(borrowing_data["book_id"])

        # Get member entity
        member = self.member_repository.get_member_by_id(member_id)
        if not member:
            raise RuntimeError(f"Member with ID {member_id} not found")

        # Get book entity
        book = self.book_repository.get_book_by_id(book_id)
        if not book:
            raise RuntimeError(f"Book with ID {book_id} not found")

        # Check business rules
        self._check_borrowing_rules(member, book)

        # Get borrowing date
        borrowing_date = borrowing_data.get("borrowing_date", date.today())

        # Create borrowing entity
        borrowing_entity = BorrowingEntity.create(
            book_id=book_id,
            member_id=member_id,
            borrowing_date=borrowing_date,
        )

        # Save borrowing to repository
        saved_borrowing = self.borrowing_repository.save_borrowing(borrowing_entity)

        # Update member's borrowing list
        member.add_borrowing(saved_borrowing.id)
        self.member_repository.save_member(member)

        return saved_borrowing.to_dict()

    def _validate_input_data(self, borrowing_data: Dict[str, Any]):
        """Validate the input data for borrowing a book."""
        required_fields = ["member_id", "book_id"]

        for field in required_fields:
            if field not in borrowing_data:
                raise ValueError(f"Missing required field: {field}")

            if not borrowing_data[field]:
                raise ValueError(f"Field {field} cannot be empty")

        # Validate UUID fields
        try:
            uuid.UUID(borrowing_data["member_id"])
            uuid.UUID(borrowing_data["book_id"])
        except ValueError:
            raise ValueError("Invalid UUID format for member_id or book_id")

        # Validate borrowing_date if provided
        if "borrowing_date" in borrowing_data:
            if not isinstance(borrowing_data["borrowing_date"], date):
                raise ValueError("borrowing_date must be a date object")

    def _check_borrowing_rules(self, member: MemberEntity, book: BookEntity):
        """Check business rules for borrowing."""
        # Check if member can borrow more books
        if not member.can_borrow_more_books():
            raise RuntimeError(
                f"Member {member.get_full_name()} has reached the maximum number of borrowings"
            )

        # Check if book is available for borrowing
        if not book.is_available_for_borrowing():
            raise RuntimeError(f"Book '{book.title}' is not available for borrowing")

        # Check if member is a minor (additional restrictions could apply)
        if member.is_minor():
            # Could add special rules for minors here
            pass

        # Check if book is already borrowed by this member
        active_borrowings = (
            self.borrowing_repository.get_active_borrowings_by_member_entity(member.id)
        )
        for borrowing in active_borrowings:
            if borrowing.book_id == book.id:
                raise RuntimeError(
                    f"Member {member.get_full_name()} has already borrowed '{book.title}'"
                )

    def return_book(
        self, borrowing_id: str, return_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Return a borrowed book.

        Args:
            borrowing_id: The borrowing ID as string
            return_date: The return date (optional, defaults to today)

        Returns:
            Dictionary with updated borrowing details
        """
        try:
            borrowing_uuid = uuid.UUID(borrowing_id)
        except ValueError:
            raise ValueError(f"Invalid borrowing ID format: {borrowing_id}")

        # Get borrowing entity (this would need to be implemented in the repository)
        # For now, we'll assume we can get it somehow
        # borrowing = self.borrowing_repository.get_borrowing_by_id(borrowing_uuid)
        # if not borrowing:
        #     raise RuntimeError(f"Borrowing with ID {borrowing_id} not found")

        # borrowing.return_book(return_date)
        # saved_borrowing = self.borrowing_repository.save_borrowing(borrowing)

        # Update member's borrowing list
        # member = self.member_repository.get_member_by_id(borrowing.member_id)
        # if member:
        #     member.remove_borrowing(borrowing.id)
        #     self.member_repository.save_member(member)

        # return saved_borrowing.to_dict()

        # Placeholder implementation
        raise NotImplementedError("Return book functionality needs to be implemented")

    def get_member_borrowings(self, member_id: uuid.UUID) -> list[Dict[str, Any]]:
        """
        Get all borrowings for a member.

        Args:
            member_id: The member ID as string

        Returns:
            List of borrowing dictionaries
        """
        try:
            member_uuid = member_id
        except ValueError:
            raise ValueError(f"Invalid member ID format: {member_id}")

        # Verify member exists
        member = self.member_repository.get_member_by_id(member_uuid)
        if not member:
            raise RuntimeError(f"Member with ID {member_id} not found")

        borrowings = self.borrowing_repository.get_active_borrowings_by_member_entity(
            member_uuid
        )
        return [borrowing.to_dict() for borrowing in borrowings]

    def get_overdue_borrowings(self) -> list[Dict[str, Any]]:
        """
        Get all overdue borrowings.

        Returns:
            List of overdue borrowing dictionaries
        """
        # This would need to be implemented in the repository
        # For now, we'll return an empty list
        return []

    def renew_borrowing(self, borrowing_id: str) -> Dict[str, Any]:
        """
        Renew a borrowing.

        Args:
            borrowing_id: The borrowing ID as string

        Returns:
            Dictionary with updated borrowing details
        """
        try:
            borrowing_uuid = uuid.UUID(borrowing_id)
        except ValueError:
            raise ValueError(f"Invalid borrowing ID format: {borrowing_id}")

        # This would need to be implemented
        # borrowing = self.borrowing_repository.get_borrowing_by_id(borrowing_uuid)
        # if not borrowing:
        #     raise RuntimeError(f"Borrowing with ID {borrowing_id} not found")

        # if not borrowing.can_be_renewed():
        #     raise RuntimeError("Borrowing cannot be renewed")

        # borrowing.renew_borrowing()
        # saved_borrowing = self.borrowing_repository.save_borrowing(borrowing)
        # return saved_borrowing.to_dict()

        # Placeholder implementation
        raise NotImplementedError(
            "Renew borrowing functionality needs to be implemented"
        )
