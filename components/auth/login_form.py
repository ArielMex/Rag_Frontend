import streamlit as st
from utils.security import sanitize_input
from utils.images import get_image_base64

try:
    from streamlit_oauth import OAuth2Component
except ImportError:
    OAuth2Component = None

try:
    import jwt
except ImportError:
    jwt = None

# Recuerda cambiar esto por st.secrets en producción
CLIENT_ID = "309045838328-v6e5q6aoaigfqlm6v8bt293ldkp75m3o.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8502"

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

def render_login_form():
    st.markdown(
        """
        <style>
            .stApp {
                background: radial-gradient(circle at 15% 30%, rgba(46, 184, 114, 0.15) 0%, transparent 40%),
                            radial-gradient(circle at 85% 80%, rgba(46, 184, 114, 0.1) 0%, transparent 40%);
            }

            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: 2.5rem !important;
                background-color: #ffffff !important;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04) !important;
                border: 1px solid rgba(0, 0, 0, 0.05) !important;
                padding: 1.5rem !important;
            }

            div[data-baseweb="input"] {
                border-radius: 0.8rem !important;
            }

            div[data-testid="stButton"] button,
            div[data-testid="stFormSubmitButton"] button,
            .stMarkdown a button {
                border-radius: 2rem !important;
                padding: 0.65rem 1rem !important;
            }

            div[data-testid="stFormSubmitButton"] button[kind="primary"],
            div[data-testid="stButton"] button[kind="primary"] {
                font-weight: 600 !important;
                font-size: 16px !important;
                background: linear-gradient(135deg, #10b981, #059669) !important;
                border: none !important;
                color: white !important;
            }

            div[data-testid="stButton"] button[kind="secondary"],
            .stMarkdown a button {
                font-weight: 400 !important;
                font-size: 14px !important;
                color: #4b5563 !important;
                background: transparent !important;
                border: 1px solid #e5e7eb !important;
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
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")

    col_left, col_center, col_right = st.columns([1, 1.2, 1])

    with col_center:
        with st.container(border=True):
            logo_b64 = get_image_base64("assets/icons/graduacion.png")

            if logo_b64:
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(46,184,114,0.3);'>
                            <img src="{logo_b64}" style="width: 32px; height: 32px; object-fit: contain;">
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;'>
                            🎓
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                "<h2 style='text-align: center; font-weight: 700; font-size: 24px; margin-bottom: 5px;'>Inicia sesión en LuminIA</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 25px;'>Accede a tu espacio de estudio con tu compañero de IA.</p>",
                unsafe_allow_html=True,
            )

            with st.form("login_form", border=False):
                st.markdown("Correo")
                email = st.text_input("Email", placeholder="ejemplo@correo.edu.mx", label_visibility="collapsed")

                st.markdown("<div style='margin-top: 10px;'>Contraseña</div>", unsafe_allow_html=True)
                password = st.text_input(
                    "Password",
                    placeholder="Ingresa tu contraseña",
                    type="password",
                    label_visibility="collapsed",
                )

                st.write("")

                submitted = st.form_submit_button("Iniciar sesión", use_container_width=True, type="primary")

                if submitted:
                    safe_email = sanitize_input(email)
                    if safe_email and password:
                        st.session_state.logged_in = True
                        st.session_state.user_email = safe_email
                        st.rerun()
                    else:
                        st.error("Por favor, ingresa tu correo y contraseña.")

            st.markdown(
                """
                <div style='display: flex; align-items: center; text-align: center; margin: 5px 0 15px 0;'>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                    <span style='padding: 0 10px; color: #9ca3af; font-size: 12px;'>o</span>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if oauth2 is not None and jwt is not None:
                try:
                    result = oauth2.authorize_button(
                        name="Continuar con Google",
                        icon="https://www.google.com.br/favicon.ico",
                        redirect_uri=REDIRECT_URI,
                        scope="openid email profile",
                        key="google_login",
                        extras_params={"prompt": "consent", "access_type": "offline"},
                        use_container_width=True,
                    )
                except Exception:
                    result = None

                if result and "token" in result:
                    id_token = result["token"]["id_token"]
                    user_info = jwt.decode(id_token, options={"verify_signature": False})
                    st.session_state.logged_in = True
                    st.session_state.user_email = user_info.get("email")
                    st.session_state.user_name = user_info.get("name")
                    st.rerun()
            else:
                st.link_button(
                    "Continuar con Google",
                    "https://accounts.google.com/o/oauth2/v2/auth?client_id=309045838328-v6e5q6aoaigfqlm6v8bt293ldkp75m3o.apps.googleusercontent.com&redirect_uri=http://localhost:8502&response_type=code&scope=openid%20email%20profile&access_type=offline&prompt=consent",
                    use_container_width=True,
                )

            st.markdown(
                "<div style='text-align: center; font-size: 14px; margin-top: 15px;'><span style='color: #6b7280;'>¿No tienes una cuenta? </span></div>",
                unsafe_allow_html=True,
            )

            st.markdown('<div class="btn-link">', unsafe_allow_html=True)
            if st.button("Crear una cuenta", use_container_width=True, type="secondary"):
                st.session_state.auth_view = "register"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)