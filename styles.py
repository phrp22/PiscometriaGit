# styles.py

# Tema Escuro + Texto Branco
# styles.py

DARK_THEME_STYLE = """
<style>
/* Define o fundo escuro e cores de texto */
:root {
    --background-color: #0e1117; /* Fundo principal */
    --secondary-background-color: #161a1f; /* Fundo da sidebar */
    --text-color: #ffffff; /* Texto branco */
}

/* Aplica fundo escuro e texto branco */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--background-color) !important;
    color: var(--text-color) !important;
}

/* Sidebar com cor secundária */
section[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color) !important;
}
</style>
"""


# Estilo específico para botão "Aceitar"
ACCEPT_BUTTON_STYLE = """
<style>
.accept-container div.stButton > button {
    background-color: #28a745 !important; /* verde */
    color: #fff !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #218838 !important;
    border-radius: 8px !important;
    transition: 0.3s !important;
    padding: 10px 20px !important;
    width: 100% !important;
    text-align: center !important;
    cursor: pointer !important;
}
.accept-container div.stButton > button:hover {
    background-color: #218838 !important;
    transform: scale(1.05) !important;
}
</style>
"""

# Estilo específico para botão "Recusar"
REJECT_BUTTON_STYLE = """
<style>
.reject-container div.stButton > button {
    background-color: #dc3545 !important; /* vermelho */
    color: #fff !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #c82333 !important;
    border-radius: 8px !important;
    transition: 0.3s !important;
    padding: 10px 20px !important;
    width: 100% !important;
    text-align: center !important;
    cursor: pointer !important;
}
.reject-container div.stButton > button:hover {
    background-color: #c82333 !important;
    transform: scale(1.05) !important;
}
</style>
"""
