# Django Recipe API

A fully-featured REST API built with Django REST Framework for managing recipes. This project demonstrates best practices in API development including Test Driven Development (TDD), Docker containerization, token-based authentication, and comprehensive API documentation.

## 🚀 Features

- **User Authentication**: Token-based authentication system with user registration and login
- **Recipe Management**: Full CRUD operations for recipes
- **Image Upload**: Upload and retrieve recipe images
- **API Documentation**: Auto-generated interactive API documentation using drf-spectacular (Swagger/OpenAPI)
- **PostgreSQL Database**: Production-ready database with migrations
- **Docker Support**: Fully containerized application with Docker and Docker Compose
- **Test Coverage**: Comprehensive test suite following TDD principles
- **Internationalization**: Multi-language support (i18n)
- **Production Ready**: Nginx reverse proxy configuration for deployment

## 🛠️ Technology Stack

- **Backend Framework**: Django 3.2.4
- **API Framework**: Django REST Framework 3.12.4
- **Database**: PostgreSQL 13
- **Authentication**: Token-based authentication
- **API Documentation**: drf-spectacular
- **Web Server**: uWSGI + Nginx (production)
- **Containerization**: Docker & Docker Compose
- **Image Processing**: Pillow
- **Code Quality**: Flake8 for linting
- **Language**: Python 3.9

## 📋 Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

Alternatively, for local development without Docker:
- Python 3.9
- PostgreSQL 13

## 🚦 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd WebApi
```

2. **Build the Docker images**
```bash
docker-compose build
```

3. **Start the services**
```bash
docker-compose up
```

The API will be available at `http://localhost:8000`

4. **Access the API documentation**
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema`

5. **Create a superuser (optional)**
```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

6. **Access the Django admin panel**
- Navigate to `http://localhost:8000/admin/`

## 📚 API Endpoints

### User Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/user/create/` | Register a new user | No |
| POST | `/api/user/token/` | Generate authentication token | No |
| GET | `/api/user/me/` | Get current user profile | Required |
| PUT | `/api/user/me/` | Update user profile | Required |
| PATCH | `/api/user/me/` | Partially update user profile | Required |

### Recipe Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/recipe/recipes/` | List all recipes | Required |
| POST | `/api/recipe/recipes/` | Create a new recipe | Required |
| GET | `/api/recipe/recipes/{id}/` | Get recipe details | Required |
| PUT | `/api/recipe/recipes/{id}/` | Update a recipe | Required |
| PATCH | `/api/recipe/recipes/{id}/` | Partially update a recipe | Required |
| DELETE | `/api/recipe/recipes/{id}/` | Delete a recipe | Required |
| POST | `/api/recipe/recipes/{id}/upload-image/` | Upload recipe image | Required |
| GET | `/api/recipe/recipes/{id}/get-image/` | Get recipe image | Required |

### Example API Requests

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/user/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "testpass123",
    "name": "Test User"
  }'
```

**Login and get token:**
```bash
curl -X POST http://localhost:8000/api/user/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "testpass123"
  }'
```

**Create a recipe:**
```bash
curl -X POST http://localhost:8000/api/recipe/recipes/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Chocolate Cake",
    "description": "Delicious chocolate cake recipe",
    "time_minutes": 45,
    "price": 15.99,
    "link": "https://example.com/recipe"
  }'
