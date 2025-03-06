import streamlit as st
import pathlib

# 🦄 Carrega o CCS para estilizar o visual, aplicando no Streamlit um design mais legal.
def load_css():
    css_path = pathlib.Path("assets/styles.css") # O caminho do estilo, fixo no trilho. 
    # Se o caminho estiver correto...
    if css_path.exists():
        with open(css_path, "r") as f: # Abrimos o código para leitura.
            css_content = f.read() # Pegamos o conteúdo e guardamos para consulta.
            st.html(f"<style>{css_content}</style>")  # Agora é só aplicar, não tem desculpa!
