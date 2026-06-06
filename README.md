# Django Design Pattern

A modular, production-ready Django REST API template with clean architecture patterns, dependency injection, and integration with modern infrastructure services.

---

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Framework** | Django 5.1, Django REST Framework |
| **Auth** | SimpleJWT (JWT), Custom Authentication Backend |
| **Database** | PostgreSQL (primary), SQLite (dev) |
| **Cache & Queue** | Redis, Celery |
| **Message Brokers** | RabbitMQ, Kafka (Confluent) |
| **Search** | Elasticsearch, Kibana |
| **Storage** | MinIO (S3-compatible) |
| **SMS** | Kavenegar |
| **DI** | Injector |
| **Validation** | Pydantic, DRF Serializers |
| **Monitoring** | django-prometheus, Sentry |
| **Task Queue** | Celery + Redis |
| **Infrastructure** | Docker, docker-compose |

---

## Architecture Layers

```
┌─────────────────────────────────────────┐
│              Presentation               │
│     api/v1/ (views, endpoints)          │
├─────────────────────────────────────────┤
│            Routing (urls/)              │
├─────────────────────────────────────────┤
│           Serializers + Schemas         │
│       (DRF Serializers, Pydantic)       │
├─────────────────────────────────────────┤
│          Permissions (permissions/)     │
├─────────────────────────────────────────┤
│           Services (services/)          │
│    Elasticsearch, MinIO, Redis, Kafka,  │
│    RabbitMQ, SMS, Email (Celery tasks)  │
├─────────────────────────────────────────┤
│        Repositories (repositories/)     │
│    Data access layer with DI injection  │
├─────────────────────────────────────────┤
│        Models (models/)                 │
├─────────────────────────────────────────┤
│   Middleware (exception, response,      │
│   validation, custom exception handler) │
└─────────────────────────────────────────┘
```

---

## Features

- **Modular API Structure** with versioning (`api/v1`)
- **Repository Pattern** for clean data access with Dependency Injection
- **Service Layer** integrating Elasticsearch, MinIO, RabbitMQ, Kafka, Redis, SMS
- **Celery Async Tasks** for email sending and SMS delivery
- **Custom Authentication** using JWT (SimpleJWT) with token blacklisting
- **Custom Exception Handling** with Persian error messages and structured JSON error codes
- **Request Validation** via decorator pattern (`@validate_serializer`)
- **Throttling / Rate Limiting** with Persian error messages (429)
- **Dependency Injection** using `injector` library for modularity & testability
- **Pydantic Schemas** for data integrity and validation
- **Pagination, Filtering, Caching** built-in patterns
- **Dockerized Infrastructure** (PostgreSQL, Redis, MinIO, RabbitMQ, ELK, Sentry)
- **Management Commands** for superuser creation, SQL import, Kafka listener
- **Prometheus Monitoring** via django-prometheus
- **Comprehensive Middleware** for exception handling and standardized API responses
- **Custom Signals** for event-driven actions
- **Avatar Management** with MinIO storage (upload, download, delete)

---

## Project Structure

