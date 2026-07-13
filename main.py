import streamlit as st

try:
    from components.auth.login_form import render_login_form
except Exception:
    def render_login_form():
        st.error("No se pudo cargar el formulario de login.")

try:
    from components.auth.register_form import render_register_form
except Exception:
    def render_register_form():
        st.error("No se pudo cargar el formulario de registro.")

st.set_page_config(
    page_title="Lumina - IA de Estudio",
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

    # Siempre arrancar en login al abrir la app, para que el cambio sea visible
    # y evitar que una sesión previa deje la vista en registro.
    if st.session_state.get("auth_view") not in {"login", "register"}:
        st.session_state.auth_view = "login"

    if not st.session_state.logged_in:
        if st.session_state.auth_view == "login":
            render_login_form()
        else:
            render_register_form()
    else:
        try:
            st.switch_page("pages/Dashboard.py")
        except Exception:
            st.info("La página de dashboard aún no está disponible, pero puedes seguir usando el login.")

if __name__ == "__main__":
    main()