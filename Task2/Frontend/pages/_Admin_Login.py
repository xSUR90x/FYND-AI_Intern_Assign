import streamlit as st

ADMIN_PASSWORD = st.secrets["ADMIN_PASSWORD"]


def go_dashboard():
    st.switch_page("pages/ADMIN_dashboard.py")


def go_home():
    st.session_state.admin_logged_in = False
    st.switch_page("Home.py")


def logout():
    st.session_state.admin_logged_in = False
    st.switch_page("pages/_Admin_Login.py")


if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


# ================================
# ALREADY LOGGED IN
# ================================
if st.session_state.admin_logged_in:

    st.success("✅ You are already logged in as Admin")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Go to Admin Dashboard"):
            go_dashboard()

    with col2:
        if st.button("Logout"):
            logout()

    st.stop()


# ================================
# LOGIN PAGE
# ================================
st.title("🔑 Admin Login")

pwd = st.text_input("Admin password", type="password")

col1, col2 = st.columns(2)

if col1.button("Login"):
    if pwd == ADMIN_PASSWORD:
        st.session_state.admin_logged_in = True
        go_dashboard()
    else:
        st.error("❌ Incorrect password")

if col2.button("Back to Home"):
    go_home()
