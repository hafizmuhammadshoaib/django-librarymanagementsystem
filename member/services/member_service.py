from member.repositories.borrowing_repository import BorrowingAbstractRepository


class MemberService:
    def __init__(
        self,
        borrowing_repository: BorrowingAbstractRepository,
        # Remove book_service from constructor - will be injected manually
    ):
        self.borrowing_repository = borrowing_repository
        self.book_service = None  # Will be set manually

    def get_member_borrowing_stats(self, member_id):
        """Get comprehensive borrowing statistics for a member"""
        total_borrowings = self.borrowing_repository.get_borrowing_count_by_member(
            member_id
        )
        active_borrowings = self.borrowing_repository.get_active_borrowings_by_member(
            member_id
        )

        return {
            "total_borrowings": total_borrowings,
            "active_borrowings": len(active_borrowings),
            "returned_borrowings": total_borrowings - len(active_borrowings),
        }

    def get_member_borrowed_books(self, member_id):
        """Get all books borrowed by a member with book details"""
        borrowings = self.borrowing_repository.get_borrowings_by_member(member_id)

        borrowed_books = []
        for borrowing in borrowings:
            # Here we could use book_service to get additional book details
            # if needed, but for now we'll use the direct relationship
            book_data = {
                "book_id": str(borrowing.book.id),
                "book_title": borrowing.book.title,
                "borrowing_date": borrowing.borrowing_date,
                "returning_date": borrowing.returning_date,
                "is_active": borrowing.returning_date is None,
            }
            borrowed_books.append(book_data)

        return borrowed_books

    def get_member_active_books(self, member_id):
        """Get currently active book borrowings for a member"""
        active_borrowings = self.borrowing_repository.get_active_borrowings_by_member(
            member_id
        )

        active_books = []
        for borrowing in active_borrowings:
            book_data = {
                "book_id": str(borrowing.book.id),
                "book_title": borrowing.book.title,
                "borrowing_date": borrowing.borrowing_date,
                "days_borrowed": (
                    borrowing.borrowing_date - borrowing.borrowing_date
                ).days,  # Placeholder
            }
            active_books.append(book_data)

        return active_books
