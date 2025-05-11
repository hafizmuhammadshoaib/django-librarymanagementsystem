from abc import ABC, abstractmethod
from book.models.book import Book
from wireup import abstract, service




@abstract
class BookAbstractRepository(ABC):
    @abstractmethod
    def add_book(self, book_data):
        raise NotImplementedError("This method should be overridden.")


@service
class BookRepository(BookAbstractRepository):
    def __init__(self):
        self.book_model = Book

    def add_book(self, book_data):
        return self.book_model.objects.create(
            title=book_data["title"],
            description=book_data["description"],
            published_date=book_data["published_date"],
            isbn=book_data["isbn"],
            author=book_data["author"],  # Author instance (not author_id)
            publisher=book_data["publisher"],  # Publisher instance (not publisher_id)
        )
