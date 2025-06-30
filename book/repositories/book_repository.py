import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from book.entities.book_entity import BookEntity
from book.entities.genre_entity import GenreEntity
from book.models.book import Book
from book.models.genre import Genre


class BookAbstractRepository(ABC):
    @abstractmethod
    def add_book(self, book_data):
        """Add a book using Django model data."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def save_book(self, book_entity: BookEntity) -> BookEntity:
        """Save a book entity to the repository."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_book_by_id(self, book_id: uuid.UUID) -> Optional[BookEntity]:
        """Get a book entity by ID."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_book_by_isbn(self, isbn: str) -> Optional[BookEntity]:
        """Get a book entity by ISBN."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_all_books(self) -> List[BookEntity]:
        """Get all book entities."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_books_by_author(self, author_id: uuid.UUID) -> List[BookEntity]:
        """Get books by author ID."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_books_by_publisher(self, publisher_id: uuid.UUID) -> List[BookEntity]:
        """Get books by publisher ID."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def search_books_by_title(self, title: str) -> List[BookEntity]:
        """Search books by title."""
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def add_book_to_genre(self, book_id: uuid.UUID, genre: Genre):
        """Add a genre to a book entity."""
        raise NotImplementedError("This method should be overridden.")


class BookRepository(BookAbstractRepository):
    def __init__(self):
        self.book_model = Book

    def add_book(self, book_data):
        """Legacy method for Django model data."""
        return self.book_model.objects.create(
            title=book_data["title"],
            description=book_data["description"],
            published_date=book_data["published_date"],
            isbn=book_data["isbn"],
            author=book_data["author"],  # Author instance (not author_id)
            publisher=book_data["publisher"],  # Publisher instance (not publisher_id)
        )

    def save_book(self, book_entity: BookEntity) -> BookEntity:
        """Save a book entity to the repository."""
        # Convert entity to Django model
        book_model = self.book_model(
            id=book_entity.id,
            title=book_entity.title,
            description=book_entity.description,
            published_date=book_entity.published_date,
            isbn=book_entity.isbn,
            author_id=book_entity.author_id,
            publisher_id=book_entity.publisher_id,
            created_at=book_entity.created_at,
            updated_at=book_entity.updated_at,
        )
        book_model.save()

        # Convert back to entity
        return self._model_to_entity(book_model)

    def get_book_by_id(self, book_id: uuid.UUID) -> Optional[BookEntity]:
        """Get a book entity by ID."""
        try:
            book_model = self.book_model.objects.get(id=book_id)
            return self._model_to_entity(book_model)
        except self.book_model.DoesNotExist:
            return None

    def get_book_by_isbn(self, isbn: str) -> Optional[BookEntity]:
        """Get a book entity by ISBN."""
        try:
            book_model = self.book_model.objects.get(isbn=isbn)
            return self._model_to_entity(book_model)
        except self.book_model.DoesNotExist:
            return None

    def get_all_books(self) -> List[BookEntity]:
        """Get all book entities."""
        book_models = self.book_model.objects.all()
        return [self._model_to_entity(book_model) for book_model in book_models]

    def get_books_by_author(self, author_id: uuid.UUID) -> List[BookEntity]:
        """Get books by author ID."""
        book_models = self.book_model.objects.filter(author_id=author_id)
        return [self._model_to_entity(book_model) for book_model in book_models]

    def get_books_by_publisher(self, publisher_id: uuid.UUID) -> List[BookEntity]:
        """Get books by publisher ID."""
        book_models = self.book_model.objects.filter(publisher_id=publisher_id)
        return [self._model_to_entity(book_model) for book_model in book_models]

    def search_books_by_title(self, title: str) -> List[BookEntity]:
        """Search books by title."""
        book_models = self.book_model.objects.filter(title__icontains=title)
        return [self._model_to_entity(book_model) for book_model in book_models]

    def add_book_to_genre(self, book_id: uuid.UUID, genre: Genre):
        """Add a genre to a book entity."""
        # Add genre to the book entity
        book = self.book_model.objects.get(id=book_id)
        book.genres.add(genre)  # type: ignore
        return self._model_to_entity(book)

        # Get the genre entity and add the book to it

    def _model_to_entity(self, book_model: Book) -> BookEntity:
        """Convert Django model to entity."""
        # Get the first genre ID if any genres exist
        # Use the reverse relationship through Genre model
        first_genre = Genre.objects.filter(books=book_model).first()
        genre_id = (
            first_genre.id if first_genre else None
        )  # Use default UUID if no genre

        return BookEntity(
            id=book_model.id,
            title=book_model.title,
            description=book_model.description,
            published_date=book_model.published_date,
            isbn=book_model.isbn,
            author_id=book_model.author.id,
            publisher_id=book_model.publisher.id,
            created_at=book_model.created_at,
            updated_at=book_model.updated_at,
            genre_id=genre_id,
        )
