# Diagramas de Arquitectura - Inyección de Dependencias

## 1. Arquitectura Hexagonal Completa

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │          controller_user.py (FastAPI Router)              │  │
│  │                                                             │  │
│  │  @router.post("/register")                                │  │
│  │  def register_user(                                       │  │
│  │      use_case = Depends(get_register_user_use_case_dependency) │
│  │  )                                                         │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└─────────────────────────┼─────────────────────────────────────────┘
                          │ Depends()
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DEPENDENCY INJECTION LAYER                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │            dependency_injection.py                        │  │
│  │                                                             │  │
│  │  class AuthDependencyContainer:                           │  │
│  │      def get_register_user_use_case() → RegisterUserUseCase │
│  │      def get_authenticate_user_use_case() → AuthenticateUserUseCase │
│  │      def get_user_repository() → UserRepositoryPort       │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└─────────────────────────┼─────────────────────────────────────────┘
                          │ Inyecta
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                           │
│  ┌──────────────────────────────┐  ┌─────────────────────────┐ │
│  │  register_user.py            │  │ authenticate_user.py    │ │
│  │                              │  │                         │ │
│  │  class RegisterUserUseCase:  │  │ class AuthenticateUser: │ │
│  │    def __init__(             │  │   def __init__(         │ │
│  │      user_repository: Port   │  │     user_repository     │ │
│  │    )                         │  │   )                     │ │
│  └────────────┬─────────────────┘  └────────┬────────────────┘ │
└─────────────────┼──────────────────────────────┼─────────────────┘
                  │                              │
                  └──────────┬───────────────────┘
                             │ Usa
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DOMAIN LAYER                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  Iuser_repository.py (PORT)               │  │
│  │                                                             │  │
│  │  class UserRepositoryPort(ABC):                           │  │
│  │      @abstractmethod                                      │  │
│  │      def create_user(user: User) → User                   │  │
│  │                                                             │  │
│  │      @abstractmethod                                      │  │
│  │      def get_user_by_email(email: str) → Optional[User]   │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└─────────────────────────┼─────────────────────────────────────────┘
                          │ Implementa
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │     user_repository.py (ADAPTER - Implementación)         │  │
│  │                                                             │  │
│  │  class UserRepository(UserRepositoryPort):                │  │
│  │      def create_user(user: User) → User:                  │  │
│  │          # Lógica de base de datos                        │  │
│  │                                                             │  │
│  │      def get_user_by_email(email: str) → Optional[User]:  │  │
│  │          # Consulta SQL                                   │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└─────────────────────────┼─────────────────────────────────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │   DATABASE   │
                   └──────────────┘
```

## 2. Flujo de Inyección de Dependencias

```
[Usuario hace POST /auth/register]
           │
           ▼
┌──────────────────────────────────┐
│  FastAPI detecta Depends()       │
│  en el parámetro use_case        │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  Llama a:                                     │
│  get_register_user_use_case_dependency()     │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  AuthDependencyContainer                      │
│  .get_register_user_use_case()               │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  Container llama:                             │
│  .get_user_repository()                      │
│  para obtener UserRepository                 │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  Crea instancia:                              │
│  RegisterUserUseCase(                        │
│      user_repository=UserRepository()        │
│  )                                           │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  FastAPI inyecta el use_case                 │
│  en el parámetro de la función               │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  Ejecuta: use_case.execute(user_data)       │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  UseCase usa el repositorio inyectado        │
│  para crear el usuario en la DB              │
└──────────┬───────────────────────────────────┘
           │
           ▼
     [Respuesta al usuario]
```

## 3. Comparación: ANTES vs DESPUÉS

### ANTES (Sin Inyección de Dependencias)

```
controller_user.py
    │
    ├─► RegisterUserUseCase()
    │       │
    │       └─► UserRepository() ❌ Dependencia dura
    │
    └─► AuthenticateUserUseCase()
            │
            └─► UserRepository() ❌ Dependencia dura

