import streamlit as st
from components.sidebar import render_sidebar
from components.salas.room_card import render_room_card

ROOMS = [
    {
        "id": "arch", "title": "Arquitectura de Software", "topic": "Ciencias de la Computación", 
        "icon": "📦", "live": True, "activeCount": 8, "nextSession": "Repasando patrones de diseño",
        "members": [{"name": "Bruno"}, {"name": "Arturo"}, {"name": "Luis"}]
    },
    {
        "id": "calc", "title": "Cálculo II", "topic": "Matemáticas", 
        "icon": "∑", "live": True, "activeCount": 5, "nextSession": "Práctica de integración por partes",
        "members": [{"name": "Hector"}, {"name": "Arturo"}]
    },
    {
        "id": "orgchem", "title": "Química Orgánica", "topic": "Química", 
        "icon": "🧪", "live": False, "activeCount": 4, "nextSession": "Empieza hoy a las 4:00 PM",
        "members": [{"name": "Luis"}, {"name": "Hector"}, {"name": "Bruno"}]
    },
    {
        "id": "ml", "title": "Fundamentos de Machine Learning", "topic": "Inteligencia Artificial", 
        "icon": "🧠", "live": True, "activeCount": 12, "nextSession": "Inmersión en descenso de gradiente",
        "members": [{"name": "Arturo"}, {"name": "Hector"}, {"name": "Luis"}, {"name": "Bruno"}]
    },
    {
        "id": "law", "title": "Derecho Constitucional", "topic": "Derecho", 
        "icon": "⚖️", "live": False, "activeCount": 6, "nextSession": "Empieza mañana a las 10:00 AM",
        "members": [{"name": "Bruno"}, {"name": "Luis"}]
    },
    {
        "id": "econ", "title": "Macroeconomía", "topic": "Economía", 
        "icon": "📈", "live": False, "activeCount": 3, "nextSession": "Empieza el viernes a las 2:00 PM",
        "members": [{"name": "Hector"}, {"name": "Arturo"}]
    },
]

FILTERS = ["Todas", "En vivo", "Mis Salas", "Programadas"]

def study_rooms_page():
    st.html("""
    <style>
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 2rem !important;
            background-color: #ffffff !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03) !important;
            border: 1px solid rgba(0,0,0,0.04) !important;
            padding: 0.5rem 0.8rem !important;
        }
        div[data-testid="stButton"] button {
            border-radius: 3rem !important;
            font-weight: 600 !important;
        }
        div[data-baseweb="input"] {
            border-radius: 2rem !important;
            background-color: #ffffff !important;
        }
        div.row-widget.stRadio > div {
            display: flex;
            gap: 15px;
        }
        div.row-widget.stRadio > div > label {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 2rem !important;
            padding: 8px 24px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        }
    </style>
    """)

    render_sidebar()

    col_title, col_actions = st.columns([1.2, 1], vertical_alignment="bottom")
    
    with col_title:
        st.html("""
        <h2 style='margin-bottom: 0px; font-weight: 700; color: #111827;'>Salas de Estudio</h2>
        <p style='color: #6b7280; font-size: 15px; margin-top: 5px;'>Únete a una sesión en vivo o crea tu propio espacio colaborativo.</p>
        """)
        
    with col_actions:
        search_col, add_col = st.columns([1.5, 1])
        with search_col:
            st.text_input("Buscar", placeholder="Buscar salas...", label_visibility="collapsed")
        with add_col:
            st.button("Nueva Sala", icon=":material/add:", type="primary", use_container_width=True)

    st.divider()

    st.radio("Filtros", options=FILTERS, horizontal=True, label_visibility="collapsed")
    st.write("")
    st.write("")

    cols = st.columns(3)
    for i, room in enumerate(ROOMS):
        with cols[i % 3]:
            render_room_card(room)

if __name__ == "__main__":
    study_rooms_page()