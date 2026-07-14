import streamlit as st
import re
import html
from utils.images import get_image_base64
from utils.api_client import registrar_usuario, generar_username

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
    # 1. Inyección de CSS Mágico
    st.markdown("""
    <style>
        /* Fondo con destellos verdes difuminados (Mesh Gradient) */
        .stApp {
            background: radial-gradient(circle at 15% 30%, rgba(46, 184, 114, 0.15) 0%, transparent 40%),
                        radial-gradient(circle at 85% 80%, rgba(46, 184, 114, 0.1) 0%, transparent 40%);
        }
        
        /* Forzar bordes muy redondeados y sombra en la tarjeta */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 1.5rem !important;
            background-color: #ffffff !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04) !important;
            border: 1px solid rgba(0,0,0,0.05) !important;
            padding: 1.5rem !important;
        }

        /* Redondear un poco más las cajas de texto y el botón */
        div[data-baseweb="input"] {
            border-radius: 0.8rem !important;
        }
        div[data-testid="stButton"] button {
            border-radius: 2rem !important;
            font-weight: 600 !important;
            padding: 0.5rem !important;
        }
        
        /* Ocultar el fondo gris de los botones secundarios para que parezcan links */
        .btn-link button {
            background: transparent !important;
            border: none !important;
            color: #2eb872 !important;
            box-shadow: none !important;
            font-size: 14px !important;
        }
        .btn-link button:hover {
            text-decoration: underline !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. Cargar ícono en Base64 con el nombre de tu archivo PNG
    icono_logo = get_image_base64("assets/icons/graduacion.png")

    # 3. Layout centrado
    st.write("") 
    st.write("") # Empujamos un poco hacia abajo
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    
    with col_center:
        with st.container(border=True):
            
            # --- Logo Dinámico (Imagen PNG) ---
            if icono_logo:
                st.markdown(f"""
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(46,184,114,0.3);'>
                            <img src="{icono_logo}" style="width: 32px; height: 32px; object-fit: contain;">
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Si no encuentra la imagen en la ruta, muestra el emoji por defecto
                st.markdown("""
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;'>
                            🎓
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            # --- Textos ---
            st.markdown("<h2 style='text-align: center; font-weight: 700; font-size: 24px; margin-bottom: 5px;'>Crea tu cuenta de LuminIA</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 25px;'>Únete a miles de estudiantes que aprenden de forma más eficaz gracias a la IA.</p>", unsafe_allow_html=True)
            
            # --- Formulario ---
            with st.form("register_form", border=False):
                st.markdown("Nombre")
                name = st.text_input("Full Name", placeholder="Josue Abraham", label_visibility="collapsed")

                st.markdown("<div style='margin-top: 10px;'>Correo</div>", unsafe_allow_html=True)
                email = st.text_input("Email", placeholder="correo@ejemplo.edu", label_visibility="collapsed")
                
                st.markdown("<div style='margin-top: 10px;'>Contraseña</div>", unsafe_allow_html=True)
                password = st.text_input("Password", placeholder="Crea una contraseña", type="password", label_visibility="collapsed")
                
                st.markdown("<div style='margin-top: 10px;'>Confirmar Contraseña</div>", unsafe_allow_html=True)
                confirm = st.text_input("Confirm Password", placeholder="Vuelve a escribir tu contraseña", type="password", label_visibility="collapsed")
                
                st.write("")
                
                # Botón Verde (tomará el color del config.toml)
                submitted = st.form_submit_button("Crear cuenta", use_container_width=True, type="primary")
                
                if submitted:
                    # Aplicamos limpieza a los textos
                    safe_name = sanitize_input(name)
                    safe_email = sanitize_input(email)
                    
                    # Ejecutamos la validación estricta de la contraseña
                    is_valid, error_msg = validar_contrasena(password)
                    
                    if not safe_name or not safe_email or not password:
                        st.error("Favor de llenar todos los campos.")
                    elif not is_valid:
                        # Si falla, mostramos el error exacto construido en la función
                        st.error(error_msg)
                    elif password != confirm:
                        st.error("Las contraseñas no coinciden.")
                    else:
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
                        else:
                            st.error(resultado["error"])
            # --- Divider con el "or" ---
            st.markdown("""
                <div style='display: flex; align-items: center; text-align: center; margin: 5px 0;'>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                    <span style='padding: 0 10px; color: #9ca3af; font-size: 12px;'>o</span>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                </div>
            """, unsafe_allow_html=True)
            
            # --- Log in (Botón invisible simulando un enlace HTML) ---
            st.markdown("""
                <div style='text-align: center; font-size: 14px; margin-top: 15px;'>
                    <span style='color: #6b7280;'>¿Ya tienes una cuenta? </span>
                </div>
            """, unsafe_allow_html=True)
            
            # Aplicamos la clase btn-link temporalmente
            st.markdown('<div class="btn-link">', unsafe_allow_html=True)
            if st.button("Iniciar Sesion", use_container_width=True):
                st.session_state.auth_view = "login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("<p style='text-align: center; font-size: 12px; color: #9ca3af; margin-top: 30px;'>Al crear una cuenta, aceptas nuestras Condiciones de uso y nuestra Política de privacidad.</p>", unsafe_allow_html=True)