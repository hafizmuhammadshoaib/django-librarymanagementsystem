from dependency_injector import containers, providers

from book.repositories.author_repository import AuthorRepository
from book.repositories.book_repository import BookRepository
from book.repositories.genre_repository import GenreRepository
from book.repositories.publisher_repository import PublisherRepository
from book.services.author_crud_service import AuthorCRUDService
from book.services.book_crud_service import BookCrudService
from book.services.genre_service import GenreService
from book.services.publisher_crud_service import PublisherCRUDService
from book.use_cases.create_book_use_case import CreateBookUseCase
from book.use_cases.get_book_use_case import GetBookUseCase


class BookContainer(containers.DeclarativeContainer):
    """Book app container."""

    # Repositories
    author_repository = providers.Singleton(AuthorRepository)
    book_repository = providers.Singleton(BookRepository)
    genre_repository = providers.Singleton(GenreRepository)
    publisher_repository = providers.Singleton(PublisherRepository)

    # Use Cases
    create_book_use_case = providers.Singleton(
        CreateBookUseCase,
        book_repository=book_repository,
        author_repository=author_repository,
        publisher_repository=publisher_repository,
        genre_repository=genre_repository,
    )

    get_book_use_case = providers.Singleton(
        GetBookUseCase,
        book_repository=book_repository,
        author_repository=author_repository,
        publisher_repository=publisher_repository,
        genre_repository=genre_repository,
    )

    # Services
    author_service = providers.Singleton(
        AuthorCRUDService,
        author_repository=author_repository,
    )

    genre_service = providers.Singleton(
        GenreService,
        genre_repository=genre_repository,
    )

    publisher_service = providers.Singleton(
        PublisherCRUDService,
        publisher_repository=publisher_repository,
    )

    book_service = providers.Singleton(
        BookCrudService,
        create_book_use_case=create_book_use_case,
        get_book_use_case=get_book_use_case,
    )
