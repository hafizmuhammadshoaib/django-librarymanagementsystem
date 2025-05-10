from book.repositories.publisher_repository import PublisherRepository


class PublisherCRUDService:
    def __init__(self, publisher_repository: PublisherRepository):
        self.publisher_repository = publisher_repository

    def get_publisher(self, publisher_id):
        return self.publisher_repository.get_publisher_by_id(publisher_id)
