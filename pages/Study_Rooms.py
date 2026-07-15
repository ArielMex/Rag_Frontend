import streamlit as st
from utils.security import require_login
from components.sidebar import render_sidebar
from components.salas.room_card import render_room_card
from utils.api_client import obtener_salas, crear_sala

if not require_login():
    st.stop()

# Respaldo local con la estructura del Backend por si la API está vacía o apagada
ROOMS_MOCK = [
    {
        "id": "arch", 
        "nombre_sala": "Arquitectura de Software", 
        "codigo_acceso": "ARC-2026"
    },
    {
        "id": "calc", 
        "nombre_sala": "Cálculo II", 
        "codigo_acceso": "CALC-INTEGRAL"
    },
    {
        "id": "orgchem", 
        "nombre_sala": "Química Orgánica", 
        "codigo_acceso": "QUIM-ORG-42"
    }
]

FILTERS = ["Todas", "En vivo", "Mis Salas", "Programadas"]

def study_rooms_page():
    # --- 1. INICIALIZACIÓN DE ESTADOS DE ENRUTAMIENTO Y DATOS ---
    if "vista_actual" not in st.session_state:
        st.session_state.vista_actual = "catalogo"
        
    if "lista_salas" not in st.session_state:
        salas_back = obtener_salas()
        # Si la API responde con datos, los usamos; si no, dejamos el mock de respaldo
        st.session_state.lista_salas = salas_back if salas_back else ROOMS_MOCK

    # --- Estilos CSS Inyectados ---
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
            border-radius: 2rem !important;
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

    # --- 2. ENRUTADOR DE VISTAS ---
    
    # === VISTA A: CATÁLOGO PRINCIPAL ===
    if st.session_state.vista_actual == "catalogo":
        col_title, col_actions = st.columns([1.2, 1], vertical_alignment="bottom")
        
        with col_title:
            st.html("""
            <h2 style='margin-bottom: 0px; font-weight: 700; color: #111827;'>Salas de Estudio</h2>
            <p style='color: #6b7280; font-size: 15px; margin-top: 5px;'>Únete a una sesión en vivo o crea tu propio espacio colaborativo.</p>
            """)
            
        with col_actions:
            search_col, add_col = st.columns([1.5, 1])
            with search_col:
                st.text_input("Buscar", placeholder="🔍 Buscar salas...", label_visibility="collapsed")
            with add_col:
                if st.button("＋ Crear Nueva Sala", type="primary", use_container_width=True):
                    st.session_state.vista_actual = "crear"
                    st.rerun()

        st.divider()

        st.radio("Filtros", options=FILTERS, horizontal=True, label_visibility="collapsed")
        st.write("")
        st.write("")

        # Grid dinámico de tarjetas
        cols = st.columns(3)
        for i, room in enumerate(st.session_state.lista_salas):
            # MAPEO: Convertimos las llaves del backend (español) a las que espera la tarjeta (inglés)
            room_mapeada = {
                "id": room.get("id"),
                "title": room.get("nombre_sala"),
                "topic": "Sala de Estudio",
                "icon": "📚",
                "live": False,
                "activeCount": 0,
                "nextSession": f"Código de acceso: {room.get('codigo_acceso')}",
                "members": []
            }
            
            with cols[i % 3]:
                render_room_card(room_mapeada)

    # === VISTA B: FORMULARIO DE CREACIÓN (POST) ===
    elif st.session_state.vista_actual == "crear":
        st.html("""
        <h2 style='margin-bottom: 0px; font-weight: 700; color: #111827;'>Crear Nueva Sala de Estudio</h2>
        <p style='color: #6b7280; font-size: 15px; margin-top: 5px;'>Configura las credenciales obligatorias para dar de alta el espacio en el servidor.</p>
        """)
        st.divider()

        with st.container(border=True):
            st.write("")
            nombre_sala = st.text_input("Nombre de la Sala *", placeholder="Ej. Estructuras de Datos, Preparación Examen...")
            codigo_acceso = st.text_input("Código de Acceso *", placeholder="Ej. ARC-2026, CODIGO-SECRETO...")
            st.write("")

            col_btn_cancelar, col_btn_guardar = st.columns([1, 1])
            
            with col_btn_cancelar:
                if st.button("Cancelar", use_container_width=True):
                    st.session_state.vista_actual = "catalogo"
                    st.rerun()
                    
            with col_btn_guardar:
                if st.button("Guardar Espacio", type="primary", use_container_width=True):
                    if not nombre_sala or not codigo_acceso:
                        st.error("Por favor completa los campos obligatorios (*)")
                    else:
                        # Generamos un ID amigable basado en texto para mandar al backend
                        id_sala = nombre_sala.lower().strip().replace(" ", "_")
                        
                        # Payload idéntico al esquema 'SalaEstudioCreate' del Backend
                        nueva_sala_payload = {
                            "id": id_sala,
                            "nombre_sala": nombre_sala,
                            "codigo_acceso": codigo_acceso
                        }

                        # Llamada HTTP mediante tu api_client
                        res = crear_sala(nueva_sala_payload)
                        
                        if res.get("success"):
                            # Trae la lista fresca de la API para sincronizar el catálogo
                            st.session_state.lista_salas = obtener_salas()
                            st.session_state.vista_actual = "catalogo"
                            st.toast(f"¡Sala '{nombre_sala}' creada exitosamente!", icon="✅")
                            st.rerun()
                        else:
                            st.error(f"Error al guardar la sala: {res.get('error')}")

if __name__ == "__main__":
    study_rooms_page()