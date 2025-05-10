from book.models.book import Book


class BookRepository:
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

    def get_books(self):
        return self.books

    def find_book_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def remove_book(self, title):
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            return True
        return False
