import streamlit as st
from utils.api_client import send_chat_message

def render_chat_conversation(modo_mini=False):
    # 1. ENCABEZADO
    st.html("""
    <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 15px;">
        <div style="background-color: #2eb872; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">✨</div>
        <div>
            <div style="font-size: 15px; font-weight: 700; color: #111827;">Lumina - Asistente de Estudio IA</div>
            <div style="font-size: 11px; color: #6b7280;">● Conectado a Gemini</div>
        </div>
    </div>
    """)

    # 2. INICIALIZAR HISTORIAL DE CHAT
    if "dashboard_messages" not in st.session_state:
        mensaje_bienvenida = (
            "¡Hola! Puedo resolver dudas rápidas sobre tus documentos aquí. "
            "(Para generar Quizzes o Flashcards, por favor ve a la vista completa de CHAT IA)."
            if modo_mini else "¡Hola! ¿Qué vamos a estudiar hoy?"
        )
        st.session_state.dashboard_messages = [
            {"role": "assistant", "content": mensaje_bienvenida}
        ]

    # 3. CONTENEDOR DE MENSAJES CON SCROLL (Ajuste de altura dinámico)
    # Reducimos la altura a 350 si estamos en el dashboard para evitar la doble barra
    altura_chat = 350 if modo_mini else 550
    contenedor_mensajes = st.container(height=altura_chat, border=False)
    
    with contenedor_mensajes:
        # PINTAMOS EL HISTORIAL
        for msg in st.session_state.dashboard_messages:
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

    # 4. ENTRADA DE TEXTO Y PROCESAMIENTO
    if prompt := st.chat_input("Escribe tu pregunta sobre los documentos...", key="dashboard_input"):
        
        # Guardamos el mensaje en el estado
        st.session_state.dashboard_messages.append({"role": "user", "content": prompt})
        
        with contenedor_mensajes:
            # Pintamos la burbuja del usuario inmediatamente
            st.html(f"""
            <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
                <div style="background-color: #2eb872; color: white; padding: 14px 18px; border-radius: 1.5rem; border-bottom-right-radius: 0.3rem; font-size: 14px; max-width: 85%; line-height: 1.5;">
                    {prompt}
                </div>
            </div>
            """)

            with st.spinner("Lumina está pensando..."):
                # Llamada a la API
                respuesta_api = send_chat_message(pregunta=prompt, sala_id="sala-prueba-123", modo_mini=modo_mini)
                
                # Desempaquetado seguro de la respuesta
                if isinstance(respuesta_api, dict) and "success" in respuesta_api:
                    if respuesta_api["success"]:
                        texto_ia = respuesta_api["data"]
                    else:
                        texto_ia = f"Hubo un error de conexión: {respuesta_api.get('error', 'Desconocido')}"
                else:
                    texto_ia = str(respuesta_api)

                st.session_state.dashboard_messages.append({"role": "assistant", "content": texto_ia})
                st.rerun()