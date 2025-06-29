from abc import ABC, abstractmethod

from book.models.publisher import Publisher


class PublisherAbstractRepository(ABC):
    @abstractmethod
    def get_publisher_by_id(self, publisher_id):
        raise NotImplementedError("This method should be overridden.")


class PublisherRepository(PublisherAbstractRepository):
    def __init__(self):
        self.publisher_model = Publisher

    def get_publisher_by_id(self, publisher_id):
        return self.publisher_model.objects.get(id=publisher_id)
