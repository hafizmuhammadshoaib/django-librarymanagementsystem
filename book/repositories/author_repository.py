from abc import ABC, abstractmethod
from book.models.author import Author
from wireup import service, abstract


@abstract
class AuthorAbstractRepository(ABC):
    @abstractmethod
    def get_author_by_id(self, author_id):
        raise NotImplementedError("This method should be overridden.")


@service
class AuthorRepository(AuthorAbstractRepository):
    def __init__(self):
        self.author_model = Author

    def get_author_by_id(self, author_id):
        return self.author_model.objects.get(id=author_id)
