from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from librarymanagementsystem.container import container
from member.serializers import (
    MemberActiveBooksResponseSerializer,
    MemberBorrowingResponseSerializer,
)
from member.services.member_service import MemberService


class MemberBorrowingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, member_id):
        """Get member's borrowing statistics and book list"""
        try:
            # Use the container to get member service
            member_service: MemberService = container.member_container.member_service()

            # Get borrowing statistics
            stats = member_service.get_member_borrowing_stats(member_id)

            # Get borrowed books list
            borrowed_books = member_service.get_member_borrowed_books(member_id)

            # Create and validate the response using serializer
            serializer = MemberBorrowingResponseSerializer.create_response(
                member_id, stats, borrowed_books
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to get member borrowing info: {e!s}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MemberActiveBooksView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, member_id):
        """Get member's currently active book borrowings"""
        try:
            # Use the container to get member service
            member_service: MemberService = container.member_container.member_service()

            active_books = member_service.get_member_active_books(member_id)

            # Create and validate the response using serializer
            serializer = MemberActiveBooksResponseSerializer.create_response(
                member_id, active_books
            )

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to get member active books: {e!s}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
