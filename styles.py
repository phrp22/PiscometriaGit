# styles.py

# 🌑 Tema Escuro (Aplicado Globalmente)
DARK_THEME_STYLE = """
<style>
/* Define o fundo escuro e cores de texto */
:root {
    --background-color: #0e1117;
    --secondary-background-color: #161a1f;
    --text-color: #ffffff;
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

# ✅ Estilo para Botão "Aceitar"
ACCEPT_BUTTON_STYLE = """
<style>
div[data-testid="stButton"].accept-container > button {
    background-color: #28a745 !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #218838 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: 0.3s !important;
}
div[data-testid="stButton"].accept-container > button:hover {
    background-color: #218838 !important;
    transform: scale(1.05) !important;
}
</style>
"""

# ❌ Estilo para Botão "Recusar"
REJECT_BUTTON_STYLE = """
<style>
div[data-testid="stButton"].reject-container > button {
    background-color: #dc3545 !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #c82333 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: 0.3s !important;
}
div[data-testid="stButton"].reject-container > button:hover {
    background-color: #c82333 !important;
    transform: scale(1.05) !important;
}
</style>
"""

# 🟣 Estilo para Botões Globais (Login, Cadastro, Logout)
PURPLE_BUTTON_STYLE = """
<style>
div[data-testid="stButton"].purple-button > button {
    background-color: #7159c1 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #836fff !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    text-align: center !important;
    cursor: pointer !important;
    transition: 0.3s ease-in-out !important;
}
div[data-testid="stButton"].purple-button > button:hover {
    background-color: #5e47b0 !important;
    transform: scale(1.05) !important;
}
</style>
"""
