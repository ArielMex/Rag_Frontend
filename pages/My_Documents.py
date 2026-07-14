import streamlit as st
import urllib.parse
from components.sidebar import render_sidebar
from utils.api_client import get_documents, upload_document, delete_document

@st.dialog("Subir nuevo documento")
def modal_subir_documento(sala_id):
    st.write("Selecciona un archivo PDF para indexarlo en la base de conocimientos.")
    archivo = st.file_uploader("Arrastra tu PDF aquí", type=["pdf"], label_visibility="collapsed")
    
    if st.button("Subir e Indexar", type="primary", use_container_width=True):
        if archivo is not None:
            with st.spinner("Subiendo y procesando vectores..."):
                respuesta = upload_document(archivo.name, archivo.getvalue(), sala_id)
                if respuesta.get("success"):
                    st.success(f"¡{archivo.name} indexado correctamente!")
                    st.rerun() 
                else:
                    st.error(f"Error al subir: {respuesta.get('error')}")
        else:
            st.warning("⚠️ Por favor selecciona un archivo primero.")

@st.dialog("Confirmar Eliminación")
def modal_confirmar_eliminacion(doc_id, nombre_doc):
    st.write(f"¿Estás seguro de que deseas eliminar el documento **{nombre_doc}**?")
    st.write("Esta acción borrará el archivo físico y toda su información indexada en la IA. Esta acción no se puede deshacer.")
    
    col_cancel, col_delete = st.columns(2)
    with col_cancel:
        if st.button("Cancelar", use_container_width=True):
            st.rerun() 
            
    with col_delete:
        if st.button("Sí, Eliminar", type="primary", use_container_width=True):
            with st.spinner("Eliminando documento..."):
                respuesta = delete_document(str(doc_id))
                if respuesta.get("success"):
                    st.success(f"Documento eliminado correctamente.")
                    st.rerun() 
                else:
                    st.error(f"Error al eliminar: {respuesta.get('error')}")

