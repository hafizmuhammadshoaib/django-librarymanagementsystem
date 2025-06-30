# Library Management System

A Django-based library management system built with clean architecture principles, featuring dependency injection, layered architecture, and separation of concerns.

## 🏗️ Architecture Overview

This project follows a **Clean Architecture** pattern with the following layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Views (API)   │  │   Serializers   │  │   URLs       │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │    Services     │  │   Use Cases     │  │  Application │ │
│  │                 │  │                 │  │   Logic      │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Domain Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │    Entities     │  │   Business      │  │  Domain      │ │
│  │                 │  │   Logic         │  │  Services    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  Repositories   │  │     Models      │  │  Containers  │ │
│  │                 │  │                 │  │  (DI)        │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
library-management-system/
├── book/                          # Book management app
│   ├── entities/                  # Domain entities with business rules
│   │   ├── book_entity.py        # Book domain entity
│   │   ├── author_entity.py      # Author domain entity
│   │   ├── genre_entity.py       # Genre domain entity
│   │   └── publisher_entity.py   # Publisher domain entity
│   ├── use_cases/                # Application layer - use cases
│   │   ├── create_book_use_case.py # Create book use case
│   │   └── get_book_use_case.py  # Get book use case
│   ├── models/                   # Infrastructure layer - data models
│   │   ├── book.py              # Book database model
│   │   ├── author.py            # Author database model
│   │   ├── genre.py             # Genre database model
│   │   └── publisher.py         # Publisher database model
│   ├── repositories/            # Infrastructure layer - data access
│   │   ├── book_repository.py   # Book data operations
│   │   ├── author_repository.py # Author data operations
│   │   ├── genre_repository.py  # Genre data operations
│   │   └── publisher_repository.py # Publisher data operations
│   ├── services/                # Application layer - services
│   │   ├── book_crud_service.py # Book business operations
│   │   ├── author_crud_service.py # Author business operations
│   │   ├── genre_service.py     # Genre business operations
│   │   └── publisher_crud_service.py # Publisher business operations
│   ├── views/                   # Presentation layer
│   │   └── book_view.py         # Book API endpoints
│   ├── serializes/              # Presentation layer - data serialization
│   │   └── book_create_serializer.py # Book creation serializer
│   └── container.py             # Infrastructure layer - dependency injection
├── member/                      # Member management app
│   ├── entities/                # Domain entities with business rules
│   │   ├── member_entity.py     # Member domain entity
│   │   └── borrowing_entity.py  # Borrowing domain entity
│   ├── use_cases/               # Application layer - use cases
│   │   └── borrow_book_use_case.py # Borrow book use case
│   ├── models/                  # Infrastructure layer - data models
│   │   ├── member.py            # Member database model
│   │   └── borrowing_history.py # Borrowing history database model
│   ├── repositories/            # Infrastructure layer - data access
│   │   ├── member_repository.py # Member data operations
│   │   └── borrowing_repository.py # Borrowing data operations
│   ├── services/                # Application layer - services
│   │   └── member_service.py    # Member business operations
│   ├── views/                   # Presentation layer
│   │   └── member_view.py       # Member API endpoints
│   └── container.py             # Infrastructure layer - dependency injection
├── librarymanagementsystem/     # Main Django project
│   ├── container.py             # Root dependency injection container
│   ├── settings.py              # Django settings
│   └── urls.py                  # Main URL configuration
├── tests/                       # Test suite
│   ├── conftest.py              # Test configuration
│   └── test_services/           # Service tests
└── requirements.txt             # Project dependencies
```

## 🔧 Core Components

### 1. **Entities (Domain Layer)**

Entities represent the core business objects with embedded business rules and validation logic.

#### Book Entity (`book/entities/book_entity.py`)

```python
@dataclass
class BookEntity:
    """Pure Book entity with business rules and no external dependencies."""

    title: str
    description: str
    published_date: date
    isbn: str
    author_id: uuid.UUID
    publisher_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        """Validate business rules after initialization."""
        self._validate_title()
        self._validate_isbn()
        self._validate_published_date()
        self._validate_description()

    def _validate_isbn(self):
        """Validate ISBN business rules."""
        if not self.isbn:
            raise ValueError("ISBN cannot be empty")

        if len(self.isbn) not in [10, 13]:
            raise ValueError("ISBN must be either 10 or 13 digits")

    def is_classic(self) -> bool:
        """Determine if the book is considered a classic (older than 50 years)."""
        return self.get_age_in_years() >= 50
