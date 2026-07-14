import streamlit as st

def render_room_card(room):
    with st.container(border=True):
        
        status_bg = "#dcfce7" if room['live'] else "#f3f4f6"
        status_text = "#166534" if room['live'] else "#4b5563"
        status_dot = "● " if room['live'] else ""
        status_label = "En vivo" if room['live'] else "Programada"

        card_html = f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
            <div style="background-color: #dcfce7; color: #10b981; width: 44px; height: 44px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 22px;">
                {room['icon']}
            </div>
            <div style="background-color: {status_bg}; color: {status_text}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">
                {status_dot}{status_label}
            </div>
        </div>
        <div style="font-size: 11px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
            {room['topic']}
        </div>
        <div style="font-size: 18px; font-weight: 700; color: #111827; margin-bottom: 6px;">
            {room['title']}
        </div>
        <div style="font-size: 13px; color: #6b7280; margin-bottom: 25px;">
            {room['nextSession']}
        </div>
        """
        
        st.html(card_html)

        col_avatars, col_btn = st.columns([1.2, 1], vertical_alignment="center")

        with col_avatars:
            avatars_html = "<div style='display: flex; align-items: center;'>"
            colors = ["#fca5a5", "#fdba74", "#fcd34d", "#86efac", "#93c5fd"] 
            
            for i, member in enumerate(room['members'][:3]):
                initial = member['name'][0]
                z_index = 10 - i
                margin = "-12px" if i > 0 else "0"
                
                avatars_html += f"""
                <div style='width: 32px; height: 32px; border-radius: 50%; background-color: {colors[i % 5]}; border: 2px solid white; display: flex; justify-content: center; align-items: center; font-size: 13px; font-weight: bold; color: #374151; margin-left: {margin}; z-index: {z_index};'>
                    {initial}
                </div>
                """
            
            if len(room['members']) > 3:
                extra = len(room['members']) - 3
                avatars_html += f"<div style='font-size: 12px; color: #6b7280; margin-left: 8px; font-weight: 600;'>+{extra}</div>"
            
            avatars_html += "</div>"
            
            st.html(avatars_html)

        with col_btn:
            btn_type = "primary" if room['live'] else "secondary"
            st.button("Unirse", key=f"join_{room['id']}", type=btn_type, use_container_width=True)