from unittest.mock import Mock

import pytest

from book.services.book_crud_service import BookCrudService


@pytest.fixture
def mock_dependencies():
    """Fixture providing mocked dependencies for BookCrudService"""
    return {
        "create_book_use_case": Mock(),
        "get_book_use_case": Mock(),
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