```
.
├── django_design_pattern/              # Django project settings
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                     # Base settings (DB, auth, REST framework, CORS)
│   │   └── extra.py                    # Celery, Redis, MinIO config
│   ├── celery.py                       # Celery app configuration
│   ├── urls.py                         # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── django_design_pattern_app/          # Main application
│   ├── api/v1/
│   │   ├── auth/auth.py                # Register, Login, Forgot/Edit Password
│   │   ├── users/users.py              # Index, Avatar CRUD
│   │   └── admin/users.py              # Admin endpoints (empty)
│   │
│   ├── cache/
│   │   ├── cache_decorators.py         # Redis caching decorators
│   │   └── redis_cache.py
│   │
│   ├── email/
│   │   └── sendemail.py                # Email sending class
│   │
│   ├── injector/
│   │   └── base_injector.py            # Central DI container
│   │
│   ├── management/commands/
│   │   ├── create_superuser.py         # Create superuser from env vars
│   │   ├── import_sql.py               # Import SQL into PostgreSQL
│   │   └── launch_queue_listener.py    # Start Kafka consumer thread
│   │
│   ├── middleware/
│   │   ├── exceptionhandler.py         # Custom DRF exception handler
│   │   ├── exceptions.py               # @handle_exceptions decorator
│   │   ├── response.py                 # Standardized APIResponse class
│   │   └── validate.py                 # @validate_serializer decorator
│   │
│   ├── models/
│   │   ├── base.py                     # BaseModel (created_at, updated_at)
│   │   └── users.py                    # Custom User model, UserManager
│   │
│   ├── modules/                        # DI module bindings
│   │   ├── elastic_module.py
│   │   ├── minio_module.py
│   │   ├── redis_module.py
│   │   ├── rabbitmq_module.py
│   │   └── kavenegar_module.py
│   │
│   ├── permissions/
│   │   └── permissions.py              # IsSuperUser, IsAuthenticated, etc.
│   │
│   ├── repositories/
│   │   ├── base_repo.py                # Base repo with MinIO + ELK injection
│   │   └── users_repo.py               # User data access layer
│   │
│   ├── schemas/
│   │   └── users.py                    # Pydantic models
│   │
│   ├── serializers/
│   │   ├── users/users_serializers.py  # User CRUD, Register, Login serializers
│   │   ├── auth/auth_serializers.py    # Refresh token, Logout serializers
│   │   └── admin/user_serializers.py
│   │
│   ├── services/
│   │   ├── elasticsearch/              # Full-text search & indexing
│   │   ├── email/tasks.py              # Celery async email task
│   │   ├── kafka/                      # Message producer & consumer
│   │   ├── minio/minio.py              # S3-compatible object storage SDK
│   │   ├── rabbitmq/rabbitmq.py        # RabbitMQ pub/sub service
│   │   ├── redis/redis.py              # Redis service
│   │   └── sms/tasks.py                # Celery async SMS task
│   │
│   ├── signals/
│   │   ├── signals.py                  # Custom signal definitions
│   │   └── receivers.py                # Signal receivers
│   │
│   ├── tests/
│   │   ├── base_test.py
│   │   └── users/test_user_login.py
│   │
│   ├── urls/
│   │   ├── urls.py                     # App-level URL routing
│   │   ├── auth.py                     # Auth endpoints
│   │   ├── users.py                    # User & avatar endpoints
│   │   └── admin/admin.py              # Admin endpoints
│   │
│   ├── utils/
│   │   ├── helper.py                   # Date/time helpers (Unix, Jalali)
│   │   ├── messages.py                 # Error/Success code messages
│   │   ├── throttle.py                 # Custom throttle classes
│   │   └── validations.py              # Serializer validation handler
│   │
│   └── apps.py
│
├── infrastructure/                     # Docker infrastructure configs
│   ├── elasticsearch/Dockerfile
│   ├── kibana/Dockerfile
│   ├── minio/Dockerfile
│   ├── postgres/Dockerfile + postgresql.conf
│   ├── rabbitmq/Dockerfile
│   ├── redis/Dockerfile
│   └── sentry/Dockerfile
│
├── docker-compose.yml                  # All services orchestration
├── dev.env                             # Environment variables
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | View | Auth |
|--------|----------|------|------|
| POST | `/register/` | `UserRegisterView` | AllowAny |
| POST | `/login/` | `UserLoginView` | AllowAny |
| POST | `/login/forgetpass/` | `UserForgetPassView` | AllowAny |
| POST | `/login/editpass/<str:username>/` | `UserEditPassView` | AllowAny |
| POST | `/index` | `IndexView` | IsAuthenticated + IsSuperUser |
| POST | `/update` | `IndexView` | IsAuthenticated + IsSuperUser |
| POST | `/avatar/upload/` | `AvatarUploadView` | IsAuthenticated |
| GET | `/avatar/<str:username>/` | `AvatarDownloadView` | AllowAny |
| DELETE | `/avatar/delete/` | `AvatarDeleteView` | IsAuthenticated |

---

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| 1000 | Invalid | 404 |
| 1004 | Required / Blank | 404 |
| 1006 | Max length / Max value | 404 |
| 1007 | Unique constraint violation | 404 |
| 1008 | Password mismatch | 404 |
| 1010 | Min length / Min value | 404 |
| 1022 | Invalid credentials (login) | 401 |
| 1023 | No identifier provided | 400 |
| 1024 | User not found | 404 |
| 1025 | Throttled (rate limited) | 429 |
| 1030 | Empty | 404 |

---

## Environment Variables

Create a `dev.env` file (already provided) with:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `1` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | `localhost 127.0.0.1` |
| `SQL_ENGINE` | Database engine | `django.db.backends.postgresql` |
| `SQL_DATABASE` | Database name | — |
| `SQL_USER` | Database user | — |
| `SQL_PASSWORD` | Database password | — |
| `SQL_HOST` | Database host | `127.0.0.1` |
| `SQL_PORT` | Database port | `5436` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `MINIO_ENDPOINT` | MinIO endpoint | `localhost:9000` |
| `MINIO_ACCESS_KEY` | MinIO access key | — |
| `MINIO_SECRET_KEY` | MinIO secret key | — |
| `BUCKET_NAME` | MinIO default bucket | `avatars` |
| `ELASTICSEARCH_HOSTS` | ES endpoint | `http://127.0.0.1:9200` |
| `EMAIL_HOST_USER` | SMTP email user | — |
| `EMAIL_HOST_PASSWORD` | SMTP email password | — |
| `KAVENEGAR_KEY` | SMS API key | — |
| `KAVENEGAR_NUM` | SMS sender number | — |
| `SUPERUSER_USERNAME` | Default superuser username | — |
| `SUPERUSER_EMAIL` | Default superuser email | — |
| `SUPERUSER_PHONE` | Default superuser phone | — |
| `SUPERUSER_PASSWORD` | Default superuser password | — |
| `SENTRY_SDK` | Sentry DSN | — |

