import streamlit as st
import streamlit.components.v1 as components

<style>
/* Estilo global para botões */
div.stButton > button {
    background-color: #7159c1 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #836fff !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out !important;
    width: 100% !important;
    padding: 12px 24px !important;
    text-align: center !important;
    box-shadow: 0px 0px 10px rgba(113, 89, 193, 0.5) !important;
    outline: none !important;
}

/* Efeito de hover - Aumenta o botão ao passar o mouse */
div.stButton > button:hover {
    transform: scale(1.05) !important;
}

/* Botões personalizados */
.accept-button {
    background-color: #28a745 !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #218838 !important;
    border-radius: 8px !important;
    transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out !important;
    padding: 10px 20px !important;
    cursor: pointer !important;
}

.accept-button:hover {
    background-color: #218838 !important;
    transform: scale(1.1) !important;
}

.reject-button {
    background-color: #dc3545 !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #c82333 !important;
    border-radius: 8px !important;
    transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out !important;
    padding: 10px 20px !important;
    cursor: pointer !important;
}

.reject-button:hover {
    background-color: #c82333 !important;
    transform: scale(1.1) !important;
}
</style>

def inject_css():
    """Carrega o arquivo styles.html e insere no app via st.components.v1.html()"""
    with open("styles.html", "r", encoding="utf-8") as f:
        css_content = f.read()
    components.html(css_content, height=0)  # Insere o CSS de forma isolada