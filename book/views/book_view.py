from typing import Any, Dict

from django.forms import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from book.serializes.book_create_serializer import BookCreateSerializer
from book.services.book_crud_service import BookCrudService
from librarymanagementsystem.container import container


class BookCreateAndGetView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pass

    def post(self, request):
        # Logic to handle POST request for creating a book
        try:
            book_create_serializer = BookCreateSerializer(data=request.data)
            book_create_serializer.is_valid(raise_exception=True)
            book_service: BookCrudService = container.book_container.book_service()
            created_book = book_service.create_book(
                book_create_serializer.validated_data  # type: ignore
            )
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        return Response(
            {
                "id": created_book.id,
                "title": created_book.title,
                "description": created_book.description,
                "published_date": created_book.published_date,
                "isbn": created_book.isbn,
                "author_id": created_book.author_id,
                "publisher_id": created_book.publisher_id,
                "genre_id": created_book.genre_id,
            },
            status=201,
        )
