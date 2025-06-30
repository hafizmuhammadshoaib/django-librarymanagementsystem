from rest_framework import serializers


class ActiveBookSerializer(serializers.Serializer):
    """Serializer for active book borrowing information."""

    book_id = serializers.UUIDField()
    borrowing_id = serializers.UUIDField()
    borrowing_date = serializers.DateField()
    borrowing_duration_days = serializers.IntegerField()
    remaining_days = serializers.IntegerField()
    is_overdue = serializers.BooleanField()
    fine_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    can_be_renewed = serializers.BooleanField()
