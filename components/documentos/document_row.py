import streamlit as st

def render_document_row(doc):
    # Imitamos el grid-cols-12: 5 columnas para nombre, 2 fecha, 2 tamaño, 2 estatus, 1 acciones
    col_name, col_date, col_size, col_status, col_actions = st.columns([5, 2, 2, 2, 1], vertical_alignment="center")
    
    with col_name:
        # Icono + Nombre y Páginas
        st.markdown(f"📄 **{doc['name']}**")
        st.caption(f"{doc['pages']} pages")
        
    with col_date:
        st.markdown(f"<span style='font-size: 0.9em; color: gray;'>{doc['date']}</span>", unsafe_allow_html=True)
        
    with col_size:
        st.markdown(f"<span style='font-size: 0.9em; color: gray;'>{doc['size']}</span>", unsafe_allow_html=True)
        
    with col_status:
        # Etiqueta de estatus con color dinámico
        if doc['status'] == "Indexed":
            st.success("🟢 Indexed", icon=None)
        else:
            st.info("🔄 Processing", icon=None)
            
    with col_actions:
        # El botón de los tres puntos que abre el submenú
        with st.popover("..."):
            st.button("👁️ View", key=f"view_{doc['id']}", use_container_width=True)
            st.button("🗑️ Delete", key=f"delete_{doc['id']}", type="primary", use_container_width=True)
            
    st.divider() # Línea sutil de separación