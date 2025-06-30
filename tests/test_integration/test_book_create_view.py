import uuid
from datetime import date
from decimal import Decimal

import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book.models.author import Author
from book.models.book import Book
from book.models.genre import Genre
from book.models.publisher import Publisher


@pytest.mark.django_db
class TestBookCreateViewIntegration(TestCase):
    """Integration tests for the book create view with real database."""

    def setUp(self):
        """Set up test data for each test."""
        self.client = APIClient()
        self.url = reverse("book_create_and_get")

        # Create test author
        self.author = Author.objects.create(
            name="Test Author", birth_date=date(1980, 1, 1), death_date=None
        )

        # Create test publisher
        self.publisher = Publisher.objects.create(
            name="Test Publisher", website="https://testpublisher.com"
        )

        # Create test genre
        self.genre = Genre.objects.create(name="Fiction")

        # Valid book data
        self.valid_book_data = {
            "title": "Test Book Title",
            "description": "A test book description for integration testing",
            "published_date": "2023-01-15",
            "isbn": "1234567890123",
            "author_id": str(self.author.id),
            "publisher_id": str(self.publisher.id),
            "genre_id": str(self.genre.id),
        }

    def test_create_book_success(self):
        """Test successful book creation through the API."""
        response = self.client.post(self.url, self.valid_book_data, format="json")

        # Assert response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertIn("id", response_data)
        self.assertEqual(response_data["title"], self.valid_book_data["title"])
        self.assertEqual(
            response_data["description"], self.valid_book_data["description"]
        )
        self.assertEqual(response_data["isbn"], self.valid_book_data["isbn"])
        self.assertEqual(response_data["author_id"], self.valid_book_data["author_id"])
        self.assertEqual(
            response_data["publisher_id"], self.valid_book_data["publisher_id"]
        )
        self.assertEqual(response_data["genre_id"], self.valid_book_data["genre_id"])

        # Assert database state
        book = Book.objects.get(id=response_data["id"])
        self.assertEqual(book.title, self.valid_book_data["title"])
        self.assertEqual(book.isbn, self.valid_book_data["isbn"])
        self.assertEqual(book.author.id, uuid.UUID(self.valid_book_data["author_id"]))
        self.assertEqual(
            book.publisher.id, uuid.UUID(self.valid_book_data["publisher_id"])
        )

        # Note: Genre relationship is handled through the use case, not directly on the Book model

    def test_create_book_missing_required_fields(self):
        """Test book creation with missing required fields."""
        incomplete_data = {
            "title": "Test Book",
            "description": "Test description",
            # Missing other required fields
        }

        response = self.client.post(self.url, incomplete_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_invalid_isbn_format(self):
        """Test book creation with invalid ISBN format."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["isbn"] = "invalid-isbn"

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_invalid_uuid_format(self):
        """Test book creation with invalid UUID format."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["author_id"] = "invalid-uuid"

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_nonexistent_author(self):
        """Test book creation with non-existent author ID."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["author_id"] = str(uuid.uuid4())

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_nonexistent_publisher(self):
        """Test book creation with non-existent publisher ID."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["publisher_id"] = str(uuid.uuid4())

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_nonexistent_genre(self):
        """Test book creation with non-existent genre ID."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["genre_id"] = str(uuid.uuid4())

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_duplicate_isbn(self):
        """Test book creation with duplicate ISBN."""
        # Create first book
        response1 = self.client.post(self.url, self.valid_book_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Try to create second book with same ISBN
        response2 = self.client.post(self.url, self.valid_book_data, format="json")

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response2.json()
        self.assertIn("error", response_data)
        self.assertIn("already exists", response_data["error"])

    def test_create_book_empty_title(self):
        """Test book creation with empty title."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["title"] = ""

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_title_too_long(self):
        """Test book creation with title exceeding max length."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["title"] = "A" * 101  # Exceeds max_length=100

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_description_too_long(self):
        """Test book creation with description exceeding max length."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["description"] = "A" * 256  # Exceeds max_length=255

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_invalid_date_format(self):
        """Test book creation with invalid date format."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["published_date"] = "invalid-date"

        response = self.client.post(self.url, invalid_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_create_book_future_date(self):
        """Test book creation with future published date."""
        invalid_data = self.valid_book_data.copy()
        invalid_data["published_date"] = "2030-01-01"

        response = self.client.post(self.url, invalid_data, format="json")

        # This should fail as future dates are not allowed
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertIn("future", response_data["error"])

    def test_get_method_not_implemented(self):
        """Test that GET method returns appropriate response."""
        response = self.client.get(self.url)

        # The view now returns a proper response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("message", response_data)

    def test_create_book_with_special_characters(self):
        """Test book creation with special characters in title and description."""
        special_data = self.valid_book_data.copy()
        special_data["title"] = "Test Book: The Sequel! (2023)"
        special_data["description"] = (
            "A book with special chars: @#$%^&*()_+-=[]{}|;':\",./<>?"
        )

        response = self.client.post(self.url, special_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data["title"], special_data["title"])
        self.assertEqual(response_data["description"], special_data["description"])

    def test_create_multiple_books_success(self):
        """Test creating multiple books successfully."""
        # Create second set of test data
        author2 = Author.objects.create(
            name="Second Author", birth_date=date(1990, 5, 15)
        )

        publisher2 = Publisher.objects.create(
            name="Second Publisher", website="https://secondpublisher.com"
        )

        genre2 = Genre.objects.create(name="Non-Fiction")

        book_data2 = {
            "title": "Second Test Book",
            "description": "Another test book description",
            "published_date": "2023-06-20",
            "isbn": "9876543210987",
            "author_id": str(author2.id),
            "publisher_id": str(publisher2.id),
            "genre_id": str(genre2.id),
        }

        # Create first book
        response1 = self.client.post(self.url, self.valid_book_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Create second book
        response2 = self.client.post(self.url, book_data2, format="json")
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Verify both books exist in database
        self.assertEqual(Book.objects.count(), 2)

        book1 = Book.objects.get(isbn=self.valid_book_data["isbn"])
        book2 = Book.objects.get(isbn=book_data2["isbn"])

        self.assertNotEqual(book1.id, book2.id)
        self.assertEqual(book1.title, self.valid_book_data["title"])
        self.assertEqual(book2.title, book_data2["title"])
