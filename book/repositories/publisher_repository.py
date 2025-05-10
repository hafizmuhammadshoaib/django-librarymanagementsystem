from book.models.publisher import Publisher


class PublisherRepository:
    def __init__(self):
        self.publisher_model = Publisher

    def get_publisher_by_id(self, publisher_id):
        return self.publisher_model.objects.get(id=publisher_id)
