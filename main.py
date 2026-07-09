import streamlit as st
from components.auth.login_form import render_login_form
from components.auth.register_form import render_register_form

st.set_page_config(
    page_title="Lumina - Learning Studio",
    page_icon="🎓",
    layout="wide"
)

def main():
    st.html("""
    <style>
        header[data-testid="stHeader"], .stAppHeader {
            display: none !important;
            visibility: hidden !important;
        }
    </style>
    """)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "auth_view" not in st.session_state:
        st.session_state.auth_view = "login"

    if not st.session_state.logged_in:
        if st.session_state.auth_view == "login":
            render_login_form()
        else:
            render_register_form()
    else:
        st.switch_page("pages/Dashboard.py")

if __name__ == "__main__":
    main()