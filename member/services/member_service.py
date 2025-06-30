import uuid
from typing import Any, Dict, List, Optional

from django.forms import ValidationError

from member.repositories.borrowing_repository import BorrowingAbstractRepository
from member.repositories.member_repository import MemberAbstractRepository
from member.use_cases.borrow_book_use_case import BorrowBookUseCase


class MemberService:
    def __init__(
        self,
        borrowing_repository: BorrowingAbstractRepository,
        member_repository: MemberAbstractRepository,
        borrow_book_use_case: BorrowBookUseCase,
    ):
        self.borrowing_repository = borrowing_repository
        self.member_repository = member_repository
        self.borrow_book_use_case = borrow_book_use_case

    def borrow_book(self, borrowing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Borrow a book using the BorrowBookUseCase.

        Args:
            borrowing_data: Dictionary containing borrowing information
                - member_id: str
                - book_id: str
                - borrowing_date: date (optional, defaults to today)

        Returns:
            Dictionary with borrowing details

        Raises:
            ValidationError: If validation fails or business rules are violated
        """
        try:
            return self.borrow_book_use_case.execute(borrowing_data)
        except (ValueError, RuntimeError) as e:
            raise ValidationError(str(e))

    def get_member_borrowings(self, member_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Get all borrowings for a member using the BorrowBookUseCase.

        Args:
            member_id: The member ID as string

        Returns:
            List of borrowing dictionaries
        """
        try:
            return self.borrow_book_use_case.get_member_borrowings(member_id)
        except (ValueError, RuntimeError) as e:
            raise ValidationError(str(e))

    def get_member_borrowing_stats(self, member_id: uuid.UUID) -> Dict[str, Any]:
        """Get comprehensive borrowing statistics for a member"""
        try:
            member_uuid = member_id
            member = self.member_repository.get_member_by_id(member_uuid)

            if not member:
                raise ValidationError(f"Member with ID {member_id} not found")

            # Use entity business logic
            borrowing_count = member.get_borrowing_count()
            is_active_borrower = member.is_active_borrower()
            is_heavy_borrower = member.is_heavy_borrower()
            can_borrow_more = member.can_borrow_more_books()

            return {
                "total_borrowings": borrowing_count,
                "active_borrowings": borrowing_count,  # All borrowings are active in entity
                "returned_borrowings": 0,  # Would need to be calculated from actual borrowings
                "is_active_borrower": is_active_borrower,
                "is_heavy_borrower": is_heavy_borrower,
                "can_borrow_more": can_borrow_more,
                "member_age": member.get_age(),
                "is_minor": member.is_minor(),
                "is_senior": member.is_senior(),
                "membership_duration_days": member.get_membership_duration_days(),
                "is_long_term_member": member.is_long_term_member(),
            }
        except Exception as e:
            raise ValidationError(str(e))

    def get_member_borrowed_books(self, member_id: uuid.UUID) -> List[Dict[str, Any]]:
        """Get all books borrowed by a member with book details"""
        try:
            borrowings = self.borrow_book_use_case.get_member_borrowings(member_id)

            borrowed_books = []
            for borrowing in borrowings:
                book_data = {
                    "book_id": borrowing["book_id"],
                    "borrowing_id": borrowing["id"],
                    "borrowing_date": borrowing["borrowing_date"],
                    "returning_date": borrowing["returning_date"],
                    "is_active": borrowing["is_returned"] is False,
                    "is_overdue": borrowing["is_overdue"],
                    "status": borrowing["status"],
                    "due_date": borrowing["due_date"],
                    "days_overdue": borrowing["days_overdue"],
                    "fine_amount": borrowing["fine_amount"],
                    "can_be_renewed": borrowing["can_be_renewed"],
                }
                borrowed_books.append(book_data)

            return borrowed_books
        except Exception as e:
            raise ValidationError(str(e))

    def get_member_active_books(self, member_id: uuid.UUID) -> List[Dict[str, Any]]:
        """Get currently active book borrowings for a member"""
        try:
            borrowings = self.borrow_book_use_case.get_member_borrowings(member_id)

            # Filter for active borrowings (not returned)
            active_borrowings = [b for b in borrowings if not b["is_returned"]]

            active_books = []
            for borrowing in active_borrowings:
                book_data = {
                    "book_id": borrowing["book_id"],
                    "borrowing_id": borrowing["id"],
                    "borrowing_date": borrowing["borrowing_date"],
                    "borrowing_duration_days": borrowing["borrowing_duration_days"],
                    "remaining_days": borrowing["remaining_days"],
                    "is_overdue": borrowing["is_overdue"],
                    "fine_amount": borrowing["fine_amount"],
                    "can_be_renewed": borrowing["can_be_renewed"],
                }
                active_books.append(book_data)

            return active_books
        except Exception as e:
            raise ValidationError(str(e))

    def get_overdue_borrowings(self) -> List[Dict[str, Any]]:
        """
        Get all overdue borrowings using the BorrowBookUseCase.

        Returns:
            List of overdue borrowing dictionaries
        """
        try:
            return self.borrow_book_use_case.get_overdue_borrowings()
        except Exception as e:
            raise ValidationError(str(e))

    def renew_borrowing(self, borrowing_id: str) -> Dict[str, Any]:
        """
        Renew a borrowing using the BorrowBookUseCase.

        Args:
            borrowing_id: The borrowing ID as string

        Returns:
            Dictionary with updated borrowing details
        """
        try:
            return self.borrow_book_use_case.renew_borrowing(borrowing_id)
        except (ValueError, RuntimeError) as e:
            raise ValidationError(str(e))

    def return_book(
        self, borrowing_id: str, return_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Return a borrowed book using the BorrowBookUseCase.

        Args:
            borrowing_id: The borrowing ID as string
            return_date: The return date as string (optional, defaults to today)

        Returns:
            Dictionary with updated borrowing details
        """
        try:
            # Convert string date to date object if provided
            from datetime import date

            parsed_return_date = None
            if return_date:
                parsed_return_date = date.fromisoformat(return_date)

            return self.borrow_book_use_case.return_book(
                borrowing_id, parsed_return_date
            )
        except (ValueError, RuntimeError) as e:
            raise ValidationError(str(e))
