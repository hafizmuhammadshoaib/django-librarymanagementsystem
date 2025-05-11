from abc import ABC, abstractmethod
from book.models.genre import Genre
from wireup import abstract, service


@abstract
class GenreAbstractRepository(ABC):
    @abstractmethod
    def get_genre_by_id(self, genre_id):
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def add_genre_to_book(self, book, genre_id):
        raise NotImplementedError("This method should be overridden.")


@service
class GenreRepository(GenreAbstractRepository):
    def __init__(self):
        self.genre = Genre

    def get_genre_by_id(self, genre_id):
        return self.genre.objects.get(id=genre_id)

    def add_genre_to_book(self, book, genre_id):
        genre = self.genre.objects.get(id=genre_id)  # Fetch Genre instance
        book.genres.add(genre)