```

**Upload a recipe image:**
```bash
curl -X POST http://localhost:8000/api/recipe/recipes/1/upload-image/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -F "image=@/path/to/image.jpg"
```

## 📁 Project Structure

```
WebApi/
├── app/                          # Main Django application
│   ├── app/                      # Project settings and configuration
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Main URL configuration
│   │   └── wsgi.py               # WSGI configuration
│   ├── core/                     # Core app (models, admin)
│   │   ├── models.py             # User and Recipe models
│   │   ├── admin.py              # Django admin configuration
│   │   ├── management/           # Custom management commands
│   │   │   └── commands/
│   │   │       └── wait_for_db.py  # Wait for database command
│   │   └── tests/                # Core app tests
│   ├── user/                     # User app (authentication)
│   │   ├── views.py              # User views
│   │   ├── serializers.py        # User serializers
│   │   ├── urls.py               # User URL routes
│   │   └── tests/                # User app tests
│   ├── recipe/                   # Recipe app
│   │   ├── views.py              # Recipe views
│   │   ├── serializers.py        # Recipe serializers
│   │   ├── urls.py               # Recipe URL routes
│   │   └── tests/                # Recipe app tests
│   ├── locale/                   # Internationalization files
│   └── manage.py                 # Django management script
├── proxy/                        # Nginx proxy configuration
│   ├── Dockerfile                # Nginx Dockerfile
│   ├── default.config.tpl        # Nginx configuration template
│   └── run.sh                    # Nginx startup script
├── scripts/                      # Utility scripts
│   └── run.sh                    # Application startup script
├── docker-compose.yml            # Development Docker Compose
├── docker-compose-deploy.yml     # Production Docker Compose
├── Dockerfile                    # Application Dockerfile
├── requirements.txt              # Python dependencies
├── requirements.dev.txt          # Development dependencies
└── README.md                     # This file
```

## ⚙️ Configuration

### Environment Variables

#### Development (docker-compose.yml)
The development environment uses the following default values:
- `DB_HOST=db` - Database host
- `DB_NAME=devdb` - Database name
- `DB_USER=alejo` - Database user
- `DB_PASS=password` - Database password
- `DEBUG=1` - Enable debug mode

#### Production (docker-compose-deploy.yml)
For production, create a `.env` file with:
```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASS=your_secure_password
DJANGO_SECRET_KEY=your_secret_key
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 🧪 Testing

### Run all tests
```bash
docker-compose run --rm app sh -c "python manage.py test"
```

### Run tests for a specific app
```bash
docker-compose run --rm app sh -c "python manage.py test core"
docker-compose run --rm app sh -c "python manage.py test user"
docker-compose run --rm app sh -c "python manage.py test recipe"
```

### Run linting
```bash
docker-compose run --rm app sh -c "flake8"
```

### Code Coverage
The project follows Test Driven Development (TDD) principles. Tests are located in the `tests/` directory within each app.

## 🚀 Production Deployment

### Build for production
```bash
docker-compose -f docker-compose-deploy.yml build
```

### Start production services
```bash
docker-compose -f docker-compose-deploy.yml up -d
```

### Collect static files
```bash
docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py collectstatic --noinput"
```

### Run migrations
```bash
docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py migrate"
```

### Create superuser
```bash
docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"
```

The production setup includes:
- **Nginx** reverse proxy on port 80
- **uWSGI** application server
- **PostgreSQL** database with persistent volumes
- **Static/Media files** served by Nginx

## 🔧 Development Workflow

### Common Docker Commands

**Build images:**
```bash
docker-compose build
```

**Start services:**
```bash
docker-compose up
```

**Start services in detached mode:**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Access shell in app container:**
```bash
docker-compose run --rm app sh
```

### Common Django Commands

**Create migrations:**
```bash
docker-compose run --rm app sh -c "python manage.py makemigrations"
```

**Apply migrations:**
```bash
docker-compose run --rm app sh -c "python manage.py migrate"
```

**Create a new app:**
```bash
docker-compose run --rm app sh -c "python manage.py startapp <app_name>"
```

**Create superuser:**
```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

**Access Python shell:**
```bash
docker-compose run --rm app sh -c "python manage.py shell"
```

## 🌍 Internationalization

The project supports multiple languages using Django's internationalization framework.

### Add a new language
```bash
docker-compose run --rm app sh -c "python manage.py makemessages -l <language_code>"
```

Example for Spanish:
```bash
docker-compose run --rm app sh -c "python manage.py makemessages -l es"
```

### Compile messages
```bash
docker-compose run --rm app sh -c "python manage.py compilemessages"
```

Translation files are located in `app/locale/`.

## 🐛 Troubleshooting

### Database connection issues
If you encounter database connection errors:
```bash
docker-compose run --rm app sh -c "python manage.py wait_for_db"
```

### Reset database
```bash
docker-compose down -v
docker-compose up
```

### Clear Python cache
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### View container logs
```bash
docker-compose logs app
docker-compose logs db
docker-compose logs proxy
```

## 📖 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

## 👏 Acknowledgments

This project is based on the Udemy course: "Create an advanced REST API with Python, Django REST Framework and Docker using Test Driven Development (TDD)".
