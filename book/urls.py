from django.urls import path
from rest_framework.routers import DefaultRouter

from book.views import book_view

urlpatterns = [
    path("", book_view.BookCreateAndGetView.as_view(), name="book_create_and_get"),
    path(
        "<uuid:book_id>/",
        book_view.BookCreateAndGetView.as_view(),
        name="book_get_by_id",
    ),
]

router = DefaultRouter()
urlpatterns += router.urls
