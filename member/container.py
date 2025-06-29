from member.repositories.borrowing_repository import (
    BorrowingAbstractRepository,
    BorrowingRepository,
)
from member.services.member_service import MemberService

member_services = [
    MemberService,
    BorrowingRepository,
    BorrowingAbstractRepository,
]
