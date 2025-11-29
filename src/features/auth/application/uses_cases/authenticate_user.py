from datetime import datetime, timedelta
from jose import jwt
import bcrypt
from src.features.auth.domain.ports.Iuser_repository import UserRepositoryPort
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "123456789")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class AuthenticateUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort):
        self.user_repo = user_repository

    def execute(self, correo: str, contrasena: str):
        user = self.user_repo.get_user_by_email(correo)
        if not user or not bcrypt.checkpw(contrasena.encode('utf-8'), user["contrasena"].encode('utf-8')):
            raise Exception("Credenciales incorrectas")

        token_data = {
            "sub": user["correo"],
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}