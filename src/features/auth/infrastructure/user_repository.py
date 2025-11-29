from sqlalchemy.orm import Session
from sqlalchemy import text
from src.features.auth.domain.entities.user import User
from src.features.auth.domain.ports.Iuser_repository import UserRepositoryPort
from src.features.db.db_config import engine
import bcrypt

class UserRepository(UserRepositoryPort):
    def create_user(self, user: User) -> User:
        hashed_password = bcrypt.hashpw(user.contrasena.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        print("Hashed password:", hashed_password)
        with engine.connect() as conn:
            query = text("""
                INSERT INTO usuario (nombre, apellido_paterno, apellido_materno, contrasena, correo, url_foto)
                VALUES (:nombre, :apellido_paterno, :apellido_materno, :hashed_password, :correo, :url_foto)
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
            query = text("SELECT * FROM usuario WHERE correo = :correo")
            result = conn.execute(query, {"correo": correo}).first()
            return dict(result._mapping) if result else None