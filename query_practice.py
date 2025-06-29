import uuid
from datetime import date, timedelta

from django.db.models import Count

from book.models import Author, Book, Genre, Publisher
from member.models import BorrowingHistory

# Fetch all books written by a specific author.
author_id = uuid.UUID("45b8609c-6c66-43be-bc5c-c0086dd5d595")
books_by_author = (
    Book.objects.filter(author_id=author_id)
    .select_related("author")
    .select_related("publisher")
)
for book in books_by_author:
    print(book.author.name)
    print(book.publisher.name)

# Get all genres associated with a particular book.
book_id = uuid.UUID("0ba64846-a4bc-4998-a3bb-38923bbbe57c")

book = Book.objects.filter(id=book_id).prefetch_related("genres").first()
if book:
    for genre in book.genres.all():
        print(genre.name)

# Find all books published by a specific publisher.
publisher_id = uuid.UUID("27afbd41-8a6b-449e-9f0b-8a5ab4b86e99")
books = Book.objects.filter(publisher_id=publisher_id).select_related("publisher")
for book in books:
    print(f"{book.publisher.name}, {book.title}")


# Retrieve all members who borrowed a specific book.
book_id = uuid.UUID("042340e3-a290-46c1-8e9a-10869560e6d1")
borrowing_histories = BorrowingHistory.objects.filter(book=book_id).select_related(
    "member"
)
for borrowing_history in borrowing_histories:
    print(
        f"member name {borrowing_history.member.first_name} {borrowing_history.member.last_name}"
    )

# List all books borrowed by a member in the last 30 days.
current_date = date.today()
last_30_days_date = current_date - timedelta(30)

borrowing_histories = (
    BorrowingHistory.objects.filter(
        borrowing_date__gte=last_30_days_date,
        borrowing_date__lte=current_date,
    )
    .select_related("member")
    .select_related("book")
    .exclude(returning_date__isnull=False)
)
# optimized version
borrowing_histories = (
    BorrowingHistory.objects.filter(
        borrowing_date__range=(last_30_days_date, current_date),
        returning_date__isnull=True,  # Only include unreturned books
    )
    .select_related("member", "book")  # Optimize database queries
    .order_by("-borrowing_date")  # Optional: Order by borrowing date (newest first)
)
for borrowing_history in borrowing_histories:
    print(
        f"borrowing history id {borrowing_history.id} member {borrowing_history.member.first_name} book {borrowing_history.book.title}"
    )

# Find authors who have written books in a specific genre.
genre_id = uuid.UUID("a887f76a-9e13-479d-a95c-ea279f75bc81")

genres = Genre.objects.filter(id=genre_id).prefetch_related("books")
for genre in genres:
    books = genre.books.all().select_related("author")
    for book in books:
        book_author = book.author
        print(f"genre {genre.name} book {book.title} author {book_author.name}")

# Get the most popular genre based on the number of books.
genre = Genre.objects.annotate(count=Count("books")).order_by("-count").first()
print(genre.name)

# Find all books that are currently borrowed (not yet returned).

borrowing_histories = BorrowingHistory.objects.filter(
    returning_date__isnull=True
).select_related("book")
for borrowing_history in borrowing_histories:
    print(
        f"book name{borrowing_history.book.title} book id {borrowing_history.book.id}"
    )


# Retrieve the publisher with the most published books.
publisher = Publisher.objects.annotate(count=Count("book")).order_by("-count").first()

if publisher:
    print(f"{publisher.name} {publisher.count}")


# List all authors who have not written any books yet.
authors_without_books = Author.objects.exclude(book__isnull=False)

authors_without_books = Author.objects.filter(book__isnull=True)
for author in authors_without_books:
    print(author.name)


authors_without_books = Author.objects.exclude(book__isnull=False)
for author in authors_without_books:
    print(author.name)
