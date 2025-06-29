from book.repositories.author_repository import AuthorAbstractRepository


class AuthorCRUDService:
    def __init__(self, author_repository: AuthorAbstractRepository):
        self.author_repository = author_repository

    def get_author(self, author_id):
        return self.author_repository.get_author_by_id(author_id)
