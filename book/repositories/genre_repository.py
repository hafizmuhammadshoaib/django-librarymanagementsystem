from book.models.genre import Genre


class GenreRepository:
    def __init__(self):
        self.genre = Genre

    def get_genre_by_id(self, genre_id):
        return self.genre.objects.get(id=genre_id)

    def add_genre(self, genre_name):
        self.genre.execute("INSERT INTO genres (name) VALUES (?)", (genre_name,))
        self.genre.commit()

    def update_genre(self, genre_id, genre_name):
        self.genre.execute(
            "UPDATE genres SET name = ? WHERE id = ?", (genre_name, genre_id)
        )
        self.genre.commit()

    def delete_genre(self, genre_id):
        self.genre.execute("DELETE FROM genres WHERE id = ?", (genre_id,))
        self.genre.commit()

    def add_genre_to_book(self, book, genre_id):
        genre = self.genre.objects.get(id=genre_id)  # Fetch Genre instance
        book.genres.add(genre)
