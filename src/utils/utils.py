"""
Utilidades generales para la aplicación.
"""
import re
import uuid
from datetime import datetime, timezone
from typing import Optional, Any
from email_validator import validate_email, EmailNotValidError

def generate_uuid() -> str:
    """
    Genera un UUID único.
    
    Returns:
        str: UUID generado
    """
    return str(uuid.uuid4())

def is_valid_email(email: str) -> bool:
    """
    Valida si un email tiene formato válido.
    
    Args:
        email (str): Email a validar
        
    Returns:
        bool: True si el email es válido, False en caso contrario
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def sanitize_string(text: str) -> str:
    """
    Sanitiza una cadena de texto eliminando caracteres peligrosos.
    
    Args:
        text (str): Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    if not text:
        return ""
    
    # Eliminar caracteres de control y espacios extra
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    return sanitized

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Formatea una fecha/hora en string.
    
    Args:
        dt (datetime): Fecha/hora a formatear
        format_str (str): Formato deseado
        
    Returns:
        str: Fecha/hora formateada
    """
    if not dt:
        return ""
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.strftime(format_str)

def parse_datetime(date_string: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
    """
    Parsea una cadena de fecha/hora a datetime.
    
    Args:
        date_string (str): Cadena de fecha/hora
        format_str (str): Formato esperado
        
    Returns:
        Optional[datetime]: Fecha/hora parseada o None si falla
    """
    try:
        return datetime.strptime(date_string, format_str)
    except (ValueError, TypeError):
        return None

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Trunca un texto a una longitud máxima.
    
    Args:
        text (str): Texto a truncar
        max_length (int): Longitud máxima
        suffix (str): Sufijo a agregar si se trunca
        
    Returns:
        str: Texto truncado
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def safe_get_nested(data: dict, *keys, default: Any = None) -> Any:
    """
    Obtiene un valor de un diccionario anidado de forma segura.
    
    Args:
        data (dict): Diccionario a consultar
        *keys: Claves anidadas
        default: Valor por defecto si no se encuentra
        
    Returns:
        Any: Valor encontrado o default
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def is_valid_phone(phone: str) -> bool:
    """
    Valida si un número de teléfono tiene formato válido.
    
    Args:
        phone (str): Número de teléfono a validar
        
    Returns:
        bool: True si el teléfono es válido, False en caso contrario
    """
    if not phone:
        return False
    
    # Patrón básico para números de teléfono (puede ajustarse según país)
    pattern = r'^\+?[\d\s\-\(\)]{7,15}$'
    return bool(re.match(pattern, phone))

def normalize_string(text: str) -> str:
    """
    Normaliza una cadena de texto (lowercase, sin espacios extra).
    
    Args:
        text (str): Texto a normalizar
        
    Returns:
        str: Texto normalizado
    """
    if not text:
        return ""
    
    return re.sub(r'\s+', ' ', text.lower().strip())
