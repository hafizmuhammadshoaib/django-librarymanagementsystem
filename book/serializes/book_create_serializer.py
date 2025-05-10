from rest_framework import serializers


class BookCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=255)
    published_date = serializers.DateField()
    isbn = serializers.CharField(max_length=13)
    author_id = serializers.UUIDField()
    publisher_id = serializers.UUIDField()
    genre_id = serializers.UUIDField()
