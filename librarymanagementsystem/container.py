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

# Book app services
