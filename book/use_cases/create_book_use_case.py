from typing import Any, Dict

from django.db import transaction

from book.entities.book_entity import BookEntity
from book.repositories.author_repository import AuthorAbstractRepository
from book.repositories.book_repository import BookAbstractRepository
from book.repositories.genre_repository import GenreAbstractRepository
from book.repositories.publisher_repository import PublisherAbstractRepository


class CreateBookUseCase:
    """Use case for creating a new book."""

    def __init__(
        self,
        book_repository: BookAbstractRepository,
        author_repository: AuthorAbstractRepository,
        publisher_repository: PublisherAbstractRepository,
        genre_repository: GenreAbstractRepository,
    ):
        self.book_repository = book_repository
        self.author_repository = author_repository
        self.publisher_repository = publisher_repository
        self.genre_repository = genre_repository

    def execute(self, book_data: Dict[str, Any]) -> BookEntity:
        """
        Execute the create book use case.

        Args:
            book_data: Dictionary containing book information

        Returns:
            BookEntity: The created book entity

        Raises:
            ValueError: If validation fails
            RuntimeError: If required entities don't exist
        """
        # Validate input data
        self._validate_input_data(book_data)

        # Check if book with same ISBN already exists
        existing_book = self.book_repository.get_book_by_isbn(book_data["isbn"])
        if existing_book:
            raise ValueError(f"Book with ISBN {book_data['isbn']} already exists")

        # Get author entity
        author_id = book_data["author_id"]
        author = self.author_repository.get_author_entity_by_id(author_id)
        if not author:
            raise RuntimeError(f"Author with ID {author_id} not found")

        # Get publisher entity
        publisher_id = book_data["publisher_id"]
        publisher = self.publisher_repository.get_publisher_entity_by_id(publisher_id)
        if not publisher:
            raise RuntimeError(f"Publisher with ID {publisher_id} not found")

        # Create book entity
        book_entity = BookEntity(
            title=book_data["title"],
            description=book_data["description"],
            published_date=book_data["published_date"],
            isbn=book_data["isbn"],
            author_id=author_id,
            publisher_id=publisher_id,
        )

        genre_id = book_data["genre_id"]
        genre = self.genre_repository.get_genre_entity_by_id(genre_id)
        if not genre:
            raise RuntimeError(f"Genre with ID {genre_id} not found")

        with transaction.atomic():
            saved_book = self.book_repository.save_book(book_entity)
            genre_model = self.genre_repository.entity_to_model(genre)
            saved_book = self.book_repository.add_book_to_genre(
                saved_book.id, genre_model
            )

        return saved_book

    def _validate_input_data(self, book_data: Dict[str, Any]):
        """Validate the input data for creating a book."""
        required_fields = [
            "title",
            "description",
            "published_date",
            "isbn",
            "author_id",
            "publisher_id",
        ]

        for field in required_fields:
            if field not in book_data:
                raise ValueError(f"Missing required field: {field}")

            if not book_data[field]:
                raise ValueError(f"Field {field} cannot be empty")

        # Debug: Check isbn field type
        if "isbn" in book_data:
            isbn_value = book_data["isbn"]
            if not isinstance(isbn_value, str):
                raise ValueError(
                    f"ISBN must be a string, got {type(isbn_value)}: {isbn_value}"
                )

        # Validate UUID fields
        # try:
        #     uuid.UUID(book_data["author_id"])
        #     uuid.UUID(book_data["publisher_id"])
        # except ValueError:
        #     raise ValueError("Invalid UUID format for author_id or publisher_id")

        # Validate genre_ids if provided
        if "genre_ids" in book_data:
            if not isinstance(book_data["genre_ids"], list):
                raise ValueError("genre_ids must be a list")
