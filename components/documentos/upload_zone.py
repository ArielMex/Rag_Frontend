import streamlit as st
from utils.api_client import upload_document

def render_upload_zone():
    # 1. Buscamos la sala activa. Si no hay (ej. estamos en el Dashboard), usamos un ID personal.
    sala_id = st.session_state.get("sala_activa", "espacio_personal_default")

    with st.container(border=True):
        # 2. Tu encabezado visual
        st.html("""
        <div style="margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827;">Subir Documentos</h3>
            <p style="margin: 0; color: #6b7280; font-size: 14px; margin-top: 4px;">Arrastra PDFs para construir tu base de conocimientos</p>
        </div>
        """)
        
        # 3. El uploader nativo de Streamlit
        uploaded_file = st.file_uploader("Arrastra y suelta tus archivos aquí", label_visibility="collapsed")
        
        # 4. La lógica de conexión dinámica
        if uploaded_file:
            # Agregamos un botón para confirmar la subida
            if st.button("Procesar e Indexar", type="primary"):
                with st.spinner("Procesando con IA..."):
                    
                    file_bytes = uploaded_file.getvalue()
                    resultado = upload_document(
                        file_name=uploaded_file.name,
                        file_bytes=file_bytes,
                        sala_id=sala_id  # <-- Usa la sala colaborativa o el espacio personal
                    )
                    
                    if resultado["success"]:
                        # 5. Tu tarjeta visual de éxito con variables dinámicas
                        peso_mb = uploaded_file.size / (1024 * 1024)
                        st.html(f"""
                        <div style="border: 1px solid #e5e7eb; border-radius: 1.2rem; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; background-color: #fafafa; margin-top: 20px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="background-color: white; border: 1px solid #e5e7eb; border-radius: 10px; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; font-size: 18px;">📄</div>
                                <div>
                                    <div style="font-size: 14px; font-weight: 600; color: #111827;">{uploaded_file.name}</div>
                                    <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">{peso_mb:.1f} MB</div>
                                </div>
                            </div>
                            <div style="background-color: #dcfce7; color: #166534; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                                ✓ Indexado
                            </div>
                        </div>
                        """)
                    else:
                        st.error(resultado["error"])