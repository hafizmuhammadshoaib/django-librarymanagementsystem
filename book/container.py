from wireup import create_sync_container

from book.repositories.author_repository import AuthorRepository
from book.repositories.book_repository import BookRepository
from book.repositories.genre_repository import GenreRepository
from book.repositories.publisher_repository import PublisherRepository
from book.services.author_crud_service import AuthorCRUDService
from book.services.book_crud_service import BookCrudService
from book.services.genre_service import GenreService
from book.services.publisher_crud_service import PublisherCRUDService

container = create_sync_container(
    services=[
        PublisherCRUDService,
        AuthorCRUDService,
        GenreService,
        BookCrudService,
        BookRepository,
        GenreRepository,
        AuthorRepository,
        PublisherRepository,
    ],
)
