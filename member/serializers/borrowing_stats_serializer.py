from rest_framework import serializers


class BorrowingStatsSerializer(serializers.Serializer):
    """Serializer for member borrowing statistics."""

    total_borrowings = serializers.IntegerField()
    active_borrowings = serializers.IntegerField()
    returned_borrowings = serializers.IntegerField()
    is_active_borrower = serializers.BooleanField()
    is_heavy_borrower = serializers.BooleanField()
    can_borrow_more = serializers.BooleanField()
    member_age = serializers.IntegerField()
    is_minor = serializers.BooleanField()
    is_senior = serializers.BooleanField()
    membership_duration_days = serializers.IntegerField()
    is_long_term_member = serializers.BooleanField()
