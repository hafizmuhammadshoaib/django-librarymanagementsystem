from abc import ABC, abstractmethod

from book.models.author import Author


class AuthorAbstractRepository(ABC):
    @abstractmethod
    def get_author_by_id(self, author_id):
        raise NotImplementedError("This method should be overridden.")


class AuthorRepository(AuthorAbstractRepository):
    def __init__(self):
        self.author_model = Author

    def get_author_by_id(self, author_id):
        return self.author_model.objects.get(id=author_id)
