import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from book.entities.author_entity import AuthorEntity
from book.entities.book_entity import BookEntity
from book.entities.genre_entity import GenreEntity
from book.entities.publisher_entity import PublisherEntity
from book.repositories.author_repository import AuthorAbstractRepository
from book.repositories.book_repository import BookAbstractRepository
from book.repositories.genre_repository import GenreAbstractRepository
from book.repositories.publisher_repository import PublisherAbstractRepository


class BookRepositoryInterface(ABC):
    """Abstract interface for book repository."""

    @abstractmethod
    def get_book_by_id(self, book_id: uuid.UUID) -> Optional[BookEntity]:
        """Get a book by ID."""
        pass

    @abstractmethod
    def get_all_books(self) -> List[BookEntity]:
        """Get all books."""
        pass

    @abstractmethod
    def get_books_by_author(self, author_id: uuid.UUID) -> List[BookEntity]:
        """Get books by author ID."""
        pass

    @abstractmethod
    def get_books_by_publisher(self, publisher_id: uuid.UUID) -> List[BookEntity]:
        """Get books by publisher ID."""
        pass

    @abstractmethod
    def search_books_by_title(self, title: str) -> List[BookEntity]:
        """Search books by title."""
        pass


class AuthorRepositoryInterface(ABC):
    """Abstract interface for author repository."""

    @abstractmethod
    def get_author_by_id(self, author_id: uuid.UUID) -> Optional[AuthorEntity]:
        """Get an author by ID."""
        pass


class PublisherRepositoryInterface(ABC):
    """Abstract interface for publisher repository."""

    @abstractmethod
    def get_publisher_by_id(self, publisher_id: uuid.UUID) -> Optional[PublisherEntity]:
        """Get a publisher by ID."""
        pass


class GenreRepositoryInterface(ABC):
    """Abstract interface for genre repository."""

    @abstractmethod
    def get_genre_by_id(self, genre_id: uuid.UUID) -> Optional[GenreEntity]:
        """Get a genre by ID."""
        pass


class GetBookUseCase:
    """Use case for retrieving books."""

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

    def get_book_by_id(self, book_id: str) -> Optional[BookEntity]:
        """
        Get a book by ID with full details.

        Args:
            book_id: The book ID as string

        Returns:
            Dictionary with book details including related entities, or None if not found
        """
        try:
            book_uuid = uuid.UUID(book_id)
        except ValueError:
            raise ValueError(f"Invalid book ID format: {book_id}")

        book_entity = self.book_repository.get_book_by_id(book_uuid)
        if not book_entity:
            return None

        return book_entity

    def get_all_books(self) -> List[BookEntity]:
        """
        Get all books with optional details.

        Args:
            include_details: Whether to include author, publisher, and genre details

        Returns:
            List of book dictionaries
        """
        return self.book_repository.get_all_books()

    # def get_books_by_author(self, author_id: str) -> List[Dict[str, Any]]:
    #     """
    #     Get all books by a specific author.

    #     Args:
    #         author_id: The author ID as string

    #     Returns:
    #         List of book dictionaries
    #     """
    #     try:
    #         author_uuid = uuid.UUID(author_id)
    #     except ValueError:
    #         raise ValueError(f"Invalid author ID format: {author_id}")

    #     # Verify author exists
    #     author = self.author_repository.get_author_entity_by_id(author_uuid)
    #     if not author:
    #         raise RuntimeError(f"Author with ID {author_id} not found")

    #     book_entities = self.book_repository.get_books_by_author(author_uuid)
    #     return [self._enrich_book_data(book) for book in book_entities]

    # def get_books_by_publisher(self, publisher_id: str) -> List[Dict[str, Any]]:
    #     """
    #     Get all books by a specific publisher.

    #     Args:
    #         publisher_id: The publisher ID as string

    #     Returns:
    #         List of book dictionaries
    #     """
    #     try:
    #         publisher_uuid = uuid.UUID(publisher_id)
    #     except ValueError:
    #         raise ValueError(f"Invalid publisher ID format: {publisher_id}")

    #     # Verify publisher exists
    #     publisher = self.publisher_repository.get_publisher_entity_by_id(publisher_uuid)
    #     if not publisher:
    #         raise RuntimeError(f"Publisher with ID {publisher_id} not found")

    #     book_entities = self.book_repository.get_books_by_publisher(publisher_uuid)
    #     return [self._enrich_book_data(book) for book in book_entities]

    # def search_books_by_title(self, title: str) -> List[Dict[str, Any]]:
    #     """
    #     Search books by title.

    #     Args:
    #         title: The title to search for

    #     Returns:
    #         List of matching book dictionaries
    #     """
    #     if not title or not title.strip():
    #         raise ValueError("Search title cannot be empty")

    #     book_entities = self.book_repository.search_books_by_title(title.strip())
    #     return [self._enrich_book_data(book) for book in book_entities]

    # def get_classic_books(self) -> List[Dict[str, Any]]:
    #     """
    #     Get all classic books (older than 50 years).

    #     Returns:
    #         List of classic book dictionaries
    #     """
    #     all_books = self.book_repository.get_all_books()
    #     classic_books = [book for book in all_books if book.is_classic()]
    #     return [self._enrich_book_data(book) for book in classic_books]

    # def get_books_by_genre(self, genre_id: str) -> List[Dict[str, Any]]:
    #     """
    #     Get all books in a specific genre.

    #     Args:
    #         genre_id: The genre ID as string

    #     Returns:
    #         List of book dictionaries
    #     """
    #     try:
    #         genre_uuid = uuid.UUID(genre_id)
    #     except ValueError:
    #         raise ValueError(f"Invalid genre ID format: {genre_id}")

    #     # Verify genre exists
    #     genre = self.genre_repository.get_genre_entity_by_id(genre_uuid)
    #     if not genre:
    #         raise RuntimeError(f"Genre with ID {genre_id} not found")

    #     all_books = self.book_repository.get_all_books()
    #     genre_books = [book for book in all_books if book.genre_id == genre_uuid]
    #     return [self._enrich_book_data(book) for book in genre_books]

    # def _enrich_book_data(self, book_entity: BookEntity) -> Dict[str, Any]:
    #     """
    #     Enrich book data with related entity information.

    #     Args:
    #         book_entity: The book entity to enrich

    #     Returns:
    #         Dictionary with enriched book data
    #     """
    #     book_data = book_entity.to_dict()

    #     # Add author details
    #     author = self.author_repository.get_author_entity_by_id(book_entity.author_id)
    #     if author:
    #         book_data["author"] = author.to_dict()

    #     # Add publisher details
    #     publisher = self.publisher_repository.get_publisher_entity_by_id(
    #         book_entity.publisher_id
    #     )
    #     if publisher:
    #         book_data["publisher"] = publisher.to_dict()

    #     # Add genre details
    #     genres = []
    #     if book_entity.genre_id:
    #         genre = self.genre_repository.get_genre_entity_by_id(book_entity.genre_id)
    #         if genre:
    #             genres.append(genre.to_dict())
    #     book_data["genres"] = genres

    #     return book_data
