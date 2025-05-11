from book.models.author import Author
from wireup import service


@service
class AuthorRepository:
    def __init__(self):
        self.author_model = Author

    def get_author_by_id(self, author_id):
        return self.author_model.objects.get(id=author_id)
