import streamlit as st
import datetime

def render_top_bar():
    col_text, col_search, col_bell = st.columns([3, 1.5, 0.2], vertical_alignment="center")
    
    with col_text:
        hora = datetime.datetime.now().hour
        saludo = "Buenos días" if hora < 12 else "Buenas tardes" if hora < 19 else "Buenas noches"
        
        st.html(f"""
        <div style="margin-bottom: 0px;">
            <h2 style="margin: 0; font-weight: 700; color: #111827; font-size: 26px;">{saludo}, Ariel</h2>
            <p style="margin: 0; color: #6b7280; font-size: 15px; margin-top: 4px;">Llevas una racha de 12 días — ¡sigue así!</p>
        </div>
        """)
        
    with col_search:
        st.text_input("Buscar", placeholder="🔍 Buscar documentos...", label_visibility="collapsed")
        
    with col_bell:
        st.button("🔔", key="bell_btn", use_container_width=True)