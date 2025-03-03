import streamlit as st
import streamlit.components.v1 as components

def inject_css():
    """Carrega o CSS do styles.html e insere no app via st.components.v1.html()"""
    with open("styles.html", "r", encoding="utf-8") as f:
        css_content = f.read()
    components.html(f"<style>{css_content}</style>", height=0)
