from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from book.models import author, genre, publisher
from book.repositories.author_repository import AuthorRepository
from book.repositories.book_repository import BookRepository
from book.repositories.genre_repository import GenreRepository
from book.repositories.publisher_repository import PublisherRepository
from book.serializes import book_create_serializer
from book.serializes.book_create_serializer import BookCreateSerializer
from book.services.author_crud_service import AuthorCRUDService
from book.services.book_crud_service import BookCrudService
from rest_framework.permissions import AllowAny

from book.services.genre_service import GenreService
from book.services.publisher_crud_service import PublisherCRUDService


class BookCreateAndGetView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pass

    def post(self, request):
        # Logic to handle POST request for creating a book
        try:
            book_create_serializer = BookCreateSerializer(data=request.data)
            book_create_serializer.is_valid(raise_exception=True)
            # Assuming the serializer is valid, we can proceed to create the book
            book_repo = BookRepository()
            genre_repo = GenreRepository()
            author_repo = AuthorRepository()
            publisher_repo = PublisherRepository()
            genre_service = GenreService(genre_repository=genre_repo)
            author_service = AuthorCRUDService(author_repository=author_repo)
            publisher_service = PublisherCRUDService(
                publisher_repository=publisher_repo
            )
            book_service = BookCrudService(
                book_repository=book_repo,
                genre_service=genre_service,
                author_service=author_service,
                publisher_service=publisher_service,
            )
            book_service.create_book(book_create_serializer.validated_data)
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        return Response({"message": "Book created successfully"}, status=201)
