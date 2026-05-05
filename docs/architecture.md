# Clean Architecture en Pazzo Backend

## Introducción

Este documento explica la implementación de Clean Architecture con Domain-Driven Design en el backend de Pazzo.

## ¿Qué es Clean Architecture?

Clean Architecture es un patrón de diseño de software que separa el código en capas concéntricas, donde las capas internas no conocen las capas externas. Esto permite:

- **Independencia de frameworks**: La lógica de negocio no depende de Django, DRF, etc.
- **Testabilidad**: Se pueden probar casos de uso sin bases de datos o APIs
- **Independencia de UI**: La lógica de negocio no sabe si es usada por REST, GraphQL, CLI, etc.
- **Independencia de base de datos**: Se puede cambiar PostgreSQL por MongoDB sin afectar la lógica
- **Mantenibilidad**: Código organizado y fácil de entender

## Capas de la Arquitectura

### 1. Domain Layer (Capa de Dominio)

**Ubicación**: `apps/<app>/domain/`

**Responsabilidad**: Contiene las reglas de negocio puras.

**Características**:
- Sin dependencias de frameworks (puro Python)
- Entidades de negocio (dataclasses)
- Excepciones de dominio
- Lógica de negocio fundamental

**Ejemplo**:
```python
# apps/users/domain/entities.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    email: str
    password_hash: str
    is_active: bool = True
    id: Optional[int] = None
    
    def verify_password(self, raw_password: str) -> bool:
        # Lógica de negocio
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password_hash)
```

**Reglas**:
- ✅ Solo Python estándar y dataclasses
- ✅ Lógica de negocio pura
- ❌ No importar Django, DRF, SQLAlchemy, etc.
- ❌ No acceso directo a base de datos

### 2. Application Layer (Capa de Aplicación)

**Ubicación**: `apps/<app>/application/`

**Responsabilidad**: Orquesta la lógica de negocio mediante casos de uso.

**Componentes**:

#### Ports (Interfaces)
Define contratos que la infraestructura debe implementar:

```python
# apps/users/application/ports.py
from abc import ABC, abstractmethod
from typing import Optional
from ..domain.entities import User

class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save(self, user: User) -> User:
        pass
```

#### DTOs (Data Transfer Objects)
Objetos para transferir datos entre capas:

```python
# apps/users/application/dtos.py
from dataclasses import dataclass

@dataclass
class UserInputDTO:
    email: str
    password: str

@dataclass
class UserOutputDTO:
    id: int
    email: str
    is_active: bool
```

#### Use Cases (Casos de Uso)
Servicios que implementan operaciones de negocio:

```python
# apps/users/application/services.py
from .ports import UserRepository
from .dtos import UserInputDTO, UserOutputDTO
from ..domain.entities import User

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
    
    def execute(self, input_dto: UserInputDTO) -> UserOutputDTO:
        # Orquestar lógica de negocio
        if self.user_repository.exists_by_email(input_dto.email):
            raise UserAlreadyExistsException(input_dto.email)
        
        user = User(
            email=input_dto.email,
            password_hash=make_password(input_dto.password),
        )
        
        saved_user = self.user_repository.save(user)
        return UserOutputDTO.from_entity(saved_user)
```

**Reglas**:
- ✅ Definir interfaces (ports) para dependencias externas
- ✅ DTOs para comunicación entre capas
- ✅ Use cases explícitos y testeables
- ❌ No conocer detalles de implementación (ORM, HTTP, etc.)

### 3. Infrastructure Layer (Capa de Infraestructura)

**Ubicación**: `apps/<app>/infrastructure/`

**Responsabilidad**: Implementa los detalles técnicos y adapta tecnologías externas.

**Componentes**:

#### Models (Modelos ORM)
Representación de persistencia:

```python
# apps/users/infrastructure/models.py
from django.db import models

class UserModel(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'
```

#### Repositories (Implementación)
Implementa los ports definidos en Application:

