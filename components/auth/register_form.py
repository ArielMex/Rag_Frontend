import streamlit as st
import re
import html
from utils.images import get_image_base64
from utils.api_client import registrar_usuario, generar_username

try:
    from streamlit_oauth import OAuth2Component
except ImportError:
    OAuth2Component = None

try:
    import jwt
except ImportError:
    jwt = None

CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8501"

oauth2 = None
if OAuth2Component is not None:
    oauth2 = OAuth2Component(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        refresh_token_endpoint="https://oauth2.googleapis.com/token",
        revoke_token_endpoint="https://oauth2.googleapis.com/revoke"
    )

# --- FUNCIONES DE SEGURIDAD INTEGRADAS ---
def sanitize_input(raw_input: str) -> str:
    """Limpia la entrada del usuario previniendo XSS e inyecciones SQL básicas."""
    if not raw_input:
        return ""
    safe_text = html.escape(raw_input)
    safe_text = re.sub(r'\s+', ' ', safe_text).strip()
    sql_patterns = [r'(?i)\bdrop\b', r'(?i)\bdelete\b', r'(?i)\btruncate\b', r'(?i)\bunion\b', r'--', r';']
    for pattern in sql_patterns:
        safe_text = re.sub(pattern, '[BLOQUEADO]', safe_text)
    return safe_text

def validar_contrasena(password: str) -> tuple[bool, str]:
    """Evalúa la contraseña y devuelve exactamente qué requisitos faltan."""
    faltantes = []
    
    if len(password) < 8:
        faltantes.append("al menos 8 caracteres")
    if not re.search(r"[A-Z]", password):
        faltantes.append("una letra mayúscula")
    if not re.search(r"[a-z]", password):
        faltantes.append("una letra minúscula")
    if not re.search(r"[0-9]", password):
        faltantes.append("un número")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        faltantes.append("un carácter especial (ej. @, #, $, %)")
        
    if faltantes:
        mensaje = "A tu contraseña le falta: " + ", ".join(faltantes) + "."
        return False, mensaje
    
    return True, "Válida"
# -----------------------------------------

