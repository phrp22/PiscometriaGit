import streamlit as st
from auth import get_user
from layout import render_main_layout
from dashboard import render_dashboard

st.set_page_config(
    page_title="Academia Diagnóstica",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def main():
    user = get_user()
    if user:
        render_dashboard()
    else:
        render_main_layout()

    if st.session_state.get("refresh", False):
        st.session_state["refresh"] = False
        st.rerun()

if __name__ == "__main__":
    if "user" not in st.session_state:
        st.session_state["user"] = None
    main()