```python
# apps/users/infrastructure/repositories.py
from ..application.ports import UserRepository
from ..domain.entities import User
from .models import UserModel

class DjangoUserRepository(UserRepository):
    def find_by_email(self, email: str) -> Optional[User]:
        try:
            user_model = UserModel.objects.get(email=email)
            return self._to_entity(user_model)
        except UserModel.DoesNotExist:
            return None
    
    def save(self, user: User) -> User:
        if user.id:
            user_model = UserModel.objects.get(id=user.id)
            # Update...
        else:
            user_model = UserModel.objects.create(...)
        
        return self._to_entity(user_model)
    
    @staticmethod
    def _to_entity(model: UserModel) -> User:
        # Convertir ORM model a domain entity
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
        )
```

**Reglas**:
- ✅ Implementar ports de Application
- ✅ Convertir entre modelos ORM y entidades de dominio
- ✅ Manejar detalles de persistencia
- ❌ No exponer detalles de ORM a capas superiores

### 4. Interfaces Layer (Capa de Interfaces)

**Ubicación**: `apps/<app>/interfaces/`

**Responsabilidad**: Expone la aplicación al mundo exterior (API REST, CLI, etc.).

**Componentes**:

#### Serializers
Validan y transforman datos HTTP:

```python
# apps/users/interfaces/serializers.py
from rest_framework import serializers
from ..application.services import RegisterUserUseCase
from ..application.dtos import UserInputDTO

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    
    def create(self, validated_data):
        input_dto = UserInputDTO(**validated_data)
        
        use_case = RegisterUserUseCase(repository=DjangoUserRepository())
        user_dto = use_case.execute(input_dto)
        
        return user_dto
```

#### ViewSets
Manejan requests HTTP y delegan a use cases:

```python
# apps/users/interfaces/viewsets.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user_dto = serializer.save()
            return Response(
                UserSerializer(user_dto).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

**Reglas**:
- ✅ Validar datos de entrada
- ✅ Delegar a use cases
- ✅ Manejar códigos HTTP y respuestas
- ❌ No lógica de negocio aquí

## Flujo de Datos

```
HTTP Request
    ↓
[ViewSet] - Valida request
    ↓
[Serializer] - Transforma a DTO
    ↓
[Use Case] - Ejecuta lógica de negocio
    ↓
[Repository] - Accede a datos
    ↓
[ORM Model] ← → Database
    ↓
[Entity] - Regresa al Use Case
    ↓
[DTO] - Transforma para respuesta
    ↓
[Serializer] - Formatea JSON
    ↓
HTTP Response
```

## Dependency Rule (Regla de Dependencias)

```
┌─────────────────────────────────────┐
│         Interfaces Layer            │  ← Solo conoce Application
│  (ViewSets, Serializers, URLs)      │
├─────────────────────────────────────┤
│      Infrastructure Layer           │  ← Solo conoce Application & Domain
│  (Models, Repositories, Adapters)   │
├─────────────────────────────────────┤
│       Application Layer             │  ← Solo conoce Domain
│   (Ports, DTOs, Use Cases)          │
├─────────────────────────────────────┤
│          Domain Layer               │  ← No conoce a nadie
│   (Entities, Exceptions)            │
└─────────────────────────────────────┘
```

**Regla de Oro**: Las dependencias solo apuntan hacia adentro, nunca hacia afuera.

## Beneficios en Pazzo

### 1. Testabilidad

**Tests Unitarios** (Domain/Application) sin Django:
```python
def test_user_verify_password():
    user = User(email="test@test.com", password_hash=make_password("pass"))
    assert user.verify_password("pass") is True
```

**Tests de Integración** (Infrastructure) con DB:
```python
@pytest.mark.django_db
def test_repository_saves_user():
    repo = DjangoUserRepository()
    user = User(email="test@test.com", password_hash="hash")
    saved = repo.save(user)
    assert saved.id is not None
```

**Tests E2E** (Interfaces) API completa:
```python
def test_register_endpoint(api_client):
    response = api_client.post('/api/v1/users/register/', {...})
    assert response.status_code == 201
```

### 2. Cambio de Tecnología Sin Dolor

Cambiar PostgreSQL → MongoDB:
- ✅ Domain: Sin cambios
- ✅ Application: Sin cambios
- ⚠️ Infrastructure: Nueva implementación de Repository
- ✅ Interfaces: Sin cambios

### 3. Múltiples Interfaces

Puedes agregar GraphQL, gRPC, CLI sin tocar la lógica de negocio:

```
Domain ← Application ← Infrastructure
                ↑           ↑
            REST API    GraphQL API
            CLI Tool    Background Jobs
