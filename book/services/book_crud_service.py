from typing import Any, Dict, List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.forms import ValidationError

from book.entities.book_entity import BookEntity
from book.use_cases.create_book_use_case import CreateBookUseCase
from book.use_cases.get_book_use_case import GetBookUseCase


class BookCrudService:
    def __init__(
        self,
        create_book_use_case: CreateBookUseCase,
        get_book_use_case: GetBookUseCase,
    ):
        self.create_book_use_case = create_book_use_case
        self.get_book_use_case = get_book_use_case

    def create_book(self, book_data: Dict[str, Any]) -> BookEntity:
        """
        Create a new book using the CreateBookUseCase.

        Args:
            book_data: Dictionary containing book information

        Returns:
            BookEntity: The created book entity

        Raises:
            ValidationError: If validation fails
            RuntimeError: If required entities don't exist
        """
        try:
            return self.create_book_use_case.execute(book_data)
        except (ValueError, RuntimeError) as e:
            raise ValidationError(e)

    def get_book_by_id(self, book_id: str) -> Optional[BookEntity]:
        """
        Get a book by ID using the GetBookUseCase.

        Args:
            book_id: The book ID as string

        Returns:
            Dictionary with book details including related entities, or None if not found
        """
        try:
            return self.get_book_use_case.get_book_by_id(book_id)
        except ValueError as e:
            raise ValidationError(str(e))

    def get_all_books(self) -> List[BookEntity]:
        """
        Get all books using the GetBookUseCase.

        Args:
            include_details: Whether to include author, publisher, and genre details

        Returns:
            List of book dictionaries
        """
        return self.get_book_use_case.get_all_books()

    # def get_books_by_author(self, author_id: str) -> List[Dict[str, Any]]:
    #     """
    #     Get all books by a specific author using the GetBookUseCase.

    #     Args:
    #         author_id: The author ID as string

    #     Returns:
    #         List of book dictionaries
    #     """
    #     try:
    #         return self.get_book_use_case.get_books_by_author(author_id)
    #     except (ValueError, RuntimeError) as e:
    #         raise ValidationError(str(e))

    # def get_books_by_publisher(self, publisher_id: str) -> List[Dict[str, Any]]:
    #     """
    #     Get all books by a specific publisher using the GetBookUseCase.

    #     Args:
    #         publisher_id: The publisher ID as string

    #     Returns:
    #         List of book dictionaries
    #     """
    #     try:
    #         return self.get_book_use_case.get_books_by_publisher(publisher_id)
    #     except (ValueError, RuntimeError) as e:
    #         raise ValidationError(str(e))

    # def search_books_by_title(self, title: str) -> List[Dict[str, Any]]:
    #     """
    #     Search books by title using the GetBookUseCase.

    #     Args:
    #         title: The title to search for

    #     Returns:
    #         List of matching book dictionaries
    #     """
    #     try:
    #         return self.get_book_use_case.search_books_by_title(title)
    #     except ValueError as e:
    #         raise ValidationError(str(e))

    # def get_classic_books(self) -> List[Dict[str, Any]]:
    #     """
    #     Get all classic books using the GetBookUseCase.

    #     Returns:
    #         List of classic book dictionaries
    #     """
    #     return self.get_book_use_case.get_classic_books()

    # def get_books_by_genre(self, genre_id: str) -> List[Dict[str, Any]]:
    #     """
    #     Get all books in a specific genre using the GetBookUseCase.

    #     Args:
    #         genre_id: The genre ID as string

    #     Returns:
    #         List of book dictionaries
    #     """
    #     try:
    #         return self.get_book_use_case.get_books_by_genre(genre_id)
    #     except (ValueError, RuntimeError) as e:
    #         raise ValidationError(str(e))
