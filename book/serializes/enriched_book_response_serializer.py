from rest_framework import serializers

from .author_response_serializer import AuthorResponseSerializer
from .genre_response_serializer import GenreResponseSerializer
from .publisher_response_serializer import PublisherResponseSerializer


class EnrichedBookResponseSerializer(serializers.Serializer):
    """Serializer for enriched book response data with related entities."""

    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    published_date = serializers.DateField()
    isbn = serializers.CharField()
    author = AuthorResponseSerializer(
        allow_null=True,
    )
    publisher = PublisherResponseSerializer(allow_null=True)
    genre = GenreResponseSerializer(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
