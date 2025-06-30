import uuid
from unittest.mock import Mock

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from book.entities.book_entity import BookEntity


class TestBookCrudService:
    @pytest.mark.django_db
    def test_create_book_success(
        self, book_service, mock_dependencies, valid_book_data
    ):
        """Test successful book creation"""
        # Setup mock returns
        mock_book_entity = Mock(spec=BookEntity)
        mock_dependencies[
            "create_book_use_case"
        ].execute.return_value = mock_book_entity

        # Call method
        result = book_service.create_book(valid_book_data)

        # Assertions
        assert result == mock_book_entity
        mock_dependencies["create_book_use_case"].execute.assert_called_once_with(
            valid_book_data
        )

    @pytest.mark.django_db
    def test_create_book_validation_error(
        self, book_service, mock_dependencies, valid_book_data
    ):
        """Test validation error during book creation"""
        mock_dependencies["create_book_use_case"].execute.side_effect = ValueError(
            "Invalid data"
        )

        with pytest.raises(ValidationError, match="Invalid data"):
            book_service.create_book(valid_book_data)

    @pytest.mark.django_db
    def test_create_book_runtime_error(
        self, book_service, mock_dependencies, valid_book_data
    ):
        """Test runtime error during book creation"""
        mock_dependencies["create_book_use_case"].execute.side_effect = RuntimeError(
            "Author not found"
        )

        with pytest.raises(ValidationError, match="Author not found"):
            book_service.create_book(valid_book_data)

    def test_get_book_by_id_success(self, book_service, mock_dependencies):
        """Test successful book retrieval by ID"""
        book_id = str(uuid.uuid4())
        expected_book_data = {
            "id": book_id,
            "title": "Test Book",
            "author": {"name": "Test Author"},
            "publisher": {"name": "Test Publisher"},
        }
        mock_dependencies[
            "get_book_use_case"
        ].get_book_by_id.return_value = expected_book_data

        result = book_service.get_book_by_id(book_id)

        assert result == expected_book_data
        mock_dependencies["get_book_use_case"].get_book_by_id.assert_called_once_with(
            book_id
        )

    def test_get_book_by_id_not_found(self, book_service, mock_dependencies):
        """Test book retrieval when book doesn't exist"""
        book_id = str(uuid.uuid4())
        mock_dependencies["get_book_use_case"].get_book_by_id.return_value = None

        result = book_service.get_book_by_id(book_id)

        assert result is None
        mock_dependencies["get_book_use_case"].get_book_by_id.assert_called_once_with(
            book_id
        )

    def test_get_book_by_id_invalid_format(self, book_service, mock_dependencies):
        """Test book retrieval with invalid ID format"""
        invalid_book_id = "invalid-uuid"
        mock_dependencies["get_book_use_case"].get_book_by_id.side_effect = ValueError(
            "Invalid book ID format"
        )

        with pytest.raises(ValidationError, match="Invalid book ID format"):
            book_service.get_book_by_id(invalid_book_id)

    def test_get_all_books_with_details(self, book_service, mock_dependencies):
        """Test getting all books with details"""
        expected_books = [
            {"id": "1", "title": "Book 1", "author": {"name": "Author 1"}},
            {"id": "2", "title": "Book 2", "author": {"name": "Author 2"}},
        ]
        mock_dependencies[
            "get_book_use_case"
        ].get_all_books.return_value = expected_books

        result = book_service.get_all_books(include_details=True)

        assert result == expected_books
        mock_dependencies["get_book_use_case"].get_all_books.assert_called_once_with(
            True
        )

    def test_get_all_books_without_details(self, book_service, mock_dependencies):
        """Test getting all books without details"""
        expected_books = [
            {"id": "1", "title": "Book 1"},
            {"id": "2", "title": "Book 2"},
        ]
        mock_dependencies[
            "get_book_use_case"
        ].get_all_books.return_value = expected_books

        result = book_service.get_all_books(include_details=False)

        assert result == expected_books
        mock_dependencies["get_book_use_case"].get_all_books.assert_called_once_with(
            False
        )

    def test_get_books_by_author_success(self, book_service, mock_dependencies):
        """Test getting books by author successfully"""
        author_id = str(uuid.uuid4())
        expected_books = [
            {"id": "1", "title": "Book 1", "author": {"name": "Author 1"}}
        ]
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_author.return_value = expected_books

        result = book_service.get_books_by_author(author_id)

        assert result == expected_books
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_author.assert_called_once_with(author_id)

    def test_get_books_by_author_invalid_id(self, book_service, mock_dependencies):
        """Test getting books by author with invalid ID"""
        invalid_author_id = "invalid-uuid"
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_author.side_effect = ValueError("Invalid author ID format")

        with pytest.raises(ValidationError, match="Invalid author ID format"):
            book_service.get_books_by_author(invalid_author_id)

    def test_get_books_by_author_not_found(self, book_service, mock_dependencies):
        """Test getting books by author when author doesn't exist"""
        author_id = str(uuid.uuid4())
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_author.side_effect = RuntimeError("Author not found")

        with pytest.raises(ValidationError, match="Author not found"):
            book_service.get_books_by_author(author_id)

    def test_get_books_by_publisher_success(self, book_service, mock_dependencies):
        """Test getting books by publisher successfully"""
        publisher_id = str(uuid.uuid4())
        expected_books = [
            {"id": "1", "title": "Book 1", "publisher": {"name": "Publisher 1"}}
        ]
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_publisher.return_value = expected_books

        result = book_service.get_books_by_publisher(publisher_id)

        assert result == expected_books
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_publisher.assert_called_once_with(publisher_id)

    def test_get_books_by_publisher_invalid_id(self, book_service, mock_dependencies):
        """Test getting books by publisher with invalid ID"""
        invalid_publisher_id = "invalid-uuid"
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_publisher.side_effect = ValueError("Invalid publisher ID format")

        with pytest.raises(ValidationError, match="Invalid publisher ID format"):
            book_service.get_books_by_publisher(invalid_publisher_id)

    def test_get_books_by_publisher_not_found(self, book_service, mock_dependencies):
        """Test getting books by publisher when publisher doesn't exist"""
        publisher_id = str(uuid.uuid4())
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_publisher.side_effect = RuntimeError("Publisher not found")

        with pytest.raises(ValidationError, match="Publisher not found"):
            book_service.get_books_by_publisher(publisher_id)

    def test_search_books_by_title_success(self, book_service, mock_dependencies):
        """Test searching books by title successfully"""
        search_title = "Python"
        expected_books = [
            {"id": "1", "title": "Python Programming", "author": {"name": "Author 1"}}
        ]
        mock_dependencies[
            "get_book_use_case"
        ].search_books_by_title.return_value = expected_books

        result = book_service.search_books_by_title(search_title)

        assert result == expected_books
        mock_dependencies[
            "get_book_use_case"
        ].search_books_by_title.assert_called_once_with(search_title)

    def test_search_books_by_title_empty_title(self, book_service, mock_dependencies):
        """Test searching books with empty title"""
        empty_title = ""
        mock_dependencies[
            "get_book_use_case"
        ].search_books_by_title.side_effect = ValueError("Search title cannot be empty")

        with pytest.raises(ValidationError, match="Search title cannot be empty"):
            book_service.search_books_by_title(empty_title)

    def test_get_classic_books(self, book_service, mock_dependencies):
        """Test getting classic books"""
        expected_books = [
            {"id": "1", "title": "Classic Book 1", "published_date": "1950-01-01"},
            {"id": "2", "title": "Classic Book 2", "published_date": "1960-01-01"},
        ]
        mock_dependencies[
            "get_book_use_case"
        ].get_classic_books.return_value = expected_books

        result = book_service.get_classic_books()

        assert result == expected_books
        mock_dependencies["get_book_use_case"].get_classic_books.assert_called_once()

    def test_get_books_by_genre_success(self, book_service, mock_dependencies):
        """Test getting books by genre successfully"""
        genre_id = str(uuid.uuid4())
        expected_books = [{"id": "1", "title": "Book 1", "genre": {"name": "Fiction"}}]
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_genre.return_value = expected_books

        result = book_service.get_books_by_genre(genre_id)

        assert result == expected_books
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_genre.assert_called_once_with(genre_id)

    def test_get_books_by_genre_invalid_id(self, book_service, mock_dependencies):
        """Test getting books by genre with invalid ID"""
        invalid_genre_id = "invalid-uuid"
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_genre.side_effect = ValueError("Invalid genre ID format")

        with pytest.raises(ValidationError, match="Invalid genre ID format"):
            book_service.get_books_by_genre(invalid_genre_id)

    def test_get_books_by_genre_not_found(self, book_service, mock_dependencies):
        """Test getting books by genre when genre doesn't exist"""
        genre_id = str(uuid.uuid4())
        mock_dependencies[
            "get_book_use_case"
        ].get_books_by_genre.side_effect = RuntimeError("Genre not found")

        with pytest.raises(ValidationError, match="Genre not found"):
            book_service.get_books_by_genre(genre_id)