def my_documents_page():
    if "filtro_docs" not in st.session_state:
        st.session_state.filtro_docs = "Todos los Archivos"

    SALA_ID_PRUEBA = "sala-prueba-123"
    
    st.html("""
    <style>
        div[data-baseweb="input"] {
            border-radius: 2rem !important;
            background-color: #ffffff !important;
        }
        
        button[kind="secondary"] {
            background-color: white !important;
            color: #6b7280 !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 2rem !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            padding: 4px 16px !important;
        }
        button[kind="secondary"]:hover {
            color: #111827 !important;
            border-color: #d1d5db !important;
            background-color: #f9fafb !important;
        }
        
        button[kind="primary"] {
            background-color: #111827 !important;
            color: white !important;
            border: none !important;
            border-radius: 2rem !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            padding: 4px 16px !important;
        }
        button[kind="primary"]:hover {
            background-color: #1f2937 !important;
            color: white !important;
        }
        
        button[data-testid="stPopoverButton"] {
            background: transparent !important;
            border: none !important;
            color: #9ca3af !important;
            font-weight: bold !important;
            font-size: 20px !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        button[data-testid="stPopoverButton"]:hover {
            color: #111827 !important;
            background: transparent !important;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 2rem !important;
            background-color: #ffffff !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.03) !important;
            border: 1px solid #e5e7eb !important;
        }
    </style>
    """)

    render_sidebar()

    col_title, col_actions = st.columns([1.5, 1], vertical_alignment="bottom")
    with col_title:
        st.html("""
        <div style="margin-bottom: 5px;">
            <h2 style="margin: 0; font-weight: 700; color: #111827; font-size: 26px;">Mis Documentos</h2>
            <p style="margin: 0; color: #6b7280; font-size: 15px; margin-top: 4px;">Tu base de conocimientos indexada, lista para estudiar con IA.</p>
        </div>
        """)
        
    with col_actions:
        col_search, col_btn = st.columns([2, 1])
        with col_search:
            busqueda = st.text_input("Buscar", placeholder="Buscar documentos...", label_visibility="collapsed")
        with col_btn:
            # Icono restaurado en el botón Subir
            if st.button("Subir", icon=":material/upload:", type="primary", use_container_width=True):
                modal_subir_documento(SALA_ID_PRUEBA)

    st.divider()

    documentos_reales = get_documents(SALA_ID_PRUEBA)
    if documentos_reales is None:
        documentos_reales = []
        
    total_docs = len(documentos_reales)

    st.html(f"""
    <div style="display: flex; gap: 20px; margin-bottom: 25px;">
        <div style="flex: 1; border: 1px solid #e5e7eb; border-radius: 2.5rem; padding: 20px 30px; background-color: white; display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
            <div style="background-color: #ecfdf5; color: #10b981; min-width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;">📄</div>
            <div>
                <div style="font-size: 24px; font-weight: 700; color: #111827; line-height: 1.2;">{total_docs}</div>
                <div style="font-size: 13px; color: #6b7280; font-weight: 500;">Documentos Totales</div>
            </div>
        </div>
        <div style="flex: 1; border: 1px solid #e5e7eb; border-radius: 2.5rem; padding: 20px 30px; background-color: white; display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
            <div style="background-color: #ecfdf5; color: #10b981; min-width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;">✓</div>
            <div>
                <div style="font-size: 24px; font-weight: 700; color: #111827; line-height: 1.2;">{total_docs}</div>
                <div style="font-size: 13px; color: #6b7280; font-weight: 500;">Indexados y Listos</div>
            </div>
        </div>
    </div>
    """)

    filtros = ["Todos los Archivos", "Indexados", "Recientes"]
    cols_filtros = st.columns([1.5, 1.1, 1.1, 4], gap="small") 
    
    for i, filtro in enumerate(filtros):
        with cols_filtros[i]:
            if st.button(filtro, type="primary" if st.session_state.filtro_docs == filtro else "secondary", use_container_width=True):
                st.session_state.filtro_docs = filtro
                st.rerun()
                
    st.write("") 

    documentos_mostrar = documentos_reales.copy()
    
    if st.session_state.filtro_docs == "Indexados":
        documentos_mostrar = [doc for doc in documentos_mostrar if doc.get('estado', 'indexado').lower() == 'indexado']
    elif st.session_state.filtro_docs == "Recientes":
        documentos_mostrar = sorted(documentos_mostrar, key=lambda x: str(x.get('created_at', '')), reverse=True)[:5]

    if busqueda:
        documentos_mostrar = [
            doc for doc in documentos_mostrar 
            if busqueda.lower() in doc.get('nombre_archivo', '').lower()
        ]
    
    with st.container(border=True):
        h_name, h_date, h_status, h_action = st.columns([5, 2, 2, 0.5], vertical_alignment="center")
        header_style = "<span style='color: #9ca3af; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>"
        
        h_name.html(f"{header_style}Nombre</span>")
        h_date.html(f"{header_style}Subido</span>")
        h_status.html(f"{header_style}Estado</span>")
        
        st.divider() 
        
        if not documentos_reales:
            st.info("Aún no hay documentos en esta sala. Haz clic en '+ Subir' para indexar tu primer PDF.")
        elif not documentos_mostrar:
            st.warning("No se encontraron documentos para los filtros o búsqueda actuales.")
        else:
            for doc in documentos_mostrar:
                nombre = doc.get('nombre_archivo', 'Documento Desconocido')
                fecha = str(doc.get('created_at', 'Reciente'))[:10] 
                bg_color = "#dcfce7"
                icon_color = "#10b981"
                
                col_name, col_date, col_status, col_action = st.columns([5, 2, 2, 0.5], vertical_alignment="center")
                
                col_name.html(f"""
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background-color: {bg_color}; color: {icon_color}; min-width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">📄</div>
                    <div>
                        <div style="font-size: 14px; font-weight: 700; color: #111827;">{nombre}</div>
                        <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">Documento PDF</div>
                    </div>
                </div>
                """)
                
                col_date.html(f"<div style='font-size: 13px; color: #6b7280; font-weight: 500;'>{fecha}</div>")
                
                status_html = '<span style="background-color: #dcfce7; color: #166534; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">✓ Indexado</span>'
                col_status.html(status_html)
                
                with col_action:
                    with st.popover("···"):
                        doc_id = doc.get('id', '')
                        
                        nombre_seguro = urllib.parse.quote(nombre)
                        url_pdf = f"http://localhost:8000/static/{doc_id}_{nombre_seguro}"
                        
                        # Icono restaurado en el botón Ver Documento
                        st.link_button("Ver Documento", url=url_pdf, icon=":material/visibility:", use_container_width=True)
                            
                        # Icono restaurado en el botón Eliminar
                        if st.button("Eliminar", icon=":material/delete:", key=f"del_{doc_id}", use_container_width=True, type="secondary"):
                            modal_confirmar_eliminacion(doc_id, nombre)
                
                st.write("") 

if __name__ == "__main__":
    my_documents_page()