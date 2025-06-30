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
│                    Business Logic Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │    Services     │  │   Validation    │  │  Business    │ │
│  │                 │  │                 │  │   Rules      │ │
│  │                 │  │                 │  │  (Missing)   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Data Access Layer                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │  Repositories   │  │     Models      │  │  Migrations  │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Containers    │  │   Dependency    │  │  Singleton   │ │
│  │ (DI Container)  │  │   Injection     │  │  Management  │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

> **Note**: Business Rules are currently missing from the implementation but can be added as separate entities in the Business Logic Layer for better separation of concerns.

## 📁 Project Structure

```
library-management-system/
├── book/                          # Book management app
│   ├── models/                    # Data models
│   │   ├── book.py               # Book entity
│   │   ├── author.py             # Author entity
│   │   ├── genre.py              # Genre entity
│   │   └── publisher.py          # Publisher entity
│   ├── repositories/             # Data access layer
│   │   ├── book_repository.py    # Book data operations
│   │   ├── author_repository.py  # Author data operations
│   │   ├── genre_repository.py   # Genre data operations
│   │   └── publisher_repository.py # Publisher data operations
│   ├── services/                 # Business logic layer
│   │   ├── book_crud_service.py  # Book business operations
│   │   ├── author_crud_service.py # Author business operations
│   │   ├── genre_service.py      # Genre business operations
│   │   └── publisher_crud_service.py # Publisher business operations
│   ├── views/                    # Presentation layer
│   │   └── book_view.py          # Book API endpoints
│   ├── serializes/               # Data serialization
│   │   └── book_create_serializer.py # Book creation serializer
│   └── container.py              # Dependency injection container
├── member/                       # Member management app
│   ├── models/                   # Member data models
│   │   ├── member.py             # Member entity
│   │   └── borrowing_history.py  # Borrowing history entity
│   ├── repositories/             # Member data access
│   │   └── borrowing_repository.py # Borrowing data operations
│   ├── services/                 # Member business logic
│   │   └── member_service.py     # Member business operations
│   ├── views/                    # Member API endpoints
│   │   └── member_view.py        # Member API views
│   └── container.py              # Member dependency injection
└── librarymanagementsystem/      # Main Django project
    ├── container.py              # Root dependency injection container
    ├── settings.py               # Django settings
    └── urls.py                   # Main URL configuration
```

## 🔧 Core Components

### 1. **Containers (Infrastructure Layer - Dependency Injection)**

The project uses **dependency-injector** for dependency injection, providing loose coupling and testability. Containers belong to the **Infrastructure Layer** as they handle dependency inversion and singleton instance management.

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

    # Services
    book_service = providers.Singleton(
        BookCrudService,
        book_repository=book_repository,
        author_service=author_service,
        # ... other dependencies
    )
```

**Benefits:**

- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Loose Coupling**: Components don't directly instantiate dependencies
- **Testability**: Easy to mock dependencies for unit testing
- **Singleton Management**: Ensures single instances of services and repositories
- **Lifecycle Management**: Controls object creation and destruction

### 2. **Models (Data Layer)**

Models represent the database schema and business entities.

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

### 3. **Repositories (Data Access Layer)**

Repositories abstract database operations and provide a clean interface for data access.

#### Book Repository (`book/repositories/book_repository.py`)

```python
class BookAbstractRepository(ABC):
    @abstractmethod
    def add_book(self, book_data):
        raise NotImplementedError("This method should be overridden.")

class BookRepository(BookAbstractRepository):
    def __init__(self):
        self.book_model = Book

    def add_book(self, book_data):
        return self.book_model.objects.create(
            title=book_data["title"],
            description=book_data["description"],
            # ... other fields
        )
```

**Benefits:**

- **Abstraction**: Hides database implementation details
- **Testability**: Easy to mock for unit testing
- **Interface Segregation**: Abstract base classes define contracts
- **Single Responsibility**: Each repository handles one entity type

### 4. **Services (Business Logic Layer)**

Services contain business logic and orchestrate operations between repositories.

#### Book Service (`book/services/book_crud_service.py`)

```python
class BookCrudService:
    def __init__(
        self,
        book_repository: BookAbstractRepository,
        author_service: AuthorCRUDService,
        publisher_service: PublisherCRUDService,
    ):
        self.book_repository = book_repository
        self.author_service = author_service
        self.publisher_service = publisher_service

    def create_book(self, book_data):
        try:
            with transaction.atomic():
                author = self.author_service.get_author(book_data["author_id"])
                publisher = self.publisher_service.get_publisher(book_data["publisher_id"])

                book = self.book_repository.add_book({
                    "title": book_data["title"],
                    "author": author,
                    "publisher": publisher,
                    # ... other fields
                })
                return book
        except ObjectDoesNotExist as e:
            raise ValidationError(f"Invalid ID: {e!s}")
```

**Key Features:**

- **Transaction Management**: Atomic operations for data consistency
- **Dependency Injection**: Services receive dependencies via constructor
- **Error Handling**: Proper exception handling and validation
- **Business Rules**: Enforces business logic and validation

### 5. **Business Rules (Business Logic Layer) - Future Enhancement**

Currently, business rules are embedded within services. For better separation of concerns, you can extract business rules into separate entities:

#### Example Business Rules Structure:

```
business_rules/
├── book_rules/
│   ├── book_creation_rules.py
│   ├── book_validation_rules.py
│   └── book_business_rules.py
├── member_rules/
│   ├── borrowing_rules.py
│   ├── member_validation_rules.py
│   └── member_business_rules.py
└── common_rules/
    ├── validation_rules.py
    └── business_constants.py
```

#### Example Business Rule Implementation:

```python
# book_rules/book_creation_rules.py
class BookCreationRules:
    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        """Validate ISBN format and checksum."""
        # ISBN validation logic
        pass

    @staticmethod
    def validate_publication_date(date: date) -> bool:
        """Validate that publication date is not in the future."""
        return date <= date.today()

    @staticmethod
    def validate_book_title(title: str) -> bool:
        """Validate book title requirements."""
        return len(title.strip()) >= 1 and len(title) <= 100

# Usage in service
class BookCrudService:
    def __init__(self, book_rules: BookCreationRules, ...):
        self.book_rules = book_rules

    def create_book(self, book_data):
        # Apply business rules
        if not self.book_rules.validate_isbn(book_data["isbn"]):
            raise ValidationError("Invalid ISBN")
        # ... rest of the logic
```

**Benefits of Separate Business Rules:**

- **Single Responsibility**: Each rule class handles specific business logic
- **Reusability**: Rules can be reused across different services
- **Testability**: Business rules can be tested independently
- **Maintainability**: Easier to modify business rules without touching services
- **Documentation**: Business rules serve as living documentation

### 6. **Views (Presentation Layer)**

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
            book_service.create_book(book_create_serializer.validated_data)

            return Response({"message": "Book created successfully"}, status=201)
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

## 🔄 Data Flow

```
HTTP Request → View → Serializer → Service → Repository → Model → Database
     ↑                                                              ↓
HTTP Response ← View ← Serializer ← Service ← Repository ← Model ← Database
```

1. **HTTP Request** arrives at a View
2. **View** validates input using Serializers
3. **Service** orchestrates business logic
4. **Repository** handles data persistence
5. **Model** represents the data structure
6. **Database** stores the data
7. **Response** flows back through the layers

## 🧪 Testing Strategy

The architecture supports comprehensive testing:

- **Unit Tests**: Test individual services and repositories in isolation
- **Integration Tests**: Test service interactions
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

1. **Maintainability**: Clear separation of concerns
2. **Testability**: Easy to unit test with dependency injection
3. **Scalability**: Modular design allows easy extension
4. **Flexibility**: Easy to swap implementations
5. **Readability**: Clear code organization and naming conventions

This architecture provides a solid foundation for building maintainable, testable, and scalable Django applications.
