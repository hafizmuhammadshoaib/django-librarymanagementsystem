from rest_framework import serializers


class BookCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    published_date = serializers.DateField()
    isbn = serializers.CharField(max_length=13)
    author_id = serializers.UUIDField()
    publisher_id = serializers.UUIDField()
    genre_id = serializers.UUIDField()


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


class AuthorResponseSerializer(serializers.Serializer):
    """Serializer for author response data."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    birth_date = serializers.DateField()
    death_date = serializers.DateField(allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class PublisherResponseSerializer(serializers.Serializer):
    """Serializer for publisher response data."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    website = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class GenreResponseSerializer(serializers.Serializer):
    """Serializer for genre response data."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


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
