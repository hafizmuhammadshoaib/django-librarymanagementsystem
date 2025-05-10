import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from book.models import Author, Publisher, Book, Genre
from member.models import Member, BorrowingHistory

# Clear existing data (optional, for a clean start)
Author.objects.all().delete()
Publisher.objects.all().delete()
Book.objects.all().delete()
Genre.objects.all().delete()
Member.objects.all().delete()
BorrowingHistory.objects.all().delete()

# Create Authors
author1 = Author.objects.create(
    id=uuid.uuid4(), name="J.K. Rowling", birth_date=datetime(1965, 7, 31).date()
)

author2 = Author.objects.create(
    id=uuid.uuid4(), name="George R.R. Martin", birth_date=datetime(1948, 9, 20).date()
)

author3 = Author.objects.create(
    id=uuid.uuid4(),
    name="Agatha Christie",
    birth_date=datetime(1890, 9, 15).date(),
    death_date=datetime(1976, 1, 12).date(),
)

author4 = Author.objects.create(
    id=uuid.uuid4(),
    name="Haruki Murakami",
    birth_date=datetime(1949, 1, 12).date(),
)

# Create Publishers
publisher1 = Publisher.objects.create(
    id=uuid.uuid4(), name="Bloomsbury Publishing", website="https://www.bloomsbury.com"
)

publisher2 = Publisher.objects.create(
    id=uuid.uuid4(), name="Bantam Books", website="https://www.bantambooks.com"
)

publisher3 = Publisher.objects.create(
    id=uuid.uuid4(), name="HarperCollins", website="https://www.harpercollins.com"
)

# Create Genres
genre1 = Genre.objects.create(id=uuid.uuid4(), name="Fantasy")

genre2 = Genre.objects.create(id=uuid.uuid4(), name="Mystery")

genre3 = Genre.objects.create(id=uuid.uuid4(), name="Thriller")

# Create Books
book1 = Book.objects.create(
    id=uuid.uuid4(),
    title="Harry Potter and the Philosopher's Stone",
    description="The first book in the Harry Potter series.",
    published_date=datetime(1997, 6, 26).date(),
    isbn="9780747532699",
    author=author1,
    publisher=publisher1,
)

book2 = Book.objects.create(
    id=uuid.uuid4(),
    title="A Game of Thrones",
    description="The first book in the A Song of Ice and Fire series.",
    published_date=datetime(1996, 8, 1).date(),
    isbn="9780553103540",
    author=author2,
    publisher=publisher2,
)

book3 = Book.objects.create(
    id=uuid.uuid4(),
    title="Murder on the Orient Express",
    description="A classic mystery novel by Agatha Christie.",
    published_date=datetime(1934, 1, 1).date(),
    isbn="9780062073495",
    author=author3,
    publisher=publisher3,
)

book4 = Book.objects.create(
    id=uuid.uuid4(),
    title="Some random book",
    description="some description",
    published_date=datetime(1935, 1, 1).date(),
    isbn="9780062073492",
    author=author3,
    publisher=publisher3,
)

# Associate Books with Genres
book1.genres.add(genre1)
book2.genres.add(genre1)
book3.genres.add(genre2)
book4.genres.add(genre3)

# Create Members
member1 = Member.objects.create(
    id=uuid.uuid4(),
    first_name="John",
    last_name="Doe",
    birth_date=datetime(1990, 5, 15).date(),
)

member2 = Member.objects.create(
    id=uuid.uuid4(),
    first_name="Jane",
    last_name="Smith",
    birth_date=datetime(1985, 10, 20).date(),
)

member3 = Member.objects.create(
    id=uuid.uuid4(),
    first_name="Alice",
    last_name="Johnson",
    birth_date=datetime(1995, 3, 10).date(),
)

# Create Borrowing History
# Book 1 borrowed by Member 1 and Member 2
BorrowingHistory.objects.create(
    id=uuid.uuid4(),
    book=book1,
    member=member1,
    borrowing_date=timezone.now() - timedelta(days=15),
    returning_date=timezone.now() - timedelta(days=10),
)

BorrowingHistory.objects.create(
    id=uuid.uuid4(),
    book=book1,
    member=member2,
    borrowing_date=timezone.now() - timedelta(days=5),
    returning_date=None,  # Book not yet returned
)

# Book 2 borrowed by Member 2 and Member 3
BorrowingHistory.objects.create(
    id=uuid.uuid4(),
    book=book2,
    member=member2,
    borrowing_date=timezone.now() - timedelta(days=20),
    returning_date=timezone.now() - timedelta(days=12),
)

BorrowingHistory.objects.create(
    id=uuid.uuid4(),
    book=book2,
    member=member3,
    borrowing_date=timezone.now() - timedelta(days=8),
    returning_date=None,  # Book not yet returned
)

# Book 3 borrowed by Member 1 and Member 3
BorrowingHistory.objects.create(
    id=uuid.uuid4(),
    book=book3,
    member=member1,
    borrowing_date=timezone.now() - timedelta(days=10),
    returning_date=timezone.now() - timedelta(days=3),
)

BorrowingHistory.objects.create(
    id=uuid.uuid4(),
    book=book3,
    member=member3,
    borrowing_date=timezone.now() - timedelta(days=2),
    returning_date=None,  # Book not yet returned
)

# Print success message
print("Sample data created successfully!")