---

## Setup & Installation

### 1. Clone and configure

```bash
git clone <repo-url>
cd django_design_pattern
cp dev.env .env   # or use dev.env directly
```

### 2. Create virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
.\venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3. Run database migrations

```bash
python manage.py migrate
```

### 4. Create superuser

```bash
python manage.py create_superuser
```

Or interactively:

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

---

## Running with Docker (Infrastructure Services)

```bash
docker-compose up -d
```

This starts: PostgreSQL, Redis, MinIO, RabbitMQ, Elasticsearch, Kibana.

To run the Django server locally (not in Docker):

```bash
python manage.py runserver
```

---

## Celery Async Tasks

Email sending and SMS delivery are handled asynchronously via Celery.

### Start the Celery worker

```bash
celery -A django_design_pattern worker -l info --pool=solo
```

### Available tasks

- `send_email_task` — Send email asynchronously (registration, login, password reset, password change notifications)
- `send_sms_task` — Send SMS via Kavenegar
- `check_sms_status_task` — Check SMS delivery status

---

## Management Commands

| Command | Description |
|---------|-------------|
| `create_superuser` | Create superuser from environment variables |
| `import_sql <file>` | Import raw SQL file into PostgreSQL |
| `launch_queue_listener` | Start Kafka consumer thread for `user_created` topic |

---

## Architecture Overview

### Request Flow

```
Request → URL Router → Middleware → Permission Check → Throttle Check
  → @validate_serializer (decorator) → Serializer Validation
    → View → Service → Repository (DI) → Model/DB
      → APIResponse
```

### Dependency Injection

The project uses `injector` library for DI. Modules (Elasticsearch, MinIO, Redis, RabbitMQ, Kavenegar) are registered in `BaseInjector` and injected into repositories and services via `@inject` decorator.

### Repository Pattern

Repositories encapsulate data access logic. Base repositories receive external service clients (MinIO, Elasticsearch) via DI. This keeps business logic clean and testable.

### Serializer Validation

The `@validate_serializer()` decorator intercepts requests, validates serializer data, and returns structured error responses with error codes before the view logic executes.

### Exception Handling

All unhandled exceptions are captured by:
1. `@handle_exceptions` decorator (Sentry + error response)
2. Custom DRF exception handler (structured Persian error messages)

---

## Testing

```bash
python manage.py test django_design_pattern_app
```

With coverage:

```bash
coverage run manage.py test django_design_pattern_app
coverage report
```

---

## Directory Overview

### `api/v1/` — API Endpoints
Versioned API views for authentication, user management, and admin operations.

### `services/` — External Integrations
Abstractions over external services: Elasticsearch, MinIO, Redis, RabbitMQ, Kafka, SMS (Kavenegar), Email (Celery tasks).

### `repositories/` — Data Access Layer
Repository pattern implementation with DI for database and service access.

### `serializers/` — Data Transformation
DRF serializers organized by domain (users, auth, admin) with custom validation.

### `schemas/` — Pydantic Models
Data contracts using Pydantic for type-safe request/response handling.

### `middleware/` — Request/Response Pipeline
Custom middleware for validation, exception handling, and standardized API responses.

### `injector/` — Dependency Injection
Central DI container wiring all service modules.

### `modules/` — DI Providers
Module definitions binding interfaces to concrete service implementations.

### `permissions/` — Access Control
Custom permission classes for role-based and superuser access.

### `cache/` — Caching Layer
Redis-based caching decorators for improved performance.

### `signals/` — Event System
Custom Django signals for decoupled event-driven communication.

### `utils/` — Utilities
Helper functions, validation logic, message definitions, throttle classes.

### `management/commands/` — CLI Commands
Custom `manage.py` commands for superuser creation, SQL import, and Kafka listener.

### `tests/` — Test Suite
Organized tests with `APIClient`, base test cases, and coverage support.

---

## Infrastructure

All services are containerized via Docker. Configuration files are in `infrastructure/`:

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Cache & Celery broker |
| MinIO | 9000, 9001 | S3-compatible object storage |
| RabbitMQ | 5672, 15672 | Message broker |
| Elasticsearch | 9200, 9300 | Full-text search |
| Kibana | 5601 | Elasticsearch visualization |
| Sentry | — | Error tracking |
