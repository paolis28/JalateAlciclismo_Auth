from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from src.features.auth.domain.ports.Iuser_repository import UserRepositoryPort
from src.features.auth.dependency import get_user_repository_dependency

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "123456789")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: UserRepositoryPort = Depends(get_user_repository_dependency)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = repo.get_user_by_email(correo)
    if user is None:
        raise credentials_exception
    return user