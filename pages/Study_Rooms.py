import streamlit as st
import urllib.parse
from utils.security import require_login
from components.sidebar import render_sidebar
from utils.images import get_image_base64
from utils.api_client import obtener_mis_salas, obtener_salas, crear_sala, unirse_a_sala_api, upload_document, get_documents

# Protegemos la ruta
if not require_login():
    st.stop()

@st.dialog("¡Bienvenido a la sala!")
def modal_exito_unirse(nombre_sala):
    st.success(f"Te has unido exitosamente a: **{nombre_sala}**")
    if st.button("Comenzar a estudiar", type="primary", use_container_width=True):
        st.rerun()

def study_rooms_page():
    # --- 0. BÚSQUEDA DEL ID Y NOMBRE DE USUARIO ---
    usuario_id = None
    for key in ["usuario_id", "user_id", "id_usuario", "id"]:
        if key in st.session_state and st.session_state[key]:
            usuario_id = st.session_state[key]
            break
            
    if not usuario_id:
        for key in ["user", "user_data", "user_info", "perfil", "datos_usuario"]:
            if key in st.session_state and isinstance(st.session_state[key], dict):
                usuario_id = st.session_state[key].get("id") or st.session_state[key].get("usuario_id")
                if usuario_id:
                    break
                    
    if not usuario_id:
        usuario_id = "Usuario"

    usuario_id = str(usuario_id)
    
    # Rescatamos tu nombre real para la tarjeta
    perfil = st.session_state.get("user_profile", {})
    nombre_usuario = perfil.get("full_name") if perfil and perfil.get("full_name") else f"Usuario {usuario_id}"

    # --- INICIALIZACIÓN DE ESTADOS ---
    if "lista_salas" not in st.session_state:
        salas_back = obtener_mis_salas(usuario_id)
        st.session_state.lista_salas = salas_back if salas_back else []
        
    if "vista_actual" not in st.session_state:
        st.session_state.vista_actual = "catalogo"

    avatar_b64 = get_image_base64("assets/icons/avatar.png")
    def create_img_tag(b64_str, size):
        if b64_str:
            radius = "50%" if "avatar" in b64_str else "0%"
            return f'<img src="{b64_str}" style="width: {size}; height: {size}; border-radius: {radius}; object-fit: cover; vertical-align: middle;">'
        return ""

    img_avatar_html = create_img_tag(avatar_b64, "24px")
    img_avatar_large_html = create_img_tag(avatar_b64, "36px")

    st.html("""
    <style>
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 1rem !important;
            background-color: #ffffff !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
            border: 1px solid #e5e7eb !important;
            padding: 1rem !important;
        }
        div[data-testid="stButton"] button {
            border-radius: 1.5rem !important;
            font-weight: 500 !important;
        }
        div[data-baseweb="input"], div[data-baseweb="select"] {
            border-radius: 0.5rem !important;
            background-color: #f9fafb !important;
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

    # ==========================================
    # VISTA 1: CATÁLOGO DE SALAS 
    # ==========================================
    if st.session_state.vista_actual == "catalogo":
        st.html("""
        <h3 style='margin-bottom: 0px; font-weight: 700; color: #3b82f6; text-transform: uppercase; font-size: 12px; letter-spacing: 1px;'>Estudio Colaborativo</h3>
        <h1 style='margin-top: 5px; font-weight: 800; color: #111827; font-size: 28px;'>Salas de estudio</h1>
        <p style='color: #6b7280; font-size: 14px; margin-bottom: 25px;'>Comparte tus documentos y utilízalos con tu grupo en Chat RAG, Flashcards y Quizzes.</p>
        """)

        col_crear, col_unirse = st.columns(2, gap="large")

        with col_crear:
            with st.container(border=True):
                st.markdown("#### Crear una sala")
                st.caption("Serás propietario y podrás invitar estudiantes.")
                with st.form("form_crear_sala", clear_on_submit=True):
                    nombre_sala = st.text_input("Nombre", placeholder="Ej. Biología — Grupo 9A", label_visibility="collapsed")
                    codigo_acceso = st.text_input("Código", placeholder="Crea una clave de acceso", type="password", label_visibility="collapsed")
                    submit_crear = st.form_submit_button("Crear", type="primary", use_container_width=True)
                    
                    if submit_crear:
                        if not nombre_sala or not codigo_acceso:
                            st.error("Completa todos los campos.")
                        else:
                            id_sala = nombre_sala.lower().strip().replace(" ", "_")
                            res = crear_sala(id_sala, nombre_sala, codigo_acceso, creador_id=usuario_id)
                            if res.get("success"):
                                st.session_state.lista_salas = obtener_mis_salas(usuario_id)
                                st.toast(f"¡Sala creada exitosamente!", icon="✅")
                                st.rerun()
                            else:
                                st.error(res.get('error'))

        with col_unirse:
            with st.container(border=True):
                st.markdown("#### Unirse a una sala")
                st.caption("Usa el código que compartió el propietario.")
                with st.form("form_unirse_sala", clear_on_submit=True):
                    codigo_ingresado = st.text_input("Código", placeholder="CÓDIGO", type="password", label_visibility="collapsed")
                    submit_join = st.form_submit_button("Unirse", use_container_width=True)
                    
                    if submit_join:
                        if codigo_ingresado:
                            todas_las_salas = obtener_salas() or []
                            sala_encontrada = next((s for s in todas_las_salas if s.get("codigo_acceso") == codigo_ingresado), None)
                            
                            if sala_encontrada:
                                res = unirse_a_sala_api(usuario_id, sala_encontrada["id"], codigo_ingresado)
                                if res.get("success"):
                                    st.session_state.lista_salas = obtener_mis_salas(usuario_id)
                                    modal_exito_unirse(sala_encontrada["nombre_sala"])
                                else:
                                    st.error(res.get('error'))
                            else:
                                st.error("Código inválido.")
                        else:
                            st.warning("Ingresa el código.")

        st.divider()

        filtros = ["Todas", "En vivo", "Mis Salas", "Programadas"]
        filtro_seleccionado = st.radio("Filtros", options=filtros, horizontal=True, label_visibility="collapsed", index=0)
        st.write("")

        if filtro_seleccionado == "Mis Salas":
            salas_a_mostrar = obtener_mis_salas(usuario_id) or []
        elif filtro_seleccionado == "Todas":
            salas_a_mostrar = obtener_salas() or []
        else:
            salas_a_mostrar = st.session_state.lista_salas

        if not salas_a_mostrar:
            st.info("Aún no tienes salas reales. ¡Crea una nueva arriba!")
        else:
            cols = st.columns(3)
            for i, room in enumerate(salas_a_mostrar):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.html(f"""
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                            <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #ecfdf5; display: flex; justify-content: center; align-items: center;">
                                {img_avatar_html} 
                            </div>
                            <div style="background-color: #f9fafb; color: #4b5563; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; border: 1px solid #e5e7eb;">
                                Programada
                            </div>
                        </div>
                        <div style="font-size: 11px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">SALA DE ESTUDIO</div>
                        <div style="font-size: 16px; font-weight: 700; color: #111827; margin-bottom: 6px;">{room.get('nombre_sala')}</div>
                        <div style="font-size: 12px; color: #6b7280; margin-bottom: 20px;">Código: {room.get('codigo_acceso')}</div>
                        """)
                        if st.button("Entrar", key=f"enter_{room['id']}", type="secondary", use_container_width=True):
                            st.session_state.vista_actual = "detalle_sala"
                            st.session_state.sala_activa_ui = room['id']
                            st.rerun()

    # ==========================================
    # VISTA 2: DETALLE DE LA SALA 
    # ==========================================
    elif st.session_state.vista_actual == "detalle_sala":
        
        st.write("")
        salas_a_mostrar = obtener_mis_salas(usuario_id) or []

        if not salas_a_mostrar:
            st.warning("No perteneces a ninguna sala.")
        else:
            if "sala_activa_ui" not in st.session_state or not any(s["id"] == st.session_state.sala_activa_ui for s in salas_a_mostrar):
                st.session_state.sala_activa_ui = salas_a_mostrar[0]["id"]

            col_lista, col_detalle = st.columns([1, 3], gap="large")

            # PANEL IZQUIERDO: MIS SALAS
            with col_lista:
                st.markdown("##### Mis salas")
                for room in salas_a_mostrar:
                    is_active = (st.session_state.sala_activa_ui == room["id"])
                    btn_type = "primary" if is_active else "secondary"
                    
                    if st.button(f"📚 {room['nombre_sala']}", key=f"sel_{room['id']}", type=btn_type, use_container_width=True):
                        st.session_state.sala_activa_ui = room["id"]
                        st.rerun()
                
                st.write("")
                if st.button("← Volver", type="secondary", use_container_width=True):
                    st.session_state.vista_actual = "catalogo"
                    st.rerun()

            # PANEL DERECHO: DETALLES DE LA SALA
            with col_detalle:
                sala_actual = next((s for s in salas_a_mostrar if s["id"] == st.session_state.sala_activa_ui), None)
                
                if sala_actual:
                    with st.container(border=True):
                        st.markdown(f"### {sala_actual['nombre_sala']}")
                        st.caption(f"Código de acceso: **{sala_actual.get('codigo_acceso', 'Oculto')}**")
                        st.divider()
                        
                        col_recursos, col_miembros = st.columns([1.5, 1], gap="large")
                        
                        # --- SECCIÓN: RECURSOS ---
                        with col_recursos:
                            st.markdown("##### Recursos compartidos")
                            st.write("Sube PDFs directamente a esta sala para estudiarlos con el equipo.")
                            
                            archivo = st.file_uploader("Arrastra tu PDF aquí", type=["pdf"], label_visibility="collapsed")
                            if st.button("Compartir documento", type="primary"):
                                if archivo:
                                    with st.spinner("Subiendo e indexando..."):
                                        res = upload_document(archivo.name, archivo.getvalue(), str(sala_actual['id']))
                                        if res.get("success"):
                                            st.success("¡Documento compartido exitosamente!")
                                            st.rerun()
                                        else:
                                            st.error(res.get('error'))
                                else:
                                    st.warning("Selecciona un archivo antes de compartir.")
                            
                            st.write("---")
                            st.markdown("**Documentos disponibles:**")
                            
                            documentos = get_documents(str(sala_actual['id']))
                            if not documentos:
                                st.info("Aún no hay documentos compartidos en esta sala.")
                            else:
                                for doc in documentos:
                                    nombre = doc.get('nombre_archivo', 'Documento')
                                    doc_id = doc.get('id', '')
                                    nombre_seguro = urllib.parse.quote(nombre)
                                    url_pdf = f"http://localhost:8000/static/{doc_id}_{nombre_seguro}"
                                    
                                    st.markdown(f"""
                                    <div style='display: flex; justify-content: space-between; align-items: center; padding: 8px; border: 1px solid #e5e7eb; border-radius: 8px; margin-bottom: 8px; background-color: #f9fafb;'>
                                        <span style='font-size: 14px; font-weight: 500; color: #111827;'>📄 {nombre}</span>
                                        <a href="{url_pdf}" target="_blank" style="text-decoration: none;">
                                            <button style="background-color: #ffffff; border: 1px solid #d1d5db; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; color: #374151; cursor: pointer;">Ver</button>
                                        </a>
                                    </div>
                                    """, unsafe_allow_html=True)

                        # --- SECCIÓN: MIEMBROS ---
                        with col_miembros:
                            st.markdown("##### Miembros")
                            
                            with st.container(border=True):
                                st.html(f"""
                                <div style="display: flex; align-items: center; margin-bottom: 4px;">
                                    {img_avatar_large_html}
                                    <div style="margin-left: 12px;">
                                        <div style="font-size: 14px; font-weight: 600; color: #111827;">{nombre_usuario} (Tú)</div>
                                        <div style="font-size: 12px; color: #6b7280;">Miembro de la sala</div>
                                    </div>
                                </div>
                                """)
                                st.write("")
                                st.caption("Todos los miembros de la sala comparten estos recursos.")

if __name__ == "__main__":
    study_rooms_page()