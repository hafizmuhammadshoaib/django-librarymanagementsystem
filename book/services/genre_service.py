from book.repositories.genre_repository import GenreAbstractRepository


class GenreService:
    def __init__(self, genre_repository: GenreAbstractRepository):
        self.genre_repository = genre_repository

    def get_genre(self, genre_id):
        return self.genre_repository.get_genre_by_id(genre_id)

    def add_genre_to_book(self, book, genre_id):
        return self.genre_repository.add_genre_to_book(book, genre_id)