Problemas:
- Difícil de testear
- Acoplamiento fuerte
- No se puede cambiar fácilmente la implementación
```

### DESPUÉS (Con Inyección de Dependencias)

```
controller_user.py
    │
    ├─► Depends(get_register_user_use_case_dependency)
    │       │
    │       └─► DependencyContainer
    │               │
    │               └─► RegisterUserUseCase(UserRepositoryPort) ✅
    │                       │
    │                       └─► UserRepository implements Port ✅
    │
    └─► Depends(get_authenticate_user_use_case_dependency)
            │
            └─► DependencyContainer
                    │
                    └─► AuthenticateUserUseCase(UserRepositoryPort) ✅
                            │
                            └─► UserRepository implements Port ✅

Ventajas:
✓ Fácil de testear (inyectar mocks)
✓ Bajo acoplamiento
✓ Flexible (cambiar implementaciones)
✓ Mantenible
```

## 4. Diagrama de Testing con Mocks

```
┌─────────────────────────────────────┐
│       test_register_user.py         │
│                                     │
│  def test_register_user():          │
│      mock_repo = Mock()             │
│      mock_repo.create_user = ...    │
│                                     │
│      use_case = RegisterUserUseCase(│
│          user_repository=mock_repo  │ ✅ Inyección de Mock
│      )                              │
│                                     │
│      result = use_case.execute(...)│
│                                     │
│      assert result is not None     │
└─────────────────────────────────────┘
           │
           ▼
    ┌─────────────┐
    │  Mock Repo  │ (No toca la DB real)
    └─────────────┘

Sin inyección de dependencias, esto sería imposible
porque el UseCase crearía UserRepository() internamente
```

## 5. Patrón Singleton del Container

```
Primera llamada:
┌──────────────────────────────────┐
│ get_dependency_container()       │
│   ↓                              │
│ ¿Container existe?               │
│   NO → Crear nuevo Container     │
│   Cache con @lru_cache()         │
└──────────────────────────────────┘

Llamadas posteriores:
┌──────────────────────────────────┐
│ get_dependency_container()       │
│   ↓                              │
│ ¿Container existe?               │
│   SÍ → Retornar Container         │
│   existente del cache            │
└──────────────────────────────────┘

Resultado: Una única instancia en toda la aplicación
```

## 6. Estructura de Archivos Actualizada

```
src/features/auth/
│
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── user.py .......................... [No cambia]
│   └── ports/
│       ├── __init__.py
│       └── Iuser_repository.py .............. [No cambia]
│
├── application/
│   ├── __init__.py
│   └── uses_cases/
│       ├── __init__.py
│       ├── register_user.py ................. [ACTUALIZAR ⚡]
│       └── authenticate_user.py ............. [ACTUALIZAR ⚡]
│
├── infrastructure/
│   ├── __init__.py
│   ├── user_repository.py ................... [No cambia]
│   └── auth_utils.py ........................ [ACTUALIZAR ⚡]
│
├── presentation/
│   ├── __init__.py
│   └── controller_user.py ................... [ACTUALIZAR ⚡]
│
├── __init__.py
└── dependency_injection.py .................. [NUEVO ⭐]
```

## 7. Ciclo de Vida de las Dependencias

```
┌───────────────────────────────────────────────────────┐
│              Inicio de la Aplicación                   │
└──────────────────────┬────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────┐
│  AuthDependencyContainer se crea (Singleton)          │
│  - Una sola vez                                       │
│  - Se mantiene durante toda la ejecución              │
└──────────────────────┬────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────┐
│  Por cada Request HTTP:                               │
│                                                        │
│  1. FastAPI detecta Depends()                         │
│  2. Llama a get_xxx_dependency()                      │
│  3. Container crea instancia del UseCase              │
│  4. UseCase recibe repositorio inyectado              │
│  5. Ejecuta lógica de negocio                         │
│  6. Retorna resultado                                 │
└──────────────────────┬────────────────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────────────────┐
│  FastAPI limpia recursos del request                  │
│  (Container sigue existiendo para próximos requests)  │
└───────────────────────────────────────────────────────┘
```
