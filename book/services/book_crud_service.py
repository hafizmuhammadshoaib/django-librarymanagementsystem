from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.forms import ValidationError

from book.repositories.book_repository import BookAbstractRepository
from book.services.author_crud_service import AuthorCRUDService
from book.services.genre_service import GenreService
from book.services.publisher_crud_service import PublisherCRUDService


class BookCrudService:
    def __init__(
        self,
        book_repository: BookAbstractRepository,
        genre_service: GenreService,
        author_service: AuthorCRUDService,
        publisher_service: PublisherCRUDService,
    ):
        self.book_repository = book_repository
        self.genre_service = genre_service
        self.author_service = author_service
        self.publisher_service = publisher_service

    def create_book(self, book_data):
        try:
            with transaction.atomic():  # Start transaction
                author = self.author_service.get_author(book_data["author_id"])
                publisher = self.publisher_service.get_publisher(
                    book_data["publisher_id"]
                )

                book = self.book_repository.add_book(
                    {
                        "title": book_data["title"],
                        "description": book_data["description"],
                        "published_date": book_data["published_date"],
                        "isbn": book_data["isbn"],
                        "author": author,
                        "publisher": publisher,
                    }
                )

                self.genre_service.add_genre_to_book(book, book_data["genre_id"])
                return book

        except ObjectDoesNotExist as e:
            raise ValidationError(f"Invalid ID: {e!s}")
