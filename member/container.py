from dependency_injector import containers, providers

from member.repositories.borrowing_repository import BorrowingRepository
from member.repositories.member_repository import MemberRepository
from member.services.member_service import MemberService
from member.use_cases.borrow_book_use_case import BorrowBookUseCase


class MemberContainer(containers.DeclarativeContainer):
    """Member app container."""

    # Repositories
    borrowing_repository = providers.Singleton(BorrowingRepository)
    member_repository = providers.Singleton(MemberRepository)

    # Book repository will be injected from the main container
    book_repository = providers.Dependency()

    # Use Cases
    borrow_book_use_case = providers.Singleton(
        BorrowBookUseCase,
        member_repository=member_repository,
        borrowing_repository=borrowing_repository,
        book_repository=book_repository,
    )

    # Services
    member_service = providers.Singleton(
        MemberService,
        borrowing_repository=borrowing_repository,
        member_repository=member_repository,
        borrow_book_use_case=borrow_book_use_case,
    )
