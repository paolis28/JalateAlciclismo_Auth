from sqlalchemy.orm import Session
from sqlalchemy import text
from src.features.auth.domain.entities.user import User
from src.features.auth.domain.ports.Iuser_repository import UserRepositoryPort
from src.features.db.db_config import engine
from passlib.hash import bcrypt

class UserRepository(UserRepositoryPort):
    def create_user(self, user: User) -> User:
        hashed_password = bcrypt.hash(user.contrasena)
        with engine.connect() as conn:
            query = text("""
                INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, correo, contrasena, url_foto)
                VALUES (:nombre, :apellido_paterno, :apellido_materno, :correo, :contrasena, :url_foto)
            """)
            conn.execute(query, {
                "nombre": user.nombre,
                "apellido_paterno": user.apellido_paterno,
                "apellido_materno": user.apellido_materno,
                "correo": user.correo,
                "contrasena": hashed_password,
                "url_foto": user.url_foto
            })
            conn.commit()
        return user

    def get_user_by_email(self, correo: str):
        with engine.connect() as conn:
            query = text("SELECT * FROM usuario WHERE correo = :email")
            result = conn.execute(query, {"email": correo}).first()
            return dict(result._mapping) if result else None