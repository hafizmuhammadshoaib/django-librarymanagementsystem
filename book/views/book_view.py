from typing import Any, Dict

from django.forms import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from book.serializes import (
    BookCreateSerializer,
    BookResponseSerializer,
    EnrichedBookResponseSerializer,
)
from book.services.book_crud_service import BookCrudService
from librarymanagementsystem.container import container


class BookCreateAndGetView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, book_id=None):
        """
        GET method to retrieve books.

        Args:
            request: The HTTP request
            book_id: Optional book ID from URL parameter

        Returns:
            - If book_id provided: Single book with enriched data
            - If no book_id: List of all books
        """
        try:
            book_service: BookCrudService = container.book_container.book_service()

            if book_id is not None:
                # Get specific book by ID
                try:
                    book_data = book_service.get_book_by_id(str(book_id))
                except (ValueError, serializers.ValidationError) as ve:
                    # Handle invalid UUID or validation error
                    return Response({"error": str(ve)}, status=400)
                if not book_data:
                    return Response(
                        {"error": f"Book with ID {book_id} not found"}, status=404
                    )

                # Serialize enriched book data
                response_serializer = EnrichedBookResponseSerializer(book_data)
                return Response(response_serializer.data, status=200)
            else:
                # Get all books (no validation or ISBN required)
                books_data = book_service.get_all_books()

                # Serialize list of enriched book data
                response_serializer = EnrichedBookResponseSerializer(
                    books_data, many=True
                )
                return Response(response_serializer.data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        # Logic to handle POST request for creating a book
        try:
            book_create_serializer = BookCreateSerializer(data=request.data)
            book_create_serializer.is_valid(raise_exception=True)
            book_service: BookCrudService = container.book_container.book_service()
            created_book = book_service.create_book(
                book_create_serializer.validated_data  # type: ignore
            )
        except (
            DjangoValidationError,
            serializers.ValidationError,
            ValueError,
        ) as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        # Serialize the response using BookResponseSerializer
        response_serializer = BookResponseSerializer(created_book.to_dict())
        return Response(response_serializer.data, status=201)