def render_register_form():
    st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(circle at 15% 30%, rgba(46, 184, 114, 0.15) 0%, transparent 40%),
                        radial-gradient(circle at 85% 80%, rgba(46, 184, 114, 0.1) 0%, transparent 40%);
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 2.5rem !important;
            background-color: #ffffff !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04) !important;
            border: 1px solid rgba(0,0,0,0.05) !important;
            padding: 1.5rem !important;
        }

        div[data-baseweb="input"] {
            border-radius: 0.8rem !important;
        }
        
        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button,
        .stMarkdown a button {
            border-radius: 2rem !important;
            padding: 0.5rem !important;
        }

        div[data-testid="stFormSubmitButton"] button[kind="primary"],
        div[data-testid="stButton"] button[kind="primary"] {
            font-weight: 600 !important;
            font-size: 16px !important;
        }

        /* BOTÓN DE GOOGLE Y SECUNDARIOS - Texto ligero y pequeño */
        div[data-testid="stButton"] button[kind="secondary"],
        .stMarkdown a button {
            font-weight: 400 !important;
            font-size: 14px !important;
            color: #4b5563 !important;
        }
        
        .btn-link button {
            background: transparent !important;
            border: none !important;
            color: #2eb872 !important;
            box-shadow: none !important;
            font-weight: 400 !important;
            font-size: 14px !important;
        }
        .btn-link button:hover {
            text-decoration: underline !important;
        }
    </style>
    """, unsafe_allow_html=True)

    icono_logo = get_image_base64("assets/icons/graduacion.png")

    st.write("") 
    st.write("") 
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    
    with col_center:
        # Lógica de Google prioritaria en registro
        if oauth2 is not None and jwt is not None:
            result = oauth2.authorize_button(
                name="Registrarse con Google",
                icon="https://www.google.com.br/favicon.ico",
                redirect_uri=REDIRECT_URI,
                scope="openid email profile",
                key="google_register",
                extras_params={"prompt": "consent", "access_type": "offline"},
                use_container_width=True
            )
            if result and "token" in result:
                id_token = result["token"]["id_token"]
                user_info = jwt.decode(id_token, options={"verify_signature": False})

                st.session_state.logged_in = True
                st.session_state.user_email = user_info.get("email")
                st.session_state.user_name = user_info.get("name")
                st.rerun()

        with st.container(border=True):
            
            if icono_logo:
                st.markdown(f"""
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(46,184,114,0.3);'>
                            <img src="{icono_logo}" style="width: 32px; height: 32px; object-fit: contain;">
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;'>
                            🎓
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<h2 style='text-align: center; font-weight: 700; font-size: 24px; margin-bottom: 5px;'>Crea tu cuenta de LuminIA</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 25px;'>Únete a miles de estudiantes que aprenden de forma más eficaz gracias a la IA.</p>", unsafe_allow_html=True)
            
            with st.form("register_form", border=False):
                st.markdown("Nombre")
                name = st.text_input("Full Name", placeholder="Josue Abraham", label_visibility="collapsed")

                st.markdown("<div style='margin-top: 10px;'>Correo</div>", unsafe_allow_html=True)
                email = st.text_input("Email", placeholder="ejemplo@correo.edu.mx", label_visibility="collapsed")
                
                st.markdown("<div style='margin-top: 10px;'>Contraseña</div>", unsafe_allow_html=True)
                password = st.text_input("Password", placeholder="Crea una contraseña", type="password", label_visibility="collapsed")
                
                st.markdown("<div style='margin-top: 10px;'>Confirmar Contraseña</div>", unsafe_allow_html=True)
                confirm = st.text_input("Confirm Password", placeholder="Vuelve a escribir tu contraseña", type="password", label_visibility="collapsed")
                
                st.write("")
                
                submitted = st.form_submit_button("Crear cuenta", use_container_width=True, type="primary")
                
                if submitted:
                    safe_name = sanitize_input(name)
                    safe_email = sanitize_input(email)
                    
                    is_valid, error_msg = validar_contrasena(password)
                    
                    if not safe_name or not safe_email or not password:
                        st.error("Favor de llenar todos los campos.")
                    elif not is_valid:
                        st.error(error_msg)
                    elif password != confirm:
                        st.error("Las contraseñas no coinciden.")
                    else:
                        # API de Backend Integrada (Resolución de conflicto)
                        username_generado = generar_username(safe_name)
                        payload = {
                            "email": safe_email,
                            "username": username_generado,
                            "full_name": safe_name,
                            "password": password
                        }
                        resultado = registrar_usuario(payload)

                        if resultado["success"]:
                            st.success("¡La cuenta se ha creado correctamente! Ya puedes iniciar sesión.")
                            st.session_state.auth_view = "login"
                            st.rerun()
                        else:
                            st.error(resultado["error"])
            
            # --- Divider con el "or" ---
            st.markdown("""
                <div style='display: flex; align-items: center; text-align: center; margin: 5px 0 15px 0;'>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                    <span style='padding: 0 10px; color: #9ca3af; font-size: 12px;'>o</span>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                </div>
            """, unsafe_allow_html=True)
            
            if oauth2 is None:
                st.link_button(
                    "Registrarse con Google",
                    "",
                    use_container_width=True
                )
            
            st.markdown("""
                <div style='text-align: center; font-size: 14px; margin-top: 15px;'>
                    <span style='color: #6b7280;'>¿Ya tienes una cuenta? </span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="btn-link">', unsafe_allow_html=True)
            if st.button("Iniciar Sesion", use_container_width=True):
                st.session_state.auth_view = "login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; font-size: 12px; color: #9ca3af; margin-top: 30px;'>Al crear una cuenta, aceptas nuestras Condiciones de uso y nuestra Política de privacidad.</p>", unsafe_allow_html=True)