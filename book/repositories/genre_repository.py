from book.models.genre import Genre
from wireup import service


@service
class GenreRepository:
    def __init__(self):
        self.genre = Genre

    def get_genre_by_id(self, genre_id):
        return self.genre.objects.get(id=genre_id)

    def add_genre_to_book(self, book, genre_id):
        genre = self.genre.objects.get(id=genre_id)  # Fetch Genre instance
        book.genres.add(genre)
