"""
Contenedor de Inyección de Dependencias para el feature de Auth
"""
from functools import lru_cache
from src.features.auth.domain.ports.Iuser_repository import UserRepositoryPort
from src.features.auth.infrastructure.user_repository import UserRepository
from src.features.auth.application.uses_cases.register_user import RegisterUserUseCase
from src.features.auth.application.uses_cases.authenticate_user import AuthenticateUserUseCase


class AuthDependencyContainer:
    """
    Contenedor que gestiona todas las dependencias del módulo de autenticación.
    Implementa el patrón Singleton para asegurar una única instancia.
    """
    _instance = None
    _user_repository: UserRepositoryPort = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_user_repository(self) -> UserRepositoryPort:
        """
        Retorna la instancia del repositorio de usuarios.
        Implementa lazy loading para crear la instancia solo cuando se necesita.
        """
        if self._user_repository is None:
            self._user_repository = UserRepository()
        return self._user_repository
    
    def get_register_user_use_case(self) -> RegisterUserUseCase:
        """
        Retorna una instancia del caso de uso de registro de usuario
        con sus dependencias inyectadas.
        """
        return RegisterUserUseCase(user_repository=self.get_user_repository())
    
    def get_authenticate_user_use_case(self) -> AuthenticateUserUseCase:
        """
        Retorna una instancia del caso de uso de autenticación de usuario
        con sus dependencias inyectadas.
        """
        return AuthenticateUserUseCase(user_repository=self.get_user_repository())


# Función helper para FastAPI Depends
@lru_cache()
def get_dependency_container() -> AuthDependencyContainer:
    """
    Función helper para usar con FastAPI Depends().
    El decorador lru_cache asegura que siempre retorne la misma instancia.
    """
    return AuthDependencyContainer()


# Funciones de dependencia para FastAPI
def get_user_repository_dependency() -> UserRepositoryPort:
    """Dependencia para inyectar el repositorio de usuarios"""
    container = get_dependency_container()
    return container.get_user_repository()


def get_register_user_use_case_dependency() -> RegisterUserUseCase:
    """Dependencia para inyectar el caso de uso de registro"""
    container = get_dependency_container()
    return container.get_register_user_use_case()


def get_authenticate_user_use_case_dependency() -> AuthenticateUserUseCase:
    """Dependencia para inyectar el caso de uso de autenticación"""
    container = get_dependency_container()
    return container.get_authenticate_user_use_case()