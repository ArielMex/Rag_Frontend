import streamlit as st

def render_study_metrics():
    # Íconos de fuego en naranja
    icon_fuego_large = '<span class="material-symbols-rounded" style="font-size: 28px; color: #ff8a00;">local_fire_department</span>'
    icon_fuego_small = '<span class="material-symbols-rounded" style="font-size: 18px; color: #ff8a00;">local_fire_department</span>'

    streak_html = f"""
    <div style="background-color: #2eb872; border-radius: 2rem; padding: 1.8rem; color: white; display: flex; flex-direction: column; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(46,184,114,0.2);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 25px;">
            <div>
                <div style="font-size: 15px; font-weight: 500; opacity: 0.9; margin-bottom: 5px;">Racha Actual</div>
                <div style="font-size: 42px; font-weight: 700; display: flex; align-items: baseline; gap: 8px; line-height: 1;">
                    12 <span style="font-size: 18px; font-weight: 500; opacity: 0.9;">días</span>
                </div>
            </div>
            <div style="background-color: rgba(255,255,255,0.7); width: 48px; height: 48px; border-radius: 50%; display: flex; justify-content: center; align-items: center;">
                {icon_fuego_large}
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
    """
    
    days = ["L", "M", "M", "J", "V", "S", "D"]
    for i, d in enumerate(days):
        bg = "rgba(255,255,255,0.7)" if i < 5 else "rgba(255,255,255,0.15)"
        icon_html = icon_fuego_small if i < 5 else ""
        
        streak_html += f"""
            <div style="display: flex; flex-direction: column; align-items: center; gap: 10px; flex: 1;">
                <div style="background-color: {bg}; width: 100%; max-width: 50px; height: 32px; border-radius: 16px; display: flex; justify-content: center; align-items: center;">
                    {icon_html}
                </div>
                <div style="font-size: 13px; font-weight: 600; opacity: 0.9;">{d}</div>
            </div>
        """
        
    streak_html += "</div></div>"
    st.html(streak_html)

    col1, col2, col3 = st.columns(3)
    
    # Lista de métricas con Material Icons inyectados directamente
    metrics = [
        {"icon_tag": '<span class="material-symbols-rounded" style="font-size: 24px;">menu_book</span>', "value": "248", "label": "Tarjetas Repasadas", "sub": "+32 hoy"},
        {"icon_tag": '<span class="material-symbols-rounded" style="font-size: 24px;">schedule</span>', "value": "4.2h", "label": "Tiempo de Estudio", "sub": "esta semana"},
        {"icon_tag": '<span class="material-symbols-rounded" style="font-size: 24px;">trending_up</span>', "value": "86%", "label": "Dominio", "sub": "+4%"}
    ]
    
    for i, col in enumerate([col1, col2, col3]):
        with col:
            m = metrics[i]
            st.html(f"""
            <div style="border: 1px solid #f3f4f6; border-radius: 2rem; padding: 1.5rem; background-color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                <div style="background-color: #ecfdf5; color: #10b981; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                    {m['icon_tag']}
                </div>
                <div style="font-size: 26px; font-weight: 700; color: #111827; margin-bottom: 2px;">{m['value']}</div>
                <div style="font-size: 14px; font-weight: 600; color: #374151;">{m['label']}</div>
                <div style="font-size: 12px; color: #9ca3af; margin-top: 6px;">{m['sub']}</div>
            </div>
            """)