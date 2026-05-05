# Pazzo Backend Documentation

Welcome to the Pazzo backend documentation.

## Quick Links

- [Architecture Guide](architecture.md) - Deep dive into Clean Architecture implementation
- [API Documentation](api.md) - Coming soon (Swagger/OpenAPI)
- [Development Guide](../README.md#desarrollo) - How to develop new features
- [Testing Guide](../README.md#testing) - How to write and run tests

## Project Overview

Pazzo is a digital passport system for businesses and cycling routes. Users can collect stamps from businesses and cycling routes they visit.

### Technology Stack

- **Backend Framework**: Django 5.0 + Django REST Framework
- **Language**: Python 3.12 with strict type hints
- **Architecture**: Clean Architecture + Domain-Driven Design
- **Database**: PostgreSQL 15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Containerization**: Docker + Docker Compose
- **Testing**: pytest + pytest-django
- **Code Quality**: mypy (type checking), black (formatting), flake8 (linting)

### Core Features (Phase 1)

- ✅ User registration and JWT authentication
- ✅ Clean Architecture implementation
- ✅ Type-safe codebase with mypy strict mode
- ✅ Comprehensive test suite (unit, integration, e2e)
- ✅ Docker-based development environment
- ✅ Hello World authenticated endpoint (demo)

### Upcoming Features

- 📋 Passport creation and management
- 📋 Business profiles and locations
- 📋 Cycling routes
- 📋 Stamp collection system
- 📋 Achievement/rewards system
- 📋 Social features

## Getting Started

See the [README](../README.md#inicio-rápido) for installation and setup instructions.

## Architecture

The project follows **Clean Architecture** principles with **Domain-Driven Design**:

- **Domain Layer**: Pure business logic, no framework dependencies
- **Application Layer**: Use cases, DTOs, repository interfaces
- **Infrastructure Layer**: Database models, repository implementations
- **Interfaces Layer**: REST API endpoints, serializers

Read the full [Architecture Guide](architecture.md) for detailed information.

## Development Workflow

1. Create feature branch
2. Implement following Clean Architecture layers
3. Write tests (unit → integration → e2e)
4. Run type checking (`mypy`)
5. Format code (`black`, `isort`)
6. Run linter (`flake8`)
7. Ensure all tests pass
8. Create pull request

## Code Style

- Use type hints everywhere
- Follow PEP 8 (enforced by black + flake8)
- Docstrings for all public methods
- Keep functions small and focused
- Prefer composition over inheritance
- Use dataclasses for data structures

## Contributing

See contribution guidelines in [README](../README.md#contribución).
