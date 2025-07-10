# FastApp

A FastAPI-based web application for task management with user authentication and role-based access control.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Overview

FastApp is a modern web application built with FastAPI, designed for managing tasks with user authentication and
role-based permissions. It uses PostgreSQL as the database, SQLAlchemy for ORM, and Alembic for database migrations. The
application supports JWT-based authentication with access and refresh tokens.

## Features

- User authentication with JWT (access and refresh tokens)
- Role-based access control (User, Moderator, Admin)
- Task management (CRUD operations)
- PostgreSQL database integration
- Database migrations with Alembic
- Comprehensive unit and integration tests
- Dockerized setup with PostgreSQL and pgAdmin
- Health check endpoint

## Prerequisites

- Python 3.13+
- Docker and Docker Compose
- PostgreSQL (if running without Docker)
- uv (for dependency management)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/fastapp.git
   cd fastapp
   ```

2. **Create and configure the .env file**:
   Copy `.env.example` to `.env` and update the environment variables as needed.
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies**:
   If not using Docker, install dependencies using uv:
   ```bash
   pip install uv
   uv sync
   ```

## Configuration

The application uses environment variables defined in `.env` for configuration. Key variables include:

- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`: Database credentials
- `PGADMIN_EMAIL`, `PGADMIN_PASSWORD`: pgAdmin credentials
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `REFRESH_TOKEN_EXPIRE_DAYS`, `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration settings

## Running the Application

### Using Docker

Run the application with Docker Compose:

```bash
docker-compose up --build
```

This will start:

- FastAPI application at `http://localhost:8000`
- PostgreSQL database at `localhost:5432`
- pgAdmin at `http://localhost:5050`

### Without Docker

Ensure PostgreSQL is running and configured, then start the FastAPI server:

```bash
uvicorn fastapp.main:app --host 0.0.0.0 --port 8000
```

### Database Migrations

Apply database migrations using Alembic:

```bash
alembic upgrade head
```

## Testing

The project includes unit and integration tests. Run tests with pytest:

```bash
pytest
```

## Project Structure

```
fastapp/
├── alembic/                  # Database migration scripts
├── src/
│   └── fastapp/
│       ├── core/             # Core utilities
│       ├── models/           # SQLAlchemy models
│       ├── repositories/     # Data access layer
│       ├── routers/          # API routes
│       ├── schemas/          # Pydantic schemas
│       ├── services/         # Business logic
│       ├── config.py         # Application configuration
│       ├── main.py           # FastAPI application entry point
├── tests/
│   ├── fixtures/             # Test fixtures
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   ├── e2e/                  # End-to-end tests
├── .dockerignore
├── .env
├── .env.example
├── .env.test
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
```

## API Endpoints

### Health

- `GET /health`: Check application health

### Authentication

- `POST /auth/token`: Obtain access and refresh tokens
- `POST /auth/refresh`: Refresh access token
- `GET /auth/me`: Get current user details

### Tasks

- `GET /tasks/`: List all tasks for the current user
- `GET /tasks/{task_id}`: Get a specific task
- `POST /tasks/`: Create a new task
- `PATCH /tasks/{task_id}`: Update a task
- `DELETE /tasks/{task_id}`: Delete a task

### Users (Admin only)

- `POST /users/`: Create a new user
- `DELETE /users/{user_id}`: Delete a user
- `PATCH /users/{user_id}/role`: Update user role
