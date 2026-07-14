import streamlit as st
import datetime

def render_top_bar():
    col_text, col_search, col_bell = st.columns([3, 1.5, 0.3], vertical_alignment="center")
    
    with col_text:
        hora = datetime.datetime.now().hour
        saludo = "Buenos días" if hora < 12 else "Buenas tardes" if hora < 19 else "Buenas noches"
        
        # --- LÓGICA PARA OBTENER EL NOMBRE DINÁMICO ---
        perfil = st.session_state.get("user_profile")
        
        # Revisamos si hay datos de la API, de lo contrario buscamos si entró con Google
        if perfil and perfil.get("full_name"):
            nombre_completo = perfil["full_name"]
        else:
            nombre_completo = st.session_state.get("user_name", "Estudiante")
            
        # Extraemos solo la primera palabra para un saludo más casual
        primer_nombre = nombre_completo.split()[0] if nombre_completo else "Estudiante"
        
        st.html(f"""
        <div style="margin-bottom: 0px;">
            <h2 style="margin: 0; font-weight: 700; color: #111827; font-size: 26px;">{saludo}, {primer_nombre}</h2>
            <p style="margin: 0; color: #6b7280; font-size: 15px; margin-top: 4px;">Llevas una racha de 12 días — ¡sigue así!</p>
        </div>
        """)