```

## Type Hints y Clean Architecture

Usamos type hints estrictos en todas las capas:

```python
# Domain
@dataclass
class User:
    email: str
    password_hash: str
    
    def verify_password(self, raw_password: str) -> bool:
        ...

# Application
class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

# Infrastructure
class DjangoUserRepository(UserRepository):
    def find_by_email(self, email: str) -> Optional[User]:
        ...

# Interfaces
def register(self, request: Request) -> Response:
    ...
```

Esto permite:
- Detección temprana de errores
- Mejor autocomplete en IDEs
- Documentación viva del código
- Refactoring seguro

## Convenciones del Proyecto

### Naming

- **Entities**: Sustantivos singulares (`User`, `Passport`)
- **Use Cases**: Verbos imperativos (`RegisterUserUseCase`, `StampPassportUseCase`)
- **Repositories**: `<Entity>Repository` (`UserRepository`)
- **DTOs**: `<Entity>InputDTO`, `<Entity>OutputDTO`
- **Serializers**: `<Entity>Serializer`, `<Entity>RegistrationSerializer`
- **ViewSets**: `<Entity>ViewSet`

### Archivo Organization

```
apps/myapp/
├── domain/
│   ├── __init__.py
│   ├── entities.py         # Todas las entidades
│   └── exceptions.py       # Excepciones de dominio
├── application/
│   ├── __init__.py
│   ├── ports.py            # Todas las interfaces
│   ├── dtos.py             # Todos los DTOs
│   └── services.py         # Todos los use cases
├── infrastructure/
│   ├── __init__.py
│   ├── models.py           # Modelos ORM
│   ├── repositories.py     # Implementaciones de repositories
│   └── migrations/
└── interfaces/
    ├── __init__.py
    ├── serializers.py      # Serializers DRF
    ├── viewsets.py         # ViewSets
    └── urls.py             # URL routing
```

## Ejemplo Completo: Feature "Stamp Passport"

```python
# domain/entities.py
@dataclass
class Passport:
    user_id: int
    stamps: list[Stamp] = field(default_factory=list)
    
    def add_stamp(self, stamp: Stamp) -> None:
        if self.is_duplicate_stamp(stamp):
            raise DuplicateStampException()
        self.stamps.append(stamp)

# application/ports.py
class PassportRepository(ABC):
    @abstractmethod
    def find_by_user(self, user_id: int) -> Optional[Passport]:
        pass

# application/services.py
class StampPassportUseCase:
    def __init__(self, passport_repo: PassportRepository):
        self.passport_repo = passport_repo
    
    def execute(self, user_id: int, business_id: int) -> PassportDTO:
        passport = self.passport_repo.find_by_user(user_id)
        stamp = Stamp(business_id=business_id, timestamp=now())
        passport.add_stamp(stamp)
        saved = self.passport_repo.save(passport)
        return PassportDTO.from_entity(saved)

# infrastructure/repositories.py
class DjangoPassportRepository(PassportRepository):
    def find_by_user(self, user_id: int) -> Optional[Passport]:
        # Django ORM logic
        ...

# interfaces/viewsets.py
class PassportViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def stamp(self, request):
        use_case = StampPassportUseCase(DjangoPassportRepository())
        result = use_case.execute(user_id=request.user.id, ...)
        return Response(PassportSerializer(result).data)
```

## Referencias

- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design (Eric Evans)](https://www.domainlanguage.com/ddd/)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)

## Conclusión

Clean Architecture puede parecer más código inicialmente, pero ofrece:
- ✅ Código más mantenible y escalable
- ✅ Tests más fáciles de escribir
- ✅ Flexibilidad para cambiar tecnologías
- ✅ Separación clara de responsabilidades
- ✅ Equipos pueden trabajar en paralelo en diferentes capas

En Pazzo, esto nos permite evolucionar rápidamente agregando pasaportes, rutas ciclistas, y sellos sin romper código existente.
