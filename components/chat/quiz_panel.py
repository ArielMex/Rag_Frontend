import streamlit as st

def render_quiz_panel(datos_quiz):
    """
    Renderiza el panel de evaluación dinámicamente basado en un diccionario JSON.
    """
    # Inicializamos el estado para este quiz específico si no existe
    if "quiz_completado" not in st.session_state:
        st.session_state.quiz_completado = False

    is_done = st.session_state.quiz_completado
    
    preguntas = datos_quiz["evaluacion"]["preguntas"]
    total_q = len(preguntas)
    score_badge = f'<div style="background-color: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 700;">{total_q}/{total_q}</div>' if is_done else ''

    # Encabezado del Quiz
    st.html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background-color: #ecfdf5; color: #10b981; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">📋</div>
            <div>
                <div style="font-size: 15px; font-weight: 700; color: #111827;">Evaluación Generada</div>
                <div style="font-size: 11px; color: #6b7280;">{total_q} preguntas · {datos_quiz['evaluacion']['titulo']}</div>
            </div>
        </div>
        {score_badge}
    </div>
    """)

    # Usamos formularios nativos de Streamlit para manejar las respuestas de forma limpia
    with st.form(key="quiz_form", border=False):
        respuestas_usuario = {}
        puntaje_actual = 0
        
        for idx, p in enumerate(preguntas):
            st.html(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                <span style="background-color: #ecfdf5; color: #10b981; padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; text-transform: uppercase;">{p['tipo']}</span>
                <span style="color: #9ca3af; font-size: 12px; font-weight: 500;">Pregunta {idx + 1}</span>
            </div>
            <div style="font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 10px;">
                {p['pregunta']}
            </div>
            """)
            
            # Renderizamos los radio buttons nativos
            respuestas_usuario[p['id']] = st.radio(
                label=f"Pregunta {idx}", 
                options=p["opciones"], 
                index=None, 
                label_visibility="collapsed",
                key=f"q_{p['id']}",
                disabled=is_done
            )
            
            # Si ya se envió, mostramos retroalimentación individual
            if is_done:
                es_correcta = respuestas_usuario[p['id']] == p["respuesta_correcta"]
                if es_correcta:
                    st.success(f"¡Correcto! La respuesta es: {p['respuesta_correcta']}")
                    puntaje_actual += 1
                else:
                    st.error(f"Incorrecto. La respuesta correcta era: {p['respuesta_correcta']}")
            st.divider()

        # Botón de envío
        if not is_done:
            st.html('<style>div[data-testid="stFormSubmitButton"] button { background-color: #a7f3d0 !important; color: white !important; border: none !important; width: 100%;} div[data-testid="stFormSubmitButton"] button:hover { background-color: #2eb872 !important; }</style>')
            enviado = st.form_submit_button("Enviar Respuestas")
            if enviado:
                # Validar que respondió todas
                if None in respuestas_usuario.values():
                    st.warning("⚠️ Por favor, responde todas las preguntas antes de enviar.")
                else:
                    st.session_state.quiz_completado = True
                    st.rerun()

    # Botón de reinicio (fuera del formulario)
    if is_done:
        st.info(f"Obtuviste {puntaje_actual} de {total_q} respuestas correctas.")
        if st.button("↻ Repetir Evaluación", use_container_width=True):
            st.session_state.quiz_completado = False
            # Limpiamos las respuestas guardadas en sesión
            for p in preguntas:
                if f"q_{p['id']}" in st.session_state:
                    del st.session_state[f"q_{p['id']}"]
            st.rerun()