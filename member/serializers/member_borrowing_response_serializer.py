from rest_framework import serializers

from .borrowed_book_serializer import BorrowedBookSerializer
from .borrowing_stats_serializer import BorrowingStatsSerializer


class MemberBorrowingResponseSerializer(serializers.Serializer):
    """Serializer for member borrowing response."""

    member_id = serializers.UUIDField()
    borrowing_stats = BorrowingStatsSerializer()
    borrowed_books = BorrowedBookSerializer(many=True)

    @classmethod
    def create_response(cls, member_id, stats, borrowed_books):
        """Create a response instance with the given data."""
        data = {
            "member_id": member_id,
            "borrowing_stats": stats,
            "borrowed_books": borrowed_books,
        }
        return cls(data)
