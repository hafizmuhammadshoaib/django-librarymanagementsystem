from typing import Any, Dict, Optional

from django.db import transaction

from book.entities.author_entity import AuthorEntity
from book.entities.book_entity import BookEntity
from book.entities.genre_entity import GenreEntity
from book.entities.publisher_entity import PublisherEntity
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

        # Check if book with same ISBN already exists
        isbn = book_data["isbn"]
        existing_book = self.book_repository.get_book_by_isbn(isbn)

        # Get author entity
        author_id = book_data["author_id"]
        author = self.author_repository.get_author_entity_by_id(author_id)
        # Get publisher entity
        publisher_id = book_data["publisher_id"]
        publisher = self.publisher_repository.get_publisher_entity_by_id(publisher_id)
        # Get genre entity
        genre_id = book_data["genre_id"]
        genre = self.genre_repository.get_genre_entity_by_id(genre_id)

        self._validate_input_data(
            book=existing_book,
            author=author,
            publisher=publisher,
            genre=genre,
        )

        # Create book entity
        book_entity = BookEntity.create(
            title=book_data["title"],
            description=book_data["description"],
            published_date=book_data["published_date"],
            isbn=book_data["isbn"],
            author=author,
            publisher=publisher,
            genre=genre,
        )

        with transaction.atomic():
            saved_book = self.book_repository.save_book(book_entity)
            genre_model = self.genre_repository.entity_to_model(genre)
            saved_book = self.book_repository.add_book_to_genre(
                saved_book.id, genre_model
            )

        return saved_book

    def _validate_input_data(
        self,
        book: Optional[BookEntity],
        author: Optional[AuthorEntity],
        publisher: Optional[PublisherEntity],
        genre: Optional[GenreEntity],
    ):
        """Validate the input data for creating a book."""
        if book:
            raise ValueError(f"Book with ISBN {book.isbn} already exists")
        if not author:
            raise RuntimeError("Author not found")
        if not publisher:
            raise RuntimeError("Publisher not found")
        if not genre:
            raise RuntimeError("Genre not found")