```

**Key Features:**

- **Pure Domain Objects**: No external dependencies
- **Business Rules**: Embedded validation and business logic
- **Immutable by Design**: Business rules enforced at creation
- **Rich Behavior**: Methods that encapsulate business logic

#### Member Entity (`member/entities/member_entity.py`)

```python
@dataclass
class MemberEntity:
    """Pure Member entity with business rules and no external dependencies."""

    first_name: str
    last_name: str
    birth_date: date
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    borrowing_ids: List[uuid.UUID] = field(default_factory=list)

    def can_borrow_more_books(self, max_books: int = 5) -> bool:
        """Check if the member can borrow more books."""
        return self.get_borrowing_count() < max_books

    def is_minor(self) -> bool:
        """Check if the member is a minor (under 18)."""
        return self.get_age() < 18
```

### 2. **Use Cases (Application Layer)**

Use cases orchestrate the application's business logic and coordinate between entities and repositories.

#### Create Book Use Case (`book/use_cases/create_book_use_case.py`)

```python
class CreateBookUseCase:
    """Use case for creating a new book."""

    def __init__(
        self,
        book_repository: BookAbstractRepository,
        author_repository: AuthorAbstractRepository,
        publisher_repository: PublisherAbstractRepository,
        genre_repository: GenreAbstractRepository,
    ):
        self.book_repository = book_repository
        self.author_repository = author_repository
        self.publisher_repository = publisher_repository
        self.genre_repository = genre_repository

    def execute(self, book_data: Dict[str, Any]) -> BookEntity:
        """Execute the create book use case."""
        # Validate input data
        self._validate_input_data(book_data)

        # Check if book with same ISBN already exists
        existing_book = self.book_repository.get_book_by_isbn(book_data["isbn"])
        if existing_book:
            raise ValueError(f"Book with ISBN {book_data['isbn']} already exists")

        # Get related entities
        author = self.author_repository.get_author_entity_by_id(book_data["author_id"])
        publisher = self.publisher_repository.get_publisher_entity_by_id(book_data["publisher_id"])

        # Create book entity
        book_entity = BookEntity(
            title=book_data["title"],
            description=book_data["description"],
            published_date=book_data["published_date"],
            isbn=book_data["isbn"],
            author_id=book_data["author_id"],
            publisher_id=book_data["publisher_id"],
        )

        # Save with transaction
        with transaction.atomic():
            saved_book = self.book_repository.save_book(book_entity)

        return saved_book
