from django.urls import path
from book.views import book_view
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("", book_view.BookCreateAndGetView.as_view(), name="book_create_and_get"),
]

router = DefaultRouter()
urlpatterns += router.urls
