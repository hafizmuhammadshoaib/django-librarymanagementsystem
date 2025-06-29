from wireup import create_sync_container
from book.container import book_services
from member.container import member_services

global_container = create_sync_container(
    services=[
        *book_services,
        *member_services,
    ]
)

# Book app services
