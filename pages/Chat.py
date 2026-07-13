import streamlit as st
import re

from components.sidebar import render_sidebar
from utils.api_client import send_chat_message, generar_quiz_api

# Importamos ambos paneles
from components.chat.quiz_panel import render_quiz_panel
from components.chat.flashcard_panel import render_flashcards_panel

def detectar_intencion(mensaje: str):
    """
    Analiza si el usuario quiere un quiz o flashcards.
    Retorna (tema, cantidad, tipo_panel)
    """
    # 1. ¿Quiere Flashcards? (Ej: "Genera 5 flashcards sobre git")
    patron_fc = r"(?:genera|crea|haz|hazme)\s+(?:unas\s+)?(\d+)?\s*(?:flashcards|tarjetas|fichas)(?:\s+de\s+estudio)?\s+(?:de|sobre)\s+(.+)"
    match_fc = re.search(patron_fc, mensaje, re.IGNORECASE)
    
    if match_fc:
        cantidad = int(match_fc.group(1)) if match_fc.group(1) else 3
        tema = match_fc.group(2).strip().rstrip('.!?')
        return tema, cantidad, "flashcards"

    # 2. ¿Quiere Quiz? 
    patron_quiz = r"(?:genera|crea|haz|hazme)\s+(?:un\s+)?(?:quiz|cuestionario|examen|evaluacion|evaluación)"
    if re.search(patron_quiz, mensaje, re.IGNORECASE):
        cantidad = 3
        match_cantidad = re.search(r"(\d+)\s+preguntas?", mensaje, re.IGNORECASE)
        if match_cantidad:
            cantidad = int(match_cantidad.group(1))
            
        mensaje_limpio = re.sub(r"(?:de\s+)?\d+\s+preguntas?", "", mensaje, flags=re.IGNORECASE)
        match_tema = re.search(r"(?:de|sobre)\s+(.+)", mensaje_limpio, re.IGNORECASE)
        
        if match_tema:
            tema = match_tema.group(1).strip().rstrip('.!?')
            return tema, cantidad, "quiz"

    return None, None, None

