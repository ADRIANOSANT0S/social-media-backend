# Social Media Backend

Backend API built with Django 5.2, JWT authentication, and REST Framework. Project setup and authentication with poetry and Makefile.


## Feature

- JWT Authentication with rest_framework_simplejwt.
- CORS enabled via django-cores-headers.
- Database configuration via environment variable
- Automated commands with Makefile (dev, migration, startapp, lint, format, etc.).
- Code quality tool: Flake8, Black, Isort. 


## Prerequisites
- Python 3.12+.
- Poetry.
- PostgresSQL(or SQLite for development).

> ⚠️ **Note**: These instructions (Makefile, paths, shell usage) are tailored for Ubuntu/Linux environments.
> If you're using Windows or macOS, make sure to adapt paths and command syntax accordingly.


## Getting Start

1. Clone the repository

```
git clone https://github.com/ADRIANOSANT0S/social-media-backend/

cd social-media-backend
```

2. Install dependencies with Poetry

```
poetry install
```

3. Setup environment variables

Create a .env file in the project root with the following example variables:
```
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=
ALLOWED_HOSTS=
CORS_ALLOWED_ORIGINS=http://localhost:300,http://127.0.1:3001
SQL_ENGINE=
SQL_DATABASE=
SQL_USER=
SQL_PASSWORD=
SQL_HOST=
SQL_PORT=
```
Adjust accordingly for production.

4. Run migrations

```
make migrate
```

5. Start the development server

```
make dev
```


## Useful Makefile Commands

- make dev - start Django development server.
- make migrate - run migrations.
- make makemigrations - create new migrations.
- make startapp name=<app_name> - create new Django app inside apps/ folder.
- make lint - run linters (flake8, black, isort checks).
- make format auto format code (flake8, black, isort).
- make shell - open Django shell
- make test - run tests

## Notes

- Static and media file are configured but the backend does not store media files, only processes URLs.
-JWT token have short-lived access token and refresh token with rotation and blacklist enabled.
- Customize .env for different environments (development, production, staging, etc.).

