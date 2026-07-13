import streamlit as st

# Importamos todas las piezas del rompecabezas
from components.sidebar import render_sidebar
from components.dashboard.top_bar import render_top_bar
from components.dashboard.study_metrics import render_study_metrics
from components.documentos.upload_zone import render_upload_zone
from components.chat.chat_panel import render_chat_conversation

def dashboard_page():
    st.html("""
    <style>

        /* 2. ESTILO DEL DRAG & DROP (Zona de subida) */
        div[data-testid="stFileUploader"] {
            border: 2px dashed #e5e7eb !important;
            border-radius: 1.5rem !important;
            padding: 2rem !important;
            text-align: center;
        }
    </style>
    """)

    # 1. Menú lateral
    render_sidebar()

    # 2. Barra superior
    render_top_bar()
    st.divider()

    # 3. Layout principal: 2/3 para métricas y subida, 1/3 para el chat rápido
    col_main, col_chat = st.columns([2, 1], gap="large")

    with col_main:
        # Aquí van las tarjetas de estadísticas
        render_study_metrics()
        
        st.write("") # Espacio para respirar
        
        # Aquí va la zona punteada para arrastrar archivos
        render_upload_zone()

    with col_chat:
        # Reutilizamos tu panel de chat, metido en una tarjeta alta
        with st.container(border=True, height=600):
            render_chat_conversation()

if __name__ == "__main__":
    dashboard_page()