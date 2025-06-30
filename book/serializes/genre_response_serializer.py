from rest_framework import serializers


class GenreResponseSerializer(serializers.Serializer):
    """Serializer for genre response data."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
