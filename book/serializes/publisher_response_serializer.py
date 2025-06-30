from rest_framework import serializers


class PublisherResponseSerializer(serializers.Serializer):
    """Serializer for publisher response data."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    website = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
