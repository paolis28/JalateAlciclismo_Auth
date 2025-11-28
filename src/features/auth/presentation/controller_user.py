from fastapi import APIRouter, UploadFile, Form, Depends
from src.features.auth.domain.entities.user import User
from src.features.auth.application.uses_cases.register_user import RegisterUserUseCase
from src.features.auth.application.uses_cases.authenticate_user import AuthenticateUserUseCase
from src.features.auth.dependency import (
    get_register_user_use_case_dependency,
    get_authenticate_user_use_case_dependency
)

router = APIRouter(prefix="/auth/v1", tags=["Auth"])


@router.post("/register")
async def register_user(
    nombre: str = Form(...),
    apellido_paterno: str = Form(None),
    apellido_materno: str = Form(None),
    correo: str = Form(...),
    contrasena: str = Form(...),
    file: UploadFile = None,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case_dependency)
):
    user = User(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        correo=correo,
        contrasena=contrasena
    )

    result = use_case.execute(user, file)
    return {"message": "Usuario registrado correctamente", "data": result}


@router.post("/login")
async def login_user(
    correo: str = Form(...),
    contrasena: str = Form(...),
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case_dependency)
):
    """
    Endpoint para autenticar un usuario y obtener un token JWT.
    
    Args:
        correo: Correo electrónico del usuario
        contrasena: Contraseña del usuario
        use_case: Caso de uso inyectado automáticamente por FastAPI
        
    Returns:
        dict: Token de acceso y tipo de token
    """
    token = use_case.execute(correo, contrasena)
    return token