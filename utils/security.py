import streamlit as st
from utils.api_client import obtener_perfil


def require_login(redirect_to="main.py"):
    """Verifica que exista una sesión válida en `st.session_state`.

    - Si el estado `logged_in` está presente y hay `access_token`, intenta
      obtener el perfil con `obtener_perfil`.
    - Si no hay sesión válida, limpia claves de sesión relevantes y
      redirige/forza la vista de login.

    Devuelve True si la sesión parece válida, False en caso contrario.
    """
    try:
        if st.session_state.get("logged_in"):
            access_token = st.session_state.get("access_token")
            if access_token:
                perfil = obtener_perfil(access_token)
                if perfil.get("success"):
                    st.session_state["user_profile"] = perfil["data"]
                    return True
        # Si llegamos aquí, no hay sesión válida
        for k in ["access_token", "refresh_token", "logged_in", "user_profile", "auth_view"]:
            st.session_state.pop(k, None)
        st.session_state["auth_view"] = "login"
        try:
            st.switch_page(redirect_to)
        except Exception:
            # En algunos contextos (tests o workers) switch_page puede fallar;
            # devolvemos False y las páginas deben llamar a `st.stop()` tras esto.
            pass
        return False
    except Exception:
        # En caso de cualquier error inesperado, limpiamos y rechazamos acceso
        for k in ["access_token", "refresh_token", "logged_in", "user_profile", "auth_view"]:
            st.session_state.pop(k, None)
        st.session_state["auth_view"] = "login"
        return False
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