from datetime import datetime, timedelta
from jose import jwt
from src.core.config import settings
from passlib.context import CryptContext
from typing import Optional
import re

# Configuración del contexto de criptografía
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Número de rondas para bcrypt (mayor = más seguro pero más lento)
)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Crea un token JWT de acceso.
    
    Args:
        data (dict): Datos a incluir en el token
        expires_delta (timedelta, optional): Tiempo de expiración personalizado
        
    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_access_token(token: str) -> Optional[dict]:
    """
    Verifica y decodifica un token JWT.
    
    Args:
        token (str): Token JWT a verificar
        
    Returns:
        Optional[dict]: Datos del token si es válido, None en caso contrario
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando bcrypt.
    
    Args:
        password (str): Contraseña en texto plano
        
    Returns:
        str: Hash de la contraseña
        
    Raises:
        ValueError: Si la contraseña está vacía o es None
    """
    if not password or not password.strip():
        raise ValueError("La contraseña no puede estar vacía")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su hash.
    
    Args:
        plain_password (str): Contraseña en texto plano
        hashed_password (str): Hash de la contraseña almacenado
        
    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    if not plain_password or not hashed_password:
        return False
    
    return pwd_context.verify(plain_password, hashed_password)

def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Valida la fortaleza de una contraseña.
    
    Args:
        password (str): Contraseña a validar
        
    Returns:
        tuple[bool, Optional[str]]: (es_válida, mensaje_error)
    """
    if not password:
        return False, "La contraseña no puede estar vacía"
    
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if len(password) > 128:
        return False, "La contraseña no puede exceder 128 caracteres"
    
    # Verificar que contenga al menos una letra minúscula
    if not re.search(r"[a-z]", password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    # Verificar que contenga al menos una letra mayúscula
    if not re.search(r"[A-Z]", password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    # Verificar que contenga al menos un número
    if not re.search(r"\d", password):
        return False, "La contraseña debe contener al menos un número"
    
    # Verificar que contenga al menos un carácter especial
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, None

def hash_password_with_validation(password: str) -> tuple[str, Optional[str]]:
    """
    Valida y hashea una contraseña en una sola operación.
    
    Args:
        password (str): Contraseña a validar y hashear
        
    Returns:
        tuple[str, Optional[str]]: (hash, mensaje_error)
    """
    is_valid, error_message = validate_password_strength(password)
    
    if not is_valid:
        return "", error_message
    
    try:
        hashed = hash_password(password)
        return hashed, None
    except Exception as e:
        return "", f"Error al hashear la contraseña: {str(e)}"