```

**Key Features:**

- **Single Responsibility**: Each use case handles one specific business operation
- **Dependency Injection**: Receives dependencies via constructor
- **Transaction Management**: Ensures data consistency
- **Business Logic Orchestration**: Coordinates between multiple repositories

#### Borrow Book Use Case (`member/use_cases/borrow_book_use_case.py`)

```python
class BorrowBookUseCase:
    """Use case for borrowing a book."""

    def execute(self, borrowing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the borrow book use case."""
        # Validate input data
        self._validate_input_data(borrowing_data)

        # Get member and book entities
        member = self.member_repository.get_member_by_id(member_id)
        book = self.book_repository.get_book_by_id(book_id)

        # Check business rules
        self._check_borrowing_rules(member, book)

        # Create borrowing entity
        borrowing_entity = BorrowingEntity(
            book_id=book_id,
            member_id=member_id,
            borrowing_date=borrowing_date,
        )

        # Save borrowing
        saved_borrowing = self.borrowing_repository.save_borrowing(borrowing_entity)

        return saved_borrowing.to_dict()

    def _check_borrowing_rules(self, member: MemberEntity, book: BookEntity):
        """Check business rules for borrowing."""
        if not member.can_borrow_more_books():
            raise RuntimeError("Member has reached the maximum number of borrowings")

        if not book.is_available_for_borrowing():
            raise RuntimeError("Book is not available for borrowing")
```

### 3. **Services (Application Layer)**

Services act as the primary interface for the application layer, delegating business logic to use cases and handling error translation.

#### Book Service (`book/services/book_crud_service.py`)

```python
class BookCrudService:
    def __init__(
        self,
        create_book_use_case: CreateBookUseCase,
        get_book_use_case: GetBookUseCase,
    ):
        self.create_book_use_case = create_book_use_case
        self.get_book_use_case = get_book_use_case

    def create_book(self, book_data: Dict[str, Any]) -> BookEntity:
        """Create a new book using the CreateBookUseCase."""
        try:
            return self.create_book_use_case.execute(book_data)
        except (ValueError, RuntimeError) as e:
            raise ValidationError(e)

    def get_book_by_id(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Get a book by ID using the GetBookUseCase."""
        try:
            return self.get_book_use_case.get_book_by_id(book_id)
        except ValueError as e:
            raise ValidationError(str(e))

    def get_all_books(self, include_details: bool = True) -> List[Dict[str, Any]]:
        """Get all books using the GetBookUseCase."""
        return self.get_book_use_case.get_all_books(include_details)
```

**Key Features:**

- **Use Case Delegation**: Services delegate to specific use cases
- **Error Translation**: Convert domain exceptions to application exceptions
- **API Facade**: Provide a clean interface for views
- **Dependency Injection**: Receive use cases via constructor

#### Member Service (`member/services/member_service.py`)

```python
class MemberService:
    def __init__(
        self,
        borrowing_repository: BorrowingAbstractRepository,
        member_repository: MemberAbstractRepository,
        borrow_book_use_case: BorrowBookUseCase,
    ):
        self.borrowing_repository = borrowing_repository
        self.member_repository = member_repository
        self.borrow_book_use_case = borrow_book_use_case

    def borrow_book(self, borrowing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Borrow a book using the BorrowBookUseCase."""
        try:
            return self.borrow_book_use_case.execute(borrowing_data)
        except (ValueError, RuntimeError) as e:
            raise ValidationError(str(e))
```

### 4. **Containers (Infrastructure Layer - Dependency Injection)**

The project uses **dependency-injector** for dependency injection, providing loose coupling and testability.

#### Root Container (`librarymanagementsystem/container.py`)

```python
class Container(containers.DeclarativeContainer):
    """Application container."""
    config = providers.Configuration()
    book_container = providers.Container(BookContainer)
    member_container = providers.Container(MemberContainer)
```

#### Book Container (`book/container.py`)

```python
class BookContainer(containers.DeclarativeContainer):
    """Book app container."""

    # Repositories
    author_repository = providers.Singleton(AuthorRepository)
    book_repository = providers.Singleton(BookRepository)
    genre_repository = providers.Singleton(GenreRepository)
    publisher_repository = providers.Singleton(PublisherRepository)

    # Use Cases
    create_book_use_case = providers.Singleton(
        CreateBookUseCase,
        book_repository=book_repository,
        author_repository=author_repository,
        publisher_repository=publisher_repository,
        genre_repository=genre_repository,
    )

    get_book_use_case = providers.Singleton(
        GetBookUseCase,
        book_repository=book_repository,
        author_repository=author_repository,
        publisher_repository=publisher_repository,
        genre_repository=genre_repository,
    )

    # Services
    book_service = providers.Singleton(
        BookCrudService,
        create_book_use_case=create_book_use_case,
        get_book_use_case=get_book_use_case,
    )
```

**Benefits:**

- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Loose Coupling**: Components don't directly instantiate dependencies
- **Testability**: Easy to mock dependencies for unit testing
- **Singleton Management**: Ensures single instances of services and repositories
- **Lifecycle Management**: Controls object creation and destruction

### 5. **Models (Infrastructure Layer)**

Models represent the database schema and handle data persistence.

#### Book Model (`book/models/book.py`)

```python
class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Key Features:**

- **UUID Primary Keys**: For better security and distribution
- **Audit Fields**: `created_at` and `updated_at` for tracking
- **Foreign Key Relationships**: Proper entity relationships
- **Validation**: Django model validation

### 6. **Repositories (Infrastructure Layer)**

Repositories abstract database operations and provide a clean interface for data access.

#### Book Repository (`book/repositories/book_repository.py`)

```python
class BookAbstractRepository(ABC):
    @abstractmethod
    def add_book(self, book_data):
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def get_book_by_id(self, book_id: uuid.UUID) -> Optional[BookEntity]:
        raise NotImplementedError("This method should be overridden.")

class BookRepository(BookAbstractRepository):
    def __init__(self):
        self.book_model = Book

    def save_book(self, book_entity: BookEntity) -> BookEntity:
        """Save book entity to database."""
        book_model = self.entity_to_model(book_entity)
        saved_model = book_model.save()
        return self.model_to_entity(saved_model)

    def get_book_by_id(self, book_id: uuid.UUID) -> Optional[BookEntity]:
        """Get book entity by ID."""
        try:
            book_model = self.book_model.objects.get(id=book_id)
            return self.model_to_entity(book_model)
        except self.book_model.DoesNotExist:
            return None
```

**Benefits:**

- **Abstraction**: Hides database implementation details
- **Testability**: Easy to mock for unit testing
- **Interface Segregation**: Abstract base classes define contracts
- **Single Responsibility**: Each repository handles one entity type
- **Entity-Model Mapping**: Converts between domain entities and database models

### 7. **Views (Presentation Layer)**

Views handle HTTP requests and responses, delegating business logic to services.

#### Book View (`book/views/book_view.py`)

```python
class BookCreateAndGetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            book_create_serializer = BookCreateSerializer(data=request.data)
            book_create_serializer.is_valid(raise_exception=True)

            book_service: BookCrudService = container.book_container.book_service()
            created_book = book_service.create_book(
                book_create_serializer.validated_data
            )

            return Response({
                "id": created_book.id,
                "title": created_book.title,
                "description": created_book.description,
                # ... other fields
            }, status=201)
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
```

**Benefits:**

- **Separation of Concerns**: Views only handle HTTP concerns
- **Dependency Injection**: Services injected via container
- **Error Handling**: Proper HTTP status codes and error responses
- **Serialization**: Input validation and data transformation

#### Member View (`member/views/member_view.py`)

```python
class MemberBorrowingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, member_id):
        """Get member's borrowing statistics and book list"""
        try:
            member_service: MemberService = container.member_container.member_service()

            stats = member_service.get_member_borrowing_stats(member_id)
            borrowed_books = member_service.get_member_borrowed_books(member_id)

            return Response({
                "member_id": member_id,
                "borrowing_stats": stats,
                "borrowed_books": borrowed_books,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to get member borrowing info: {e!s}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
```

## 🔄 Data Flow

```
HTTP Request → View → Serializer → Service → Use Case → Entity → Repository → Model → Database
     ↑                                                                                    ↓
HTTP Response ← View ← Serializer ← Service ← Use Case ← Entity ← Repository ← Model ← Database
```

1. **HTTP Request** arrives at a View
2. **View** validates input using Serializers
3. **Service** delegates to appropriate Use Case
4. **Use Case** orchestrates business logic and coordinates entities
5. **Entity** enforces business rules and contains domain logic
6. **Repository** handles data persistence and entity-model mapping
7. **Model** represents the database structure
8. **Database** stores the data
9. **Response** flows back through the layers

## 🧪 Testing Strategy

The architecture supports comprehensive testing:

- **Unit Tests**: Test individual entities, use cases, and repositories in isolation
- **Integration Tests**: Test use case interactions and repository operations
- **API Tests**: Test complete request/response cycles
- **Mock Testing**: Easy to mock dependencies using the container

## 🚀 Getting Started

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

3. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## 📚 Key Technologies

- **Django 3.2.23**: Web framework
- **Django REST Framework 3.12.4**: API framework
- **Dependency Injector 4.48.1**: Dependency injection
- **Ruff**: Code formatting and linting

## 🎯 Architecture Benefits

1. **Maintainability**: Clear separation of concerns with distinct layers
2. **Testability**: Easy to unit test with dependency injection and pure entities
3. **Scalability**: Modular design allows easy extension and modification
4. **Flexibility**: Easy to swap implementations through dependency injection
5. **Readability**: Clear code organization and naming conventions
6. **Domain-Driven Design**: Entities contain business logic and rules
7. **Clean Architecture**: Dependencies point inward, with domain at the center

## 🔍 Key Architectural Patterns

### 1. **Clean Architecture**

- **Dependency Rule**: Dependencies point inward
- **Domain Layer**: Contains business entities and rules
- **Application Layer**: Contains use cases and application services
- **Infrastructure Layer**: Contains external concerns (database, frameworks)

### 2. **Domain-Driven Design (DDD)**

- **Entities**: Rich domain objects with business logic
- **Value Objects**: Immutable objects representing concepts
- **Aggregates**: Clusters of related entities
- **Repositories**: Abstract data access

### 3. **Dependency Injection**

- **Inversion of Control**: Framework controls object creation
- **Loose Coupling**: Components don't create their dependencies
- **Testability**: Easy to substitute implementations

### 4. **Use Case Pattern**

- **Single Responsibility**: Each use case handles one business operation
- **Orchestration**: Coordinates between multiple repositories and entities
- **Transaction Management**: Ensures data consistency

### 5. **Service Layer Pattern**

- **API Facade**: Services provide a clean interface for views
- **Use Case Delegation**: Services delegate to specific use cases
- **Error Translation**: Convert domain exceptions to application exceptions
- **Cross-Cutting Concerns**: Handle logging, caching, etc.

This architecture provides a solid foundation for building maintainable, testable, and scalable Django applications with clear separation of concerns and strong domain modeling.
