import html
import re

def validate_password(password: str) -> tuple[bool, str]:
    """
    Valida: mínimo 8 caracteres, al menos una mayúscula, una minúscula y un número.
    Retorna un booleano y un mensaje de error.
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r"[a-z]", password):
        return False, "La contraseña debe contener al menos una letra minúscula."
    if not re.search(r"[0-9]", password):
        return False, "La contraseña debe contener al menos un número."
    
    return True, "Contraseña válida."

def sanitize_input(raw_input: str) -> str:
    """
    Limpia la entrada del usuario previniendo XSS e inyecciones SQL básicas.
    """
    if not raw_input:
        return ""

    # 1. Escapar caracteres HTML/XML para prevenir XSS
    safe_text = html.escape(raw_input)
    
    # 2. Limpieza de espacios en blanco múltiples
    safe_text = re.sub(r'\s+', ' ', safe_text).strip()
    
    # 3. Bloqueo de sentencias SQL (Prevención en capa Frontend)
    sql_patterns = [
        r'(?i)\bdrop\b', 
        r'(?i)\bdelete\b', 
        r'(?i)\btruncate\b', 
        r'(?i)\bunion\b',
        r'--', 
        r';'
    ]
    for pattern in sql_patterns:
         safe_text = re.sub(pattern, '[BLOQUEADO]', safe_text)

    return safe_text