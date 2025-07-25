# Developer's Guide - Video Rental Portal Django

This guide provides comprehensive information for developers working on the Video Rental Portal Django web application.

## Architecture Overview

### Core Components

1. **Config (`src/config/`)**: Central Django configuration
   - Settings management
   - URL routing
   - WSGI/ASGI configuration

2. **Pages (`src/pages/`)**: Main web interface
   - View functions for web pages
   - HTML templates
   - Static assets

3. **Up (`src/up/`)**: API health monitoring
   - Health check endpoints
   - API connectivity verification
   - System status monitoring

## Getting Started

### Prerequisites
- Python 3.8+
- Django 5.2+
- Virtual environment (recommended)

### Setup

1. **Clone and setup environment:**
   ```bash
   cd video-rental-portal-django
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database setup:**
   ```bash
   cd src
   python manage.py migrate
   python manage.py createsuperuser  # Optional: create admin user
   ```

3. **Run development server:**
   ```bash
   python manage.py runserver
   ```

4. **Access the application:**
   - Web interface: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Development Workflow

### Adding New Features

#### 1. Films Web Application (Next Recommended Step)

To extend the app with a full films management interface:

**A. Create Films App Structure:**
```bash
cd src
python manage.py startapp films
```

**B. Recommended Films App Features:**
- Film listing with pagination
- Film detail views
- Search functionality
- Category filtering
- Actor information
- Admin interface for film management

**C. Implementation Steps:**
1. **Models** (`films/models.py`):
   ```python
   class Film(models.Model):
       title = models.CharField(max_length=200)
       description = models.TextField()
       release_year = models.IntegerField()
       language = models.CharField(max_length=50)
       rating = models.CharField(max_length=10)
       
   class Actor(models.Model):
       name = models.CharField(max_length=100)
       films = models.ManyToManyField(Film)
   ```

2. **Views** (`films/views.py`):
   - `FilmListView`: Display all films
   - `FilmDetailView`: Show individual film details
   - `FilmSearchView`: Search functionality

3. **Templates** (`films/templates/films/`):
   - `film_list.html`: Films listing page
   - `film_detail.html`: Individual film page
   - `film_search.html`: Search interface

4. **URLs** (`films/urls.py`):
   ```python
   app_name = 'films'
   urlpatterns = [
       path('', views.FilmListView.as_view(), name='list'),
       path('<int:pk>/', views.FilmDetailView.as_view(), name='detail'),
       path('search/', views.FilmSearchView.as_view(), name='search'),
   ]
   ```

#### 2. API Integration Pattern

For connecting to the backend API (localhost:8080):

**A. Create API Service Layer:**
```python
# src/services/api_client.py
import requests
from django.conf import settings

class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.api_key = settings.API_KEY
    
    def get_films(self):
        response = requests.get(f"{self.base_url}/v1/films")
        return response.json()
    
    def get_film_by_id(self, film_id):
        response = requests.get(f"{self.base_url}/v1/films/{film_id}")
        return response.json()
```

**B. Update Settings** (`src/config/settings.py`):
```python
# API Configuration
API_BASE_URL = 'http://localhost:8080'
API_KEY = 'your-api-key-here'
```

### Health Check Implementation

The `up` app monitors API connectivity:

**A. Health Check View** (`src/up/views.py`):
```python
import requests
from django.http import JsonResponse
from django.conf import settings

def health_check(request):
    try:
        response = requests.get(f"{settings.API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return JsonResponse({'status': 'ok', 'api': 'connected'})
    except requests.RequestException:
        return JsonResponse({'status': 'error', 'api': 'disconnected'}, status=503)
```

**B. URL Configuration** (`src/up/urls.py`):
```python
from django.urls import path
from . import views

app_name = 'up'
urlpatterns = [
    path('health/', views.health_check, name='health'),
]
```

## Extension Patterns

### 1. Adding New Apps

For each major feature (customers, rentals, etc.):

1. **Create Django app:**
   ```bash
   python manage.py startapp [app_name]
   ```

2. **Add to INSTALLED_APPS** in `src/config/settings.py`

3. **Create app structure:**
   - Models for data representation
   - Views for business logic
   - Templates for presentation
   - URLs for routing
   - Forms for user input (if needed)

### 2. Template Organization

**Base Template Structure:**
```
src/pages/templates/
├── base.html                    # Main layout template
├── components/                  # Reusable components
│   ├── navbar.html
│   ├── footer.html
│   └── pagination.html
├── pages/                       # Page-specific templates
│   ├── home.html
│   └── about.html
└── [app_name]/                  # App-specific templates
    ├── list.html
    ├── detail.html
    └── form.html
```

### 3. API Integration Best Practices

1. **Centralized API Client**: Use a single API client class
2. **Error Handling**: Implement proper error handling for API failures
3. **Caching**: Consider caching API responses for better performance
4. **Async Operations**: Use async views for non-blocking API calls

## Testing Strategy

### 1. Unit Tests
- Test individual functions and methods
- Mock API calls for isolated testing

### 2. Integration Tests
- Test API connectivity
- Test complete user workflows

### 3. Health Monitoring
- Implement monitoring for API availability
- Set up alerts for system failures

## Deployment Considerations

### 1. Environment Configuration
- Use environment variables for sensitive settings
- Separate settings for development/production

### 2. Static Files
- Configure static file serving for production
- Use CDN for better performance

### 3. Database
- Consider PostgreSQL for production
- Implement proper database migrations

## Recommended Next Steps

1. **Implement Films App**: Start with the films management interface
2. **Add API Integration**: Connect to the backend API
3. **Implement Search**: Add search functionality across entities
4. **User Authentication**: Add user login/logout functionality
5. **Error Handling**: Implement comprehensive error handling
6. **Testing**: Add unit and integration tests
7. **Performance**: Implement caching and optimization

## Contributing

1. Follow Django best practices
2. Write tests for new features
3. Update documentation
4. Use meaningful commit messages
5. Create pull requests for review

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- [API Documentation](./api-info.md)

---

For questions or suggestions, please refer to the project maintainer or create an issue in the project repository.