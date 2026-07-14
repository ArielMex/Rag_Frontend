import streamlit as st
from utils.security import sanitize_input
from utils.images import get_image_base64
from utils.api_client import login

def render_login_form():
    st.markdown("""
    <style>
        .stApp {
            background: radial-gradient(circle at 15% 30%, rgba(46, 184, 114, 0.15) 0%, transparent 40%),
                        radial-gradient(circle at 85% 80%, rgba(46, 184, 114, 0.1) 0%, transparent 40%);
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 1.5rem !important;
            background-color: #ffffff !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04) !important;
            border: 1px solid rgba(0,0,0,0.05) !important;
            padding: 1.5rem !important;
        }

        div[data-baseweb="input"] {
            border-radius: 0.8rem !important;
        }
        div[data-testid="stButton"] button {
            border-radius: 2rem !important;
            font-weight: 600 !important;
            padding: 0.5rem !important;
        }
        
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

    #Cargar ícono en Base64 (Asegúrate de tener un archivo png en esa ruta)
    icono_logo = get_image_base64("assets/icons/graduacion.png")

    #Layout centrado
    st.write("") 
    st.write("") 
    col_left, col_center, col_right = st.columns([1, 1.2, 1])
    
    with col_center:
        with st.container(border=True):
            
            #Logo
            if icono_logo:
                st.markdown(f"""
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(46,184,114,0.3);'>
                            <img src="{icono_logo}" style="width: 32px; height: 32px; object-fit: contain;">
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Fallback por si la imagen no se encuentra (mostraria el birrete emoji)
                st.markdown("""
                    <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                        <div style='background-color: #2eb872; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px;'>
                            🎓
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<h2 style='text-align: center; font-weight: 700; font-size: 24px; margin-bottom: 5px;'>Bienvenido de nuevo a Lumina</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #6b7280; font-size: 14px; margin-bottom: 25px;'>Inicia sesión para continuar aprendiendo con tu<br>compañero de estudio de IA.</p>", unsafe_allow_html=True)
            
            with st.form("login_form", border=False):
                st.markdown("Correo electrónico")
                email = st.text_input("Correo electrónico", placeholder="ejemplo@universidad.edu", label_visibility="collapsed")
                
                st.markdown("<div style='margin-top: 10px;'>Contraseña</div>", unsafe_allow_html=True)
                password = st.text_input("Contraseña", placeholder="Ingresa tu contraseña", type="password", label_visibility="collapsed")
                
                st.write("")
                
                submitted = st.form_submit_button("Iniciar Sesión →", use_container_width=True, type="primary")
                
                if submitted:
                    safe_email = sanitize_input(email)
                    
                    if safe_email and password:
                        resultado = login(safe_email, password)

                        if resultado["success"]:
                            datos = resultado["data"]
                            st.session_state.access_token = datos["access_token"]
                            st.session_state.refresh_token = datos["refresh_token"]
                            st.session_state.logged_in = True
                            st.rerun()
                        else:
                            st.error(resultado["error"])
                    else:
                        st.error("Por favor, ingresa tu correo y contraseña.")
            
            st.markdown("""
                <div style='display: flex; align-items: center; text-align: center; margin: 5px 0;'>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                    <span style='padding: 0 10px; color: #9ca3af; font-size: 12px;'>o</span>
                    <hr style='flex: 1; border: none; border-top: 1px solid #e5e7eb;'>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style='text-align: center; font-size: 14px; margin-top: 15px;'>
                    <span style='color: #6b7280;'>¿No tienes una cuenta? </span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="btn-link">', unsafe_allow_html=True)
            if st.button("Crear una cuenta", use_container_width=True):
                st.session_state.auth_view = "register"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<p style='text-align: center; font-size: 12px; color: #9ca3af; margin-top: 30px;'>Al iniciar sesión, aceptas nuestros Términos y Política de Privacidad.</p>", unsafe_allow_html=True)