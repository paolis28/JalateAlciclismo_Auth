from abc import ABC, abstractmethod
from typing import Optional
from src.features.auth.domain.entities.user import User

class UserRepositoryPort(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass
