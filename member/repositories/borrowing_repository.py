from abc import ABC, abstractmethod
from member.models.borrowing_history import BorrowingHistory
from wireup import abstract, service


@abstract
class BorrowingAbstractRepository(ABC):
    @abstractmethod
    def get_borrowings_by_member(self, member_id):
        raise NotImplementedError("This method should be overridden.")
    
    @abstractmethod
    def get_active_borrowings_by_member(self, member_id):
        raise NotImplementedError("This method should be overridden.")
    
    @abstractmethod
    def get_borrowing_count_by_member(self, member_id):
        raise NotImplementedError("This method should be overridden.")


@service
class BorrowingRepository(BorrowingAbstractRepository):
    def __init__(self):
        self.borrowing_model = BorrowingHistory

    def get_borrowings_by_member(self, member_id):
        return self.borrowing_model.objects.filter(member_id=member_id)
    
    def get_active_borrowings_by_member(self, member_id):
        return self.borrowing_model.objects.filter(
            member_id=member_id, 
            returning_date__isnull=True
        )
    
    def get_borrowing_count_by_member(self, member_id):
        return self.borrowing_model.objects.filter(member_id=member_id).count() 