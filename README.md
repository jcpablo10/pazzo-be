# Pazzo Backend

Backend para la aplicación Pazzo - Sistema de pasaportes digitales para negocios y rutas ciclistas.

## 🏗️ Arquitectura

Este proyecto implementa **Clean Architecture** con **Domain-Driven Design (DDD)** usando:

- **Python 3.12**
- **Django 5.0**
- **Django REST Framework**
- **PostgreSQL 15**
- **JWT Authentication** (djangorestframework-simplejwt)
- **Docker & Docker Compose**
- **Type Hints obligatorios** con mypy strict mode

## 📁 Estructura del Proyecto

```
pazzo-be/
├── apps/                           # Aplicaciones Django
│   ├── hello/                      # App Hello World (ejemplo)
│   │   ├── domain/                 # Entidades y lógica de negocio
│   │   ├── application/            # Casos de uso
│   │   ├── infrastructure/         # Base de datos y servicios externos
│   │   └── interfaces/             # API REST (serializers, viewsets)
│   └── users/                      # App de usuarios
│       ├── domain/                 # User entity, excepciones
│       ├── application/            # Ports, DTOs, Use Cases
│       ├── infrastructure/         # ORM models, repositories
│       └── interfaces/             # API endpoints
├── config/                         # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── shared/                         # Utilidades compartidas
├── tests/                          # Tests organizados por tipo
│   ├── unit/                       # Sin dependencias de Django
│   ├── integration/                # Con base de datos
│   └── e2e/                        # Tests de API completos
├── docs/                           # Documentación
├── docker-compose.yml              # Orquestación de servicios
├── Dockerfile                      # Imagen de la aplicación
├── requirements.txt                # Dependencias Python
├── mypy.ini                        # Configuración de type checking
├── pytest.ini                      # Configuración de tests
└── manage.py                       # CLI de Django
```

### Capas de Clean Architecture

Cada aplicación sigue estrictamente las siguientes capas:

1. **Domain** (`domain/`) - Lógica de negocio pura
   - Entidades (dataclasses)
   - Excepciones de dominio
   - Sin dependencias de frameworks

2. **Application** (`application/`) - Orquestación de lógica de negocio
   - Ports (interfaces/contratos)
   - DTOs (Data Transfer Objects)
   - Use Cases (servicios de aplicación)

3. **Infrastructure** (`infrastructure/`) - Implementaciones concretas
   - Modelos Django ORM
   - Repositorios (implementación de ports)
   - Adaptadores para servicios externos

4. **Interfaces** (`interfaces/`) - Capa de presentación
   - Serializers (DRF)
   - ViewSets (endpoints API)
   - URLs

## 🚀 Inicio Rápido

### Prerequisitos

