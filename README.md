# Parkinson

A Django-based data management and analysis system for collecting and analyzing multilingual Wikipedia article data related to Parkinson's disease.

## Overview

Parkinson is a command-line data pipeline built with Django that collects, parses, and analyzes Wikipedia content across multiple languages. Django is used as the foundation for managing structured, relational data and providing a convenient admin interface for data exploration and management. All operations are performed through management commands rather than web pages.

## Features

- **Multilingual Data Collection**: Gather and organize Wikipedia articles across different language editions
- **Article Management**: Organize articles by category with unique identification and Wikidata integration
- **Content Parsing**: Parse and store article structure and metadata in JSON format
- **Reference Analysis**: Extract, categorize, and analyze references including DOI and PMID identifiers
- **Editorial Analytics**: Track editing history, contributor information, and authorship patterns
- **Page Statistics**: Monitor word counts, image counts, internal links, sections, and page views
- **Query Management**: Store and manage query data for further analysis
- **Data Exploration**: Use the Django admin interface to browse and inspect collected data

## Project Structure

```
parkinson/
├── parkinson/              # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── data/                   # Main data app
│   ├── models.py           # Database models for structured data
│   ├── admin.py            # Admin interface configuration
│   ├── management/         # Custom management commands
│   │   └── commands/       # Place command scripts here
│   └── migrations/         # Database migrations
├── manage.py               # Django management script entry point
├── requirements.txt        # Python dependencies
└── db.sqlite3              # SQLite database
```

## Data Models

### Core Models

- **Category**: Wikipedia article category with ID, name, and Wikidata reference
- **Page**: Language-specific Wikipedia page entries with URLs and metadata
- **Parser**: Stores parsed article structure and content in JSON format
- **Query**: Stores query results and data in JSON format
- **Analysis**: Article statistics (word count, edit history, editors, sections, images, etc.)
- **Reference**: Article references with optional year, country code, DOI, and PMID
- **Authorship**: Contributor information and edit sizes per language version
- **Pageviews**: Page view statistics tracking

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/albertoleoncio/parkinson.git
cd parkinson
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations to set up the database:
```bash
python manage.py migrate
```

5. (Optional) Create a superuser for Django admin access:
```bash
python manage.py createsuperuser
```

## Usage

### Running Management Commands

All operations are performed through Django management commands. Create command scripts in `data/management/commands/`:

```bash
python manage.py your_command_name
```

### Data Exploration

Access the Django admin interface to browse and inspect collected data:

```bash
python manage.py runserver
```

Then navigate to `http://localhost:8000/admin/` and log in with your superuser credentials.

### Database Queries

Use Django's ORM in your management commands to query and manipulate data:

```python
from data.models import Category, Page, Analysis

# Query examples
categories = Category.objects.all()
pages = Page.objects.filter(language_code='en')
analysis = Analysis.objects.get(page=page_id)
```

## Database

SQLite3 is used for development and local data storage. The database file (`db.sqlite3`) is created automatically after running migrations.

## Dependencies

- **Django 4.2.11**: ORM and data management framework
- **bs4 0.0.2**: BeautifulSoup for HTML parsing (if needed for web scraping)

See `requirements.txt` for complete requirements.

## Configuration

### Settings

Edit `parkinson/settings.py` to customize:
- `INSTALLED_APPS`: Add or remove Django apps
- `DATABASES`: Configure database connection (if not using SQLite)
- Language and timezone settings

## Development

### Creating Management Commands

Create new command files in `data/management/commands/`:

```bash
data/management/commands/
├── __init__.py
├── collect_articles.py
├── parse_data.py
├── analyze_pages.py
└── ...
```

Each command file should inherit from `django.core.management.base.BaseCommand`.

### Making Model Changes

When you modify models in `data/models.py`, create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Shell Access

Access the Django shell for interactive data exploration and testing:

```bash
python manage.py shell
```

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available on GitHub.

## Author

Alberto Leon Cioth ([@albertoleoncio](https://github.com/albertoleoncio))

---

For more information about Django, visit [Django Documentation](https://docs.djangoproject.com/)
