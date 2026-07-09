import streamlit as st

def render_study_metrics():
    streak_html = """
    <div style="background-color: #2eb872; border-radius: 2rem; padding: 1.8rem; color: white; display: flex; flex-direction: column; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(46,184,114,0.2);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px;">
            <div>
                <div style="font-size: 15px; font-weight: 500; opacity: 0.9; margin-bottom: 5px;">Racha Actual</div>
                <div style="font-size: 42px; font-weight: 700; display: flex; align-items: baseline; gap: 8px; line-height: 1;">
                    12 <span style="font-size: 18px; font-weight: 500; opacity: 0.9;">días</span>
                </div>
            </div>
            <div style="background-color: rgba(255,255,255,0.25); width: 48px; height: 48px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;">
                🔥
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
    """
    
    days = ["L", "M", "M", "J", "V", "S", "D"]
    for i, d in enumerate(days):
        bg = "rgba(255,255,255,0.35)" if i < 5 else "rgba(255,255,255,0.15)"
        icon = "🔥" if i < 5 else ""
        streak_html += f"""
            <div style="display: flex; flex-direction: column; align-items: center; gap: 10px; flex: 1;">
                <div style="background-color: {bg}; width: 100%; max-width: 50px; height: 32px; border-radius: 16px; display: flex; justify-content: center; align-items: center; font-size: 15px;">
                    {icon}
                </div>
                <div style="font-size: 13px; font-weight: 600; opacity: 0.9;">{d}</div>
            </div>
        """
        
    streak_html += "</div></div>"
    st.html(streak_html)

    col1, col2, col3 = st.columns(3)
    metrics = [
        {"icon": "📖", "value": "248", "label": "Tarjetas Repasadas", "sub": "+32 hoy"},
        {"icon": "🕒", "value": "4.2h", "label": "Tiempo de Estudio", "sub": "esta semana"},
        {"icon": "📈", "value": "86%", "label": "Dominio", "sub": "+4%"}
    ]
    
    for i, col in enumerate([col1, col2, col3]):
        with col:
            m = metrics[i]
            st.html(f"""
            <div style="border: 1px solid #f3f4f6; border-radius: 2rem; padding: 1.5rem; background-color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                <div style="background-color: #ecfdf5; color: #10b981; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 18px; margin-bottom: 20px;">
                    {m['icon']}
                </div>
                <div style="font-size: 26px; font-weight: 700; color: #111827; margin-bottom: 2px;">{m['value']}</div>
                <div style="font-size: 14px; font-weight: 600; color: #374151;">{m['label']}</div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 6px;">{m['sub']}</div>
            </div>
            """)