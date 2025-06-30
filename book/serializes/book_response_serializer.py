from rest_framework import serializers


class BookResponseSerializer(serializers.Serializer):
    """Serializer for book response data."""

    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    published_date = serializers.DateField()
    isbn = serializers.CharField()
    author_id = serializers.UUIDField()
    publisher_id = serializers.UUIDField()
    genre_id = serializers.UUIDField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
