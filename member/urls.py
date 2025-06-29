from django.urls import path
from member.views.member_view import MemberBorrowingView, MemberActiveBooksView

urlpatterns = [
    path(
        "borrowing/<uuid:member_id>/",
        MemberBorrowingView.as_view(),
        name="member_borrowing",
    ),
    path(
        "active-books/<uuid:member_id>/",
        MemberActiveBooksView.as_view(),
        name="member_active_books",
    ),
]
