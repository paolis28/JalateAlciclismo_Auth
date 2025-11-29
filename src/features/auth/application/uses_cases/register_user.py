import cloudinary
import cloudinary.uploader
from src.features.auth.domain.entities.user import User
from src.features.auth.domain.ports.Iuser_repository import UserRepositoryPort

# cloudinary.config(
#     cloud_name="dfuajei2k",
#     api_key="782294236213671",
#     api_secret="_Qd4Z_FD3Z_Lb897PAGptEP7Eds"
# )

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepositoryPort):
        """
        Inicializa el caso de uso con inyección de dependencias.
        
        Args:
            user_repository: Implementación del puerto UserRepositoryPort
        """
        self.user_repo = user_repository

    def execute(self, user_data: User, url_foto=None):

        # Subir imagen correctamente si existe
        if url_foto:
            try:
                print("Subiendo imagen a Cloudinary...")
                # upload_result = cloudinary.uploader.upload(
                #     file.file,                # se pasa el archivo como stream
                #     folder="usuarios",
                #     public_id=user_data.correo.split("@")[0],  # opcional
                #     overwrite=True,
                #     resource_type="image"
                # )
                # url_foto = upload_result.get("secure_url")
            except Exception as e:
                print("Error al subir imagen a Cloudinary:", e)
                url_foto = None

        # Verificar si el usuario ya existe
        existing_user = self.user_repo.get_user_by_email(user_data.correo)
        if existing_user:
            raise Exception("El correo ya está registrado")

        user_data.url_foto = url_foto
        return self.user_repo.create_user(user_data)