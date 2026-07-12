import streamlit as st

def render_flashcards_panel(datos_quiz):
    """
    Renderiza el panel de flashcards reutilizando el JSON del Quiz.
    """
    preguntas = datos_quiz["evaluacion"]["preguntas"]
    total = len(preguntas)
    
    st.html(f"""
    <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 20px;">
        <div style="background-color: #fef3c7; color: #d97706; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px;">🃏</div>
        <div>
            <div style="font-size: 15px; font-weight: 700; color: #111827;">Tarjetas de Estudio (Flashcards)</div>
            <div style="font-size: 11px; color: #6b7280;">{total} tarjetas · {datos_quiz['evaluacion']['titulo']}</div>
        </div>
    </div>
    """)
    
    # Renderizamos cada "pregunta" como el anverso y cada "respuesta" como el reverso
    for idx, p in enumerate(preguntas):
        with st.container(border=True):
            # Anverso
            st.markdown(f"**{idx + 1}.** {p['pregunta']}")
            
            # Reverso (oculto en un acordeón)
            with st.expander("Girar tarjeta ⬇️"):
                st.success(f"**Concepto clave:** {p['respuesta_correcta']}")
                
    if st.button("Cerrar Flashcards", use_container_width=True):
        st.session_state.quiz_activo = False
        st.rerun()