- Docker y Docker Compose instalados
- Git

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd pazzo-be
   ```

2. **Crear archivo de entorno**
   ```bash
   cp .env.example .env
   ```
   
   Editar `.env` con tus configuraciones (opcional para desarrollo local).

3. **Levantar servicios con Docker**
   ```bash
   docker-compose up --build
   ```

   Esto iniciará:
   - PostgreSQL en puerto 5432
   - Django en puerto 8000

4. **Ejecutar migraciones** (en otra terminal)
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Crear superusuario** (opcional)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Acceder a la aplicación**
   - API: http://localhost:8000/api/v1/
   - Admin: http://localhost:8000/admin/

## 📋 Endpoints Disponibles

### Autenticación JWT

**Obtener Token**
```bash
POST /api/v1/token/
{
  "email": "user@example.com",
  "password": "your-password"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Refrescar Token**
```bash
POST /api/v1/token/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usuarios

**Registrar Usuario**
```bash
POST /api/v1/users/register/
{
  "email": "newuser@example.com",
  "password": "securepassword123"
}

Response: 201 Created
{
  "id": 1,
  "email": "newuser@example.com",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Hello World (Requiere Autenticación)

**Obtener Mensaje**
```bash
GET /api/v1/hello/
Headers: Authorization: Bearer <access_token>

Response: 200 OK
{
  "message": "Hello World from Pazzo!",
  "user": "user@example.com",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🧪 Testing

### Ejecutar todos los tests
```bash
docker-compose exec web pytest
```

### Ejecutar solo tests unitarios (rápidos, sin DB)
```bash
docker-compose exec web pytest tests/unit/ -m unit
```

### Ejecutar tests de integración
```bash
docker-compose exec web pytest tests/integration/ -m integration
```

### Ejecutar tests e2e
```bash
docker-compose exec web pytest tests/e2e/ -m e2e
```

### Ver cobertura de código
```bash
docker-compose exec web pytest --cov=apps --cov-report=html
```

El reporte HTML estará en `htmlcov/index.html`

## 🔍 Validación de Código

### Type Checking con mypy
```bash
docker-compose exec web mypy apps/
```

### Formateo con black
```bash
docker-compose exec web black .
```

### Verificar formateo
```bash
docker-compose exec web black --check .
```

### Linting con flake8
```bash
docker-compose exec web flake8 .
```

### Ordenar imports
```bash
docker-compose exec web isort .
```

## 🛠️ Desarrollo

### Crear una nueva app

1. **Crear estructura de directorios**
   ```bash
   mkdir -p apps/myapp/{domain,application,infrastructure,interfaces}
   touch apps/myapp/{__init__.py,apps.py}
   touch apps/myapp/domain/__init__.py
   touch apps/myapp/application/__init__.py
   touch apps/myapp/infrastructure/__init__.py
   touch apps/myapp/interfaces/__init__.py
   ```

2. **Implementar capas siguiendo Clean Architecture**
   - Domain: Entidades y lógica de negocio
   - Application: Ports, DTOs, Use Cases
   - Infrastructure: Models, Repositories
   - Interfaces: Serializers, ViewSets, URLs

3. **Registrar app en `config/settings.py`**
   ```python
   INSTALLED_APPS = [
       ...
       "apps.myapp",
   ]
   ```

4. **Crear URLs en `config/urls.py`**
   ```python
   path("api/v1/myapp/", include("apps.myapp.interfaces.urls")),
   ```

### Ejecutar Django Management Commands

```bash
# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Shell interactivo
docker-compose exec web python manage.py shell

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

### Acceso a la base de datos

```bash
# PostgreSQL CLI
docker-compose exec db psql -U postgres -d pazzo

# Desde el contenedor web
docker-compose exec web python manage.py dbshell
```

## 📦 Gestión de Dependencias

### Agregar nueva dependencia

1. Añadir al `requirements.txt`
2. Reconstruir imagen:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### Congelar dependencias actuales

```bash
docker-compose exec web pip freeze > requirements.txt
```

## 🐳 Docker Commands

```bash
# Levantar servicios
docker-compose up

# Levantar en background
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ borra la DB)
docker-compose down -v

# Reconstruir imágenes
docker-compose build

# Ejecutar comando en contenedor
docker-compose exec web <comando>
```

## 🔐 Variables de Entorno

Principales variables en `.env`:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `DEBUG` | Modo debug de Django | `True` |
| `SECRET_KEY` | Secret key de Django | `change-this` |
| `DB_NAME` | Nombre de base de datos | `pazzo` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `postgres` |
| `DB_HOST` | Host de PostgreSQL | `db` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | Duración token access | `15` |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | Duración token refresh | `7` |
| `CORS_ALLOWED_ORIGINS` | Orígenes CORS permitidos | `http://localhost:3000` |

## 📚 Documentación Adicional

- [Arquitectura Clean Architecture](docs/architecture.md)
- Swagger/OpenAPI (próximamente)

## 🤝 Contribución

1. Seguir estrictamente Clean Architecture
2. Usar type hints en todo el código Python
3. Escribir tests para nuevas funcionalidades
4. Ejecutar `black`, `flake8`, y `mypy` antes de commit
5. Mantener cobertura de tests > 80%

## 📝 Notas

- **JWT Tokens**: Access tokens expiran en 15 minutos, refresh tokens en 7 días
- **Type Hints**: Obligatorios en todo el código, validados con mypy strict mode
- **Tests**: Organizados en unit (sin Django), integration (con DB), y e2e (API completa)
- **Clean Architecture**: Dominio independiente de frameworks, use cases explícitos, repository pattern

## 🐛 Troubleshooting

### El contenedor web no inicia
```bash
# Ver logs
docker-compose logs web

# Verificar que PostgreSQL esté healthy
docker-compose ps
```

### Error de conexión a base de datos
```bash
# Verificar que el servicio db esté corriendo
docker-compose ps db

# Reiniciar servicios
docker-compose restart
```

### Tests fallan
```bash
# Limpiar cache de pytest
docker-compose exec web pytest --cache-clear

# Recrear base de datos de tests
docker-compose exec web python manage.py flush --noinput
```

## 📄 Licencia

[Tu licencia aquí]

## 👥 Contacto

[Tu información de contacto]
