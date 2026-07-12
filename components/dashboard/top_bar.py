import streamlit as st
import datetime

def render_top_bar():
    # Obtenemos la hora actual para el saludo dinámico
    hora = datetime.datetime.now().hour
    saludo = "\n Buenos días" if hora < 12 else "Buenas tardes" if hora < 19 else "Buenas noches"
    
    # Pintamos el saludo y la racha directamente, sin columnas extra
    st.html(f"""
    <div style="margin-bottom: 0px;">
        <h2 style="margin: 0; font-weight: 700; color: #111827; font-size: 26px;">{saludo}, Ariel</h2>
        <p style="margin: 0; color: #6b7280; font-size: 15px; margin-top: 4px;">Llevas una racha de 12 días — ¡sigue así!</p>
    </div>
    """)