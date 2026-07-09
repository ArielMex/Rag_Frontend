import streamlit as st

def render_chat_conversation():
    st.html("""
    <div style="display: flex; align-items: center; gap: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 15px; margin-bottom: 25px;">
        <div style="background-color: #2eb872; color: white; width: 42px; height: 42px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 20px;">
            ✨
        </div>
        <div>
            <div style="font-size: 16px; font-weight: 700; color: #111827;">Asistente de Estudio IA</div>
            <div style="font-size: 12px; color: #6b7280; display: flex; align-items: center; gap: 5px; margin-top: 2px;">
                <span style="color: #2eb872; font-size: 10px;">●</span> Basado en 3 documentos
            </div>
        </div>
    </div>
    """)

    st.html("""
    <div style="display: flex; justify-content: flex-end; margin-bottom: 20px;">
        <div style="background-color: #2eb872; color: white; padding: 14px 18px; border-radius: 1.5rem; border-bottom-right-radius: 0.3rem; font-size: 14px; max-width: 85%; line-height: 1.4;">
            Hazme una tarjeta de estudio sobre el ciclo del ácido cítrico del capítulo 4.
        </div>
    </div>
    """)

    st.html("""
    <div style="display: flex; justify-content: flex-start; margin-bottom: 15px;">
        <div style="background-color: #f3f4f6; color: #111827; padding: 14px 18px; border-radius: 1.5rem; border-bottom-left-radius: 0.3rem; font-size: 14px; max-width: 90%; line-height: 1.5;">
            Aquí tienes una tarjeta de estudio generada de <br>
            <span style="color: #2eb872; font-weight: 600;">📄 Organic Chemistry — Ch. 4</span>. Toca para revelar la respuesta.
        </div>
    </div>
    """)

    st.html("""
    <div style="border: 1px solid #e5e7eb; border-radius: 1.5rem; padding: 20px; background-color: white; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <div style="background-color: #ecfdf5; color: #10b981; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Pregunta</div>
            <div style="color: #9ca3af; font-size: 18px; font-weight: bold; cursor: pointer;">↻</div>
        </div>
        <div style="font-size: 16px; font-weight: 600; color: #111827; line-height: 1.5;">
            ¿Cuáles son los principales productos portadores de energía de una vuelta del ciclo del ácido cítrico?
        </div>
    </div>
    """)

    st.chat_input("Escribe tu mensaje...", key="dashboard_chat_input")