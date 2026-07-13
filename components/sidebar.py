import streamlit as st
from utils.images import get_image_base64

def render_sidebar():
    logo_b64 = get_image_base64("assets/icons/graduacion.png")
    avatar_b64 = get_image_base64("assets/icons/avatar.png")

    def create_img_tag(b64_str, size, fallback=""):
        if b64_str:
            radius = "50%" if "avatar" in b64_str else "0%"
            return f'<img src="{b64_str}" style="width: {size}; height: {size}; border-radius: {radius}; object-fit: cover;">'
        return fallback

    img_logo = create_img_tag(logo_b64, "22px", "🎓")
    img_avatar = create_img_tag(avatar_b64, "38px", "👤")

    st.html("""
    <style>
        /* 1. IMPORTAR LA FUENTE DE MATERIAL ICONS */
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0');

        /* MATAR EL HEADER EN TODAS LAS PÁGINAS */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Ajustar el espacio superior del contenido principal sin romper el sidebar */
        .block-container {
            padding-top: 1rem !important;
        }

        /* --- NUEVO: SIDEBAR FIJO SIN SCROLL --- */
        [data-testid="stSidebar"] {
            background-color: #fafafa !important;
            border-right: 1px solid #f3f4f6 !important;
            overflow: hidden !important; /* Corta cualquier intento de scroll */
        }
        
        [data-testid="stSidebar"] > div {
            overflow: hidden !important;
        }

        [data-testid="stSidebarHeader"] {
            display: none !important;
        }
        
        /* Convertir el interior del sidebar en una columna completa de arriba a abajo */
        [data-testid="stSidebarUserContent"] {
            padding: 1.5rem 1rem 1.5rem 1rem !important;
            height: 100vh !important; /* Altura 100% de la ventana */
        }
        
        [data-testid="stSidebarUserContent"] > div[data-testid="stVerticalBlock"] {
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
        }

        /* MAGIA: El penúltimo contenedor (tu tarjeta de perfil) empuja todo al fondo */
        [data-testid="stSidebarUserContent"] > div[data-testid="stVerticalBlock"] > div:nth-last-child(2) {
            margin-top: auto !important;
            margin-bottom: 15px !important; /* Separación con el botón de cerrar sesión */
        }

        /* Estilo de los Enlaces (st.page_link) */
        div[data-testid="stPageLink-NavLink"] {
            padding: 0 !important;
            margin-bottom: 0px !important;
        }
        
        div[data-testid="stPageLink-NavLink"] > a {
            padding: 10px 16px !important;
            border-radius: 20px !important; 
            color: #6b7280 !important;
            font-weight: 500 !important;
            text-decoration: none !important;
            transition: all 0.2s ease;
        }
        
        div[data-testid="stPageLink-NavLink"] > a:hover {
            background-color: #f3f4f6 !important;
            color: #111827 !important;
        }

        div[data-testid="stPageLink-NavLink"] > a[aria-current="page"] {
            background-color: #dcfce7 !important;
            color: #166534 !important;
            font-weight: 600 !important;
        }

        /* ESTILO PARA EL BOTÓN DE CERRAR SESIÓN */
        [data-testid="stSidebar"] button {
            background-color: #fef2f2 !important; 
            color: #dc2626 !important; 
            border: none !important;
            border-radius: 20px !important;
            display: flex !important;
            justify-content: flex-start !important; 
            padding: 0.2rem 1rem !important; 
            font-weight: 600 !important;
            box-shadow: none !important;
            transition: all 0.2s ease;
        }
        
        [data-testid="stSidebar"] button:hover {
            background-color: #fee2e2 !important; 
            color: #b91c1c !important;
        }
        
        [data-testid="stSidebar"] button p {
            font-size: 15px !important;
            color: inherit !important;
        }
    </style>
    """)

    with st.sidebar:
        st.html(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px; padding-left: 10px;">
            <div style="background-color: #2eb872; color: white; width: 38px; height: 38px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 20px; box-shadow: 0 4px 10px rgba(46,184,114,0.3);">
                {img_logo}
            </div>
            <div>
                <div style="font-size: 16px; font-weight: 700; color: #111827; line-height: 1.2;">Lumina</div>
                <div style="font-size: 12px; color: #6b7280;">Learning Studio</div>
            </div>
        </div>
        """)

        st.page_link("pages/Dashboard.py", label="DASHBOARD", icon=":material/dashboard:")
        st.page_link("pages/Study_Rooms.py", label="SALA DE ESTUDIOS", icon=":material/group:")
        st.page_link("pages/My_Documents.py", label="MIS DOCUMENTOS", icon=":material/description:")
        st.page_link("pages/Chat.py", label="CHAT IA", icon=":material/forum:")

            
        st.html(f"""
        <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background-color: #f3f4f6; border-radius: 20px; margin-top: 19rem">
            {img_avatar}
            <div>
                <div style="font-size: 14px; font-weight: 700; color: #111827; line-height: 1.2;">Ariel Roberto</div>
                <div style="font-size: 12px; color: #6b7280;">Estudiante</div>
            </div>
        </div>
        """)
        
        if st.button("Cerrar sesión", icon=":material/logout:", use_container_width=True):
            st.session_state.clear()
            st.rerun()