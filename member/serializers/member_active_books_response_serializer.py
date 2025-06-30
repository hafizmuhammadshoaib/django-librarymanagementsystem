from rest_framework import serializers

from .active_book_serializer import ActiveBookSerializer


class MemberActiveBooksResponseSerializer(serializers.Serializer):
    """Serializer for member active books response."""

    member_id = serializers.UUIDField()
    active_books = ActiveBookSerializer(many=True)
    count = serializers.IntegerField()

    @classmethod
    def create_response(cls, member_id, active_books):
        """Create a response instance with the given data."""
        data = {
            "member_id": member_id,
            "active_books": active_books,
            "count": len(active_books),
        }
        return cls(data)
