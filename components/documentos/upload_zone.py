import streamlit as st

def render_upload_zone():
    with st.container(border=True):
        st.html("""
        <div style="margin-bottom: 15px;">
            <h3 style="margin: 0; font-size: 18px; font-weight: 700; color: #111827;">Subir Documentos</h3>
            <p style="margin: 0; color: #6b7280; font-size: 14px; margin-top: 4px;">Arrastra PDFs para construir tu base de conocimientos</p>
        </div>
        """)
        
        uploaded_file = st.file_uploader("Arrastra y suelta tus archivos aquí", label_visibility="collapsed")
        
        st.html("""
        <div style="border: 1px solid #e5e7eb; border-radius: 1.2rem; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; background-color: #fafafa; margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background-color: white; border: 1px solid #e5e7eb; border-radius: 10px; width: 40px; height: 40px; display: flex; justify-content: center; align-items: center; font-size: 18px;">📄</div>
                <div>
                    <div style="font-size: 14px; font-weight: 600; color: #111827;">Organic Chemistry — Ch. 4.pdf</div>
                    <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">2.4 MB</div>
                </div>
            </div>
            <div style="background-color: #dcfce7; color: #166534; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                ✓ Indexado
            </div>
        </div>
        """)