from dependency_injector import containers, providers

from book.container import BookContainer
from member.container import MemberContainer


class Container(containers.DeclarativeContainer):
    """Application container."""

    # Import configurations
    config = providers.Configuration()

    # Wire up sub-containers
    book_container = providers.Container(BookContainer)
    member_container = providers.Container(MemberContainer)


# Create global container instance
container = Container()

# Wire up cross-container dependencies
container.wire(
    modules=[
        "book.views.book_view",
        "member.views.member_view",
    ]
)

# Inject the book service into the member container
container.member_container.book_crud_service.override(
    container.book_container.book_service
)

# Book app services
