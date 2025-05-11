import pytest
from unittest.mock import Mock
from book.services.book_crud_service import BookCrudService


@pytest.fixture
def mock_dependencies():
    """Fixture providing mocked dependencies for BookCrudService"""
    return {
        "book_repository": Mock(),
        "genre_service": Mock(),
        "author_service": Mock(),
        "publisher_service": Mock(),
    }


@pytest.fixture
def book_service(mock_dependencies):
    """Fixture providing BookCrudService with mocked dependencies"""
    return BookCrudService(**mock_dependencies)


@pytest.fixture
def valid_book_data():
    """Sample valid book data"""
    return {
        "title": "Test Book",
        "description": "Test Description",
        "published_date": "2023-01-01",
        "isbn": "1234567890123",
        "author_id": 1,
        "publisher_id": 1,
        "genre_id": 1,
    }
