import streamlit as st
import json
from components.sidebar import render_sidebar

# 1. MOCK: Así llegará la respuesta de tu FastAPI + LLM
MOCK_RAG_RESPONSE = """
{
  "respuesta_texto": "<b>TCP</b> está orientado a la conexión y garantiza una entrega ordenada y confiable mediante handshakes y confirmaciones. <b>UDP</b> no tiene conexión — envía datagramas sin confirmación, intercambiando confiabilidad por una menor latencia.<br><br>TCP es ideal para transferencias de archivos y páginas web; UDP es ideal para video en vivo, juegos y búsquedas de DNS donde la velocidad importa más que una entrega perfecta.",
  "evaluacion": {
    "titulo": "TCP vs UDP",
    "preguntas": [
      {
        "id": 1,
        "tipo": "Opción Múltiple",
        "pregunta": "¿Qué protocolo es más apropiado para una videollamada en vivo?",
        "opciones": ["TCP", "UDP", "FTP", "SMTP"],
        "respuesta_correcta": "UDP"
      },
      {
        "id": 2,
        "tipo": "Opción Múltiple",
        "pregunta": "¿Qué mecanismo utiliza TCP para establecer una conexión?",
        "opciones": ["Handshake de dos vías", "Handshake de tres vías", "Paso de testigo", "Inundación de difusión"],
        "respuesta_correcta": "Handshake de tres vías"
      }
    ]
  }
}
"""

def chat_page():
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False

    st.html("""
    <style>
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 1.5rem !important;
            background-color: #ffffff !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.02) !important;
            border: 1px solid #e5e7eb !important;
        }
        div[data-testid="stChatInput"] { border-radius: 2rem !important; }
        div[data-testid="stButton"] button {
            border-radius: 2rem !important;
            font-weight: 600 !important;
            padding: 0.75rem !important;
        }
    </style>
    """)

    render_sidebar()
    
    st.html("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; font-weight: 700; color: #111827; font-size: 26px;">Chat IA y Evaluaciones</h2>
        <p style="margin: 0; color: #6b7280; font-size: 15px; margin-top: 4px;">Chatea con tus fuentes y ponte a prueba con cuestionarios generados</p>
    </div>
    """)
    st.divider()

    col_chat, col_quiz = st.columns(2, gap="large")
    datos_ia = json.loads(MOCK_RAG_RESPONSE)

    with col_chat:
        with st.container(border=True, height=750):
            st.html("""
            <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 25px;">
                <div style="background-color: #2eb872; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">✨</div>
                <div>
                    <div style="font-size: 15px; font-weight: 700; color: #111827;">Asistente de Estudio IA</div>
                    <div style="font-size: 11px; color: #6b7280;">● Basado en 3 documentos</div>
                </div>
            </div>
            """)

            st.html("""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                <div style="background-color: #2eb872; color: white; padding: 14px 18px; border-radius: 1.5rem; border-bottom-right-radius: 0.3rem; font-size: 14px; max-width: 85%; line-height: 1.5;">
                    Explica la diferencia entre TCP y UDP, y hazme un cuestionario al respecto.
                </div>
            </div>
            """)

            # Inyectamos el texto del JSON
            st.html(f"""
            <div style="display: flex; justify-content: flex-start; margin-bottom: 15px;">
                <div style="background-color: #f3f4f6; color: #111827; padding: 14px 18px; border-radius: 1.5rem; border-bottom-left-radius: 0.3rem; font-size: 14px; max-width: 90%; line-height: 1.6;">
                    {datos_ia['respuesta_texto']}
                </div>
            </div>
            """)

            st.html("""
            <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; padding-left: 10px;">
                <div style="display: inline-flex; align-items: center; gap: 6px; border: 1px solid #e5e7eb; padding: 4px 12px; border-radius: 20px; font-size: 11px; color: #6b7280; width: fit-content; background: white;">
                    <span style="color: #2eb872;">📄</span> <span style="color: #10b981; font-weight: 600;">Computer Networks — Ch. 6</span> p. 212
                </div>
            </div>
            """)
            st.chat_input("Pregunta cualquier cosa sobre tus documentos...", key="chat_eval_input")

    with col_quiz:
        with st.container(border=True, height=750):
            is_done = st.session_state.quiz_completed
            opt_default = "border: 1px solid #e5e7eb; background: white; color: #111827;"
            opt_selected = "border: 1px solid #2eb872; background: #2eb872; color: white;"
            
            preguntas = datos_ia["evaluacion"]["preguntas"]
            total_q = len(preguntas)
            score_badge = f'<div style="background-color: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 700;">{total_q}/{total_q}</div>' if is_done else ''

            st.html(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background-color: #ecfdf5; color: #10b981; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">📋</div>
                    <div>
                        <div style="font-size: 15px; font-weight: 700; color: #111827;">Evaluación Generada</div>
                        <div style="font-size: 11px; color: #6b7280;">{total_q} preguntas · {datos_ia['evaluacion']['titulo']}</div>
                    </div>
                </div>
                {score_badge}
            </div>
            """)

            # Ciclo dinámico que dibuja el JSON
            for idx, p in enumerate(preguntas):
                html_opciones = ""
                for opcion in p["opciones"]:
                    es_correcta = (opcion == p["respuesta_correcta"])
                    estilo = opt_selected if (is_done and es_correcta) else opt_default
                    icono = "✓" if (is_done and es_correcta) else ""
                    
                    html_opciones += f"""
                    <div style="{estilo} padding: 12px 20px; border-radius: 1rem; font-size: 13px; font-weight: 500; display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>{opcion}</span> <span>{icono}</span>
                    </div>
                    """
                
                st.html(f"""
                <div style="background-color: #fafafa; border: 1px solid #f3f4f6; border-radius: 1.5rem; padding: 20px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                        <span style="background-color: #ecfdf5; color: #10b981; padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; text-transform: uppercase;">{p['tipo']}</span>
                        <span style="color: #9ca3af; font-size: 12px; font-weight: 500;">Pregunta {idx + 1}</span>
                    </div>
                    <div style="font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 15px;">
                        {p['pregunta']}
                    </div>
                    <div style="display: flex; flex-direction: column;">
                        {html_opciones}
                    </div>
                </div>
                """)

            st.write("")

            if not is_done:
                st.html('<style>div[data-testid="stButton"] button { background-color: #a7f3d0 !important; color: white !important; border: none !important; } div[data-testid="stButton"] button:hover { background-color: #2eb872 !important; }</style>')
                if st.button(f"Responder todas las preguntas (0/{total_q})", use_container_width=True):
                    st.session_state.quiz_completed = True
                    st.rerun()
            else:
                st.html('<style>div[data-testid="stButton"] button { background-color: #f3f4f6 !important; color: #374151 !important; border: none !important; } div[data-testid="stButton"] button:hover { background-color: #e5e7eb !important; }</style>')
                if st.button("↻ Repetir Evaluación", use_container_width=True):
                    st.session_state.quiz_completed = False
                    st.rerun()

if __name__ == "__main__":
    chat_page()