from dependency_injector import containers, providers

from member.repositories.borrowing_repository import (
    BorrowingRepository,
)
from member.services.member_service import MemberService


class MemberContainer(containers.DeclarativeContainer):
    """Member app container."""

    # Repositories
    borrowing_repository = providers.Singleton(BorrowingRepository)

    # Services
    member_service = providers.Singleton(
        MemberService,
        borrowing_repository=borrowing_repository,
    )
