from rest_framework import serializers


class AuthorResponseSerializer(serializers.Serializer):
    """Serializer for author response data."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    birth_date = serializers.DateField()
    death_date = serializers.DateField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
