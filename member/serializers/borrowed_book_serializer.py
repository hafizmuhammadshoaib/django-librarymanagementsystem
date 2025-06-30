from rest_framework import serializers


class BorrowedBookSerializer(serializers.Serializer):
    """Serializer for borrowed book information."""

    book_id = serializers.UUIDField()
    borrowing_id = serializers.UUIDField()
    borrowing_date = serializers.DateField()
    returning_date = serializers.DateField(allow_null=True)
    is_active = serializers.BooleanField()
    is_overdue = serializers.BooleanField()
    status = serializers.CharField()
    due_date = serializers.DateField()
    days_overdue = serializers.IntegerField()
    fine_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    can_be_renewed = serializers.BooleanField()
