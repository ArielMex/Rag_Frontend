import streamlit as st

def render_sidebar():
    # --- CSS Mágico Global ---
    st.html("""
    <style>
        /* 1. MATAR EL HEADER EN TODAS LAS PÁGINAS */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Ajustar el espacio superior del contenido principal sin romper el sidebar */
        .block-container {
            padding-top: 1rem !important;
        }

        /* 2. Fondo del sidebar y quitar borde feo de Streamlit */
        [data-testid="stSidebar"] {
            background-color: #fafafa !important;
            border-right: 1px solid #f3f4f6 !important;
        }
        
        /* Ocultar el espacio en blanco superior por defecto del sidebar */
        [data-testid="stSidebarHeader"] {
            display: none !important;
        }
        [data-testid="stSidebarUserContent"] {
            padding-top: 1.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 3. Estilo de los Enlaces (st.page_link) */
        div[data-testid="stPageLink-NavLink"] {
            padding: 0 !important;
            margin-bottom: 5px !important;
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
    </style>
    """)

    with st.sidebar:
        # --- BRAND (Lumina) ---
        st.html("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px; padding-left: 10px;">
            <div style="background-color: #2eb872; color: white; width: 38px; height: 38px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 20px;">
                🎓
            </div>
            <div>
                <div style="font-size: 16px; font-weight: 700; color: #111827; line-height: 1.2;">Lumina</div>
                <div style="font-size: 12px; color: #6b7280;">Learning Studio</div>
            </div>
        </div>
        """)

        # --- NAVEGACIÓN ---
        st.page_link("pages/Dashboard.py", label="DASHBOARD", icon="🎛️")
        st.page_link("pages/Study_Rooms.py", label="SALA DE ESTUDIOS", icon="👥")
        st.page_link("pages/My_Documents.py", label="MIS DOCUMENTOS", icon="📄")
        st.page_link("pages/Chat.py", label="CHAT IA", icon="💬")

        # --- EMPUJAR FOOTER AL FONDO ---
        for _ in range(12):
            st.write("")
        
        # --- SETTINGS ---
        st.html("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 10px 16px; color: #6b7280; font-weight: 500; font-size: 15px; cursor: pointer; transition: 0.2s;" onmouseover="this.style.color='#111827'" onmouseout="this.style.color='#6b7280'">
            <span style="font-size: 18px;">⚙️</span> Settings
        </div>
        """)

        # --- TARJETA DE PERFIL ---
        st.html("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 12px; background-color: #f3f4f6; border-radius: 20px; margin-top: 10px;">
            <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Ariel" style="width: 38px; height: 38px; border-radius: 50%; background-color: white; object-fit: cover;">
            <div>
                <div style="font-size: 14px; font-weight: 700; color: #111827; line-height: 1.2;">Ariel Roberto</div>
                <div style="font-size: 12px; color: #6b7280;">Pro Plan</div>
            </div>
        </div>
        """)