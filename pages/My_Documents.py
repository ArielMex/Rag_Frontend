import streamlit as st
from components.sidebar import render_sidebar

# 1. Base de datos estática con los nombres originales intactos
DOCUMENTS = [
    {"name": "Software Architecture Patterns.pdf", "pages": 86, "date": "14 Jun, 2026", "size": "4.2 MB", "status": "Indexado", "bg": "#dcfce7", "color": "#10b981"},
    {"name": "Calculus II — Integration Techniques.pdf", "pages": 52, "date": "12 Jun, 2026", "size": "2.8 MB", "status": "Indexado", "bg": "#dbeafe", "color": "#3b82f6"},
    {"name": "Organic Chemistry — Chapter 4.pdf", "pages": 120, "date": "10 Jun, 2026", "size": "6.1 MB", "status": "Indexado", "bg": "#fef3c7", "color": "#f59e0b"},
    {"name": "Neural Networks Lecture Notes.pdf", "pages": 74, "date": "9 Jun, 2026", "size": "5.4 MB", "status": "Procesando", "bg": "#f3e8ff", "color": "#a855f7"},
    {"name": "Constitutional Law Casebook.pdf", "pages": 210, "date": "6 Jun, 2026", "size": "9.7 MB", "status": "Indexado", "bg": "#fee2e2", "color": "#ef4444"},
    {"name": "Macroeconomics — Fiscal Policy.pdf", "pages": 63, "date": "3 Jun, 2026", "size": "3.3 MB", "status": "Indexado", "bg": "#cffafe", "color": "#06b6d4"},
    {"name": "World History — Modern Era.pdf", "pages": 41, "date": "28 May, 2026", "size": "1.9 MB", "status": "Indexado", "bg": "#fce7f3", "color": "#ec4899"},
]

def my_documents_page():
    st.html("""
    <style>
        div[data-baseweb="input"] {
            border-radius: 2rem !important;
            background-color: #ffffff !important;
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
            st.text_input("Buscar", placeholder="🔍 Buscar documentos...", label_visibility="collapsed")
        with col_btn:
            st.button("☁️ Subir", type="primary", use_container_width=True)

    st.divider()

    st.html("""
    <div style="display: flex; gap: 20px; margin-bottom: 25px;">
        <div style="flex: 1; border: 1px solid #e5e7eb; border-radius: 2.5rem; padding: 20px 30px; background-color: white; display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
            <div style="background-color: #ecfdf5; color: #10b981; min-width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;">📄</div>
            <div>
                <div style="font-size: 24px; font-weight: 700; color: #111827; line-height: 1.2;">24</div>
                <div style="font-size: 13px; color: #6b7280; font-weight: 500;">Documentos Totales</div>
            </div>
        </div>
        <div style="flex: 1; border: 1px solid #e5e7eb; border-radius: 2.5rem; padding: 20px 30px; background-color: white; display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
            <div style="background-color: #ecfdf5; color: #10b981; min-width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;">🗃️</div>
            <div>
                <div style="font-size: 24px; font-weight: 700; color: #111827; line-height: 1.2;">148 MB</div>
                <div style="font-size: 13px; color: #6b7280; font-weight: 500;">Almacenamiento Usado</div>
            </div>
        </div>
        <div style="flex: 1; border: 1px solid #e5e7eb; border-radius: 2.5rem; padding: 20px 30px; background-color: white; display: flex; align-items: center; gap: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
            <div style="background-color: #ecfdf5; color: #10b981; min-width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;">✓</div>
            <div>
                <div style="font-size: 24px; font-weight: 700; color: #111827; line-height: 1.2;">22</div>
                <div style="font-size: 13px; color: #6b7280; font-weight: 500;">Indexados y Listos</div>
            </div>
        </div>
    </div>
    """)

    st.html("""
    <div style="display: flex; gap: 10px; margin-bottom: 25px;">
        <div style="background-color: #111827; color: white; padding: 8px 24px; border-radius: 2rem; font-size: 13px; font-weight: 600; cursor: pointer;">Todos los Archivos</div>
        <div style="background-color: white; color: #6b7280; border: 1px solid #e5e7eb; padding: 8px 24px; border-radius: 2rem; font-size: 13px; font-weight: 500; cursor: pointer;">Indexados</div>
        <div style="background-color: white; color: #6b7280; border: 1px solid #e5e7eb; padding: 8px 24px; border-radius: 2rem; font-size: 13px; font-weight: 500; cursor: pointer;">Procesando</div>
        <div style="background-color: white; color: #6b7280; border: 1px solid #e5e7eb; padding: 8px 24px; border-radius: 2rem; font-size: 13px; font-weight: 500; cursor: pointer;">Recientes</div>
    </div>
    """)

    with st.container(border=True):
        h_name, h_date, h_size, h_status, h_action = st.columns([4, 1.5, 1, 1.5, 0.5], vertical_alignment="center")
        header_style = "<span style='color: #9ca3af; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>"
        
        h_name.html(f"{header_style}Nombre</span>")
        h_date.html(f"{header_style}Subido</span>")
        h_size.html(f"{header_style}Tamaño</span>")
        h_status.html(f"{header_style}Estado</span>")
        
        st.divider() 
        
        for doc in DOCUMENTS:
            col_name, col_date, col_size, col_status, col_action = st.columns([4, 1.5, 1, 1.5, 0.5], vertical_alignment="center")
            
            col_name.html(f"""
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background-color: {doc['bg']}; color: {doc['color']}; min-width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">📄</div>
                <div>
                    <div style="font-size: 14px; font-weight: 700; color: #111827;">{doc['name']}</div>
                    <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">{doc['pages']} páginas</div>
                </div>
            </div>
            """)
            
            col_date.html(f"<div style='font-size: 13px; color: #6b7280; font-weight: 500;'>{doc['date']}</div>")
            col_size.html(f"<div style='font-size: 13px; color: #6b7280; font-weight: 500;'>{doc['size']}</div>")
            
            if doc['status'] == "Indexado":
                status_html = '<span style="background-color: #dcfce7; color: #166534; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">✓ Indexado</span>'
            else:
                status_html = '<span style="background-color: #f3f4f6; color: #4b5563; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">↻ Procesando</span>'
            col_status.html(status_html)
            
            with col_action:
                with st.popover("···"):
                    if st.button("👁️ Ver Documento", key=f"view_{doc['name']}", use_container_width=True):
                        st.toast(f"Abriendo {doc['name']}...")
                        
                    if st.button("🗑️ Eliminar", key=f"del_{doc['name']}", use_container_width=True, type="secondary"):
                        st.toast(f"Eliminado {doc['name']} (Simulado)")
            
            st.write("") 

if __name__ == "__main__":
    my_documents_page()