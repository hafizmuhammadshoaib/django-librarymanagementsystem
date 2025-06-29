from unittest.mock import Mock

import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError


class TestBookCrudService:
    @pytest.mark.django_db
    def test_create_book_success(
        self, book_service, mock_dependencies, valid_book_data
    ):
        """Test successful book creation"""
        # Setup mock returns
        mock_book = Mock()
        mock_dependencies["author_service"].get_author.return_value = Mock()
        mock_dependencies["publisher_service"].get_publisher.return_value = Mock()
        mock_dependencies["book_repository"].add_book.return_value = mock_book

        # Call method
        result = book_service.create_book(valid_book_data)

        # Assertions
        assert result == mock_book
        mock_dependencies["author_service"].get_author.assert_called_once_with(1)
        mock_dependencies["publisher_service"].get_publisher.assert_called_once_with(1)
        mock_dependencies["book_repository"].add_book.assert_called_once()
        mock_dependencies["genre_service"].add_genre_to_book.assert_called_once_with(
            mock_book, 1
        )

    @pytest.mark.django_db
    def test_create_book_missing_author(
        self, book_service, mock_dependencies, valid_book_data
    ):
        """Test validation error when author doesn't exist"""
        mock_dependencies["author_service"].get_author.side_effect = ObjectDoesNotExist(
            "Author not found"
        )

        with pytest.raises(ValidationError, match="Invalid ID: Author not found"):
            book_service.create_book(valid_book_data)

    @pytest.mark.django_db
    def test_create_book_transaction_rollback(
        self, book_service, mock_dependencies, valid_book_data
    ):
        """Test transaction rolls back on failure"""
        # Setup successful initial steps
        mock_book = Mock()
        mock_dependencies["author_service"].get_author.return_value = Mock()
        mock_dependencies["publisher_service"].get_publisher.return_value = Mock()
        mock_dependencies["book_repository"].add_book.return_value = mock_book

        # Make genre assignment fail
        mock_dependencies["genre_service"].add_genre_to_book.side_effect = Exception(
            "DB Error"
        )

        with pytest.raises(Exception, match="DB Error"):
            book_service.create_book(valid_book_data)

        # Verify book creation was attempted
        mock_dependencies["book_repository"].add_book.assert_called_once()

    def test_get_book(self, book_service, mock_dependencies):
        """Test retrieving a book"""
        mock_book = Mock()
        mock_dependencies["book_repository"].get.return_value = mock_book

        result = book_service.get_book(1)

        assert result == mock_book
        mock_dependencies["book_repository"].get.assert_called_once_with(1)

    # def test_update_book(self, book_service, mock_dependencies):
    #     """Test updating a book"""
    #     update_data = {"title": "New Title"}
    #     mock_dependencies["book_repository"].update.return_value = True

    #     result = book_service.update_book(1, update_data)

    #     assert result is True
    #     mock_dependencies["book_repository"].update.assert_called_once_with(
    #         1, update_data
    #     )

    # def test_delete_book(self, book_service, mock_dependencies):
    #     """Test deleting a book"""
    #     mock_dependencies["book_repository"].delete.return_value = True

    #     result = book_service.delete_book(1)

    #     assert result is True
    #     mock_dependencies["book_repository"].delete.assert_called_once_with(1)