def render_interfaz_chat():
    """Renderiza el componente del Chat de Lumina y maneja el enrutamiento de peticiones."""
    with st.container(border=True, height=750):
        # Encabezado fijo
        st.html("""
        <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 15px;">
            <div style="background-color: #2eb872; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">✨</div>
            <div>
                <div style="font-size: 15px; font-weight: 700; color: #111827;">Lumina - Asistente de Estudio IA</div>
                <div style="font-size: 11px; color: #6b7280;">● Conectado a Gemini</div>
            </div>
        </div>
        """)

        # Contenedor para los mensajes (con scroll interno)
        contenedor_mensajes = st.container(height=550, border=False)
        
        with contenedor_mensajes:
            for msg in st.session_state.historial_chat:
                if msg["role"] == "user":
                    st.html(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                        <div style="background-color: #2eb872; color: white; padding: 14px 18px; border-radius: 1.5rem; border-bottom-right-radius: 0.3rem; font-size: 14px; max-width: 85%; line-height: 1.5;">
                            {msg['content']}
                        </div>
                    </div>
                    """)
                else:
                    texto_formateado = msg['content'].replace('\n', '<br>')
                    st.html(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 15px;">
                        <div style="background-color: #f3f4f6; color: #111827; padding: 14px 18px; border-radius: 1.5rem; border-bottom-left-radius: 0.3rem; font-size: 14px; max-width: 90%; line-height: 1.6;">
                            {texto_formateado}
                        </div>
                    </div>
                    """)

        # Caja de texto y lógica de intercepción
        if prompt := st.chat_input("Escribe aqui lo que quieres, un quiz, flashcard o chatea normal...", key="chat_eval_input"):
            
            st.session_state.historial_chat.append({"role": "user", "content": prompt})
            
            # Usamos un ID fijo para las pruebas ya que aún no hay sistema de salas
            ID_SALA_PRUEBA = "sala-prueba-123"
            
            with contenedor_mensajes:
                # Pintamos la pregunta del usuario inmediatamente
                st.html(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                    <div style="background-color: #2eb872; color: white; padding: 14px 18px; border-radius: 1.5rem; border-bottom-right-radius: 0.3rem; font-size: 14px; max-width: 85%; line-height: 1.5;">
                        {prompt}
                    </div>
                </div>
                """)
                
                # EL CEREBRO DE ENRUTAMIENTO (Chat Normal vs Quiz vs Flashcards)
                tema_detectado, cantidad_preguntas, tipo_panel = detectar_intencion(prompt)
                
                if tema_detectado:
                    with st.spinner(f"Diseñando {cantidad_preguntas} {tipo_panel} sobre '{tema_detectado}'..."):
                        # Le pasamos la cantidad a la API (reutilizamos la misma API del quiz)
                        respuesta_api = generar_quiz_api(sala_id=ID_SALA_PRUEBA, tema=tema_detectado, cantidad_preguntas=cantidad_preguntas)
                        
                        if respuesta_api["success"]:
                            st.session_state.datos_quiz = respuesta_api["data"]
                            st.session_state.tipo_panel_activo = tipo_panel # Guardamos qué pidió el usuario
                            st.session_state.quiz_activo = True
                            texto_ia = f"¡Listo! He generado tu material de **{tipo_panel}** sobre **{tema_detectado}**. El panel interactivo se ha abierto a la derecha."
                        else:
                            texto_ia = f"Hubo un error al generar: {respuesta_api['error']}"
                else:
                    with st.spinner("Lumina está pensando..."):
                        respuesta_api = send_chat_message(pregunta=prompt, sala_id=ID_SALA_PRUEBA)
                        
                        if respuesta_api["success"]:
                            texto_ia = respuesta_api["data"]
                        else:
                            texto_ia = f"Hubo un error de conexión: {respuesta_api['error']}"

            # Guardamos la respuesta final y recargamos
            st.session_state.historial_chat.append({"role": "assistant", "content": texto_ia})
            st.rerun()

def chat_page():
    # Inicialización de estados con el nuevo mensaje de bienvenida
    if "historial_chat" not in st.session_state:
        mensaje_bienvenida = (
            "¡Hola! Soy Lumina, tu asistente de estudio avanzado. Estoy lista para resolver "
            "cualquier duda profunda sobre tus documentos. Puedes pedirme que genere "
            "Quizzes interactivos o Tarjetas de Estudio (Flashcards) para poner a prueba tu conocimiento. "
            "(Ej: 'Hazme un quiz de 5 preguntas sobre bases de datos')."
        )
        st.session_state.historial_chat = [
            {"role": "assistant", "content": mensaje_bienvenida}
        ]
        
    if "quiz_activo" not in st.session_state:
        st.session_state.quiz_activo = False
    if "datos_quiz" not in st.session_state:
        st.session_state.datos_quiz = None
    if "tipo_panel_activo" not in st.session_state:
        st.session_state.tipo_panel_activo = "quiz" # Por defecto

    # Estilos globales de la página
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
        .st-emotion-cache-1wmy9hl { overflow: hidden; }
    </style>
    """)

    render_sidebar()
    
    # Encabezado principal
    st.html("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; font-weight: 700; color: #111827; font-size: 26px;">Chat IA y Evaluaciones</h2>
        <p style="margin: 0; color: #6b7280; font-size: 15px; margin-top: 4px;">Chatea con tus fuentes o pídele a Lumina que genere cuestionarios (Ej: "Hazme un quiz de TCP")</p>
    </div>
    """)
    st.divider()

    # ==========================================
    # LÓGICA DE RENDERIZADO DINÁMICO
    # ==========================================
    if not st.session_state.quiz_activo:
        # MODO 1: Solo el chat centrado. 
        espacio_izq, col_centro, espacio_der = st.columns([1, 2, 1])
        with col_centro:
            render_interfaz_chat()
    else:
        # MODO 2: Pantalla dividida
        col_chat, col_panel = st.columns(2, gap="large")
        with col_chat:
            render_interfaz_chat()
        with col_panel:
            if st.session_state.datos_quiz:
                with st.container(border=True, height=750):
                    # DECIDIMOS QUÉ COMPONENTE PINTAR BASADO EN EL ESTADO
                    if st.session_state.get("tipo_panel_activo") == "flashcards":
                        render_flashcards_panel(st.session_state.datos_quiz)
                    else:
                        render_quiz_panel(st.session_state.datos_quiz)
            else:
                st.error("⚠️ No se encontraron datos para la evaluación.")

if __name__ == "__main__":
    chat_page()