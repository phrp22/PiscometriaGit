BUTTON_STYLE = """
<style>
/* Garante que os botões padrão fiquem roxos */
div.stButton > button:not([aria-label="✅ Aceitar"]):not([aria-label="❌ Recusar"]) {
    background-color: #7159c1 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #836fff !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out, box-shadow 0.2s ease-in-out !important;
    width: 100% !important;
    padding: 12px 24px !important;
    text-align: center !important;
    box-shadow: 0px 5px 10px rgba(113, 89, 193, 0.5) !important;
    outline: none !important;
}

/* Hover dos botões padrão */
div.stButton > button:not([aria-label="✅ Aceitar"]):not([aria-label="❌ Recusar"]):hover {
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(113, 89, 193, 0.7) !important;
}

/* Efeito ao pressionar os botões padrão */
div.stButton > button:not([aria-label="✅ Aceitar"]):not([aria-label="❌ Recusar"]):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(113, 89, 193, 0.5) !important;
}

/* Estiliza o botão "Aceitar" corretamente */
button[aria-label="✅ Aceitar"], button[data-testid="stBaseButton-secondary"] {
    background-color: #28a745 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #218838 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    text-align: center !important;
    cursor: pointer !important;
    transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out, box-shadow 0.2s ease-in-out !important;
    box-shadow: 0px 5px 10px rgba(40, 167, 69, 0.5) !important;
    outline: none !important;
}

/* Hover do botão "Aceitar" */
button[aria-label="✅ Aceitar"]:hover, button[data-testid="stBaseButton-secondary"]:hover {
    background-color: #218838 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(40, 167, 69, 0.7) !important;
}

/* Pressão do botão "Aceitar" */
button[aria-label="✅ Aceitar"]:active, button[data-testid="stBaseButton-secondary"]:active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(40, 167, 69, 0.5) !important;
}

/* Efeito de clique finalizado para "Aceitar" */
button[aria-label="✅ Aceitar"].pressed {
    background-color: #1e7e34 !important;
    border-color: #155724 !important;
    box-shadow: 0px 0px 15px rgba(40, 167, 69, 0.9) !important;
}

/* Estiliza o botão "Recusar" corretamente */
button[aria-label="❌ Recusar"] {
    background-color: #dc3545 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #c82333 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    text-align: center !important;
    cursor: pointer !important;
    transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out, box-shadow 0.2s ease-in-out !important;
    box-shadow: 0px 5px 10px rgba(220, 53, 69, 0.5) !important;
    outline: none !important;
}

/* Hover do botão "Recusar" */
button[aria-label="❌ Recusar"]:hover {
    background-color: #c82333 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(220, 53, 69, 0.7) !important;
}

/* Pressão do botão "Recusar" */
button[aria-label="❌ Recusar"]:active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(220, 53, 69, 0.5) !important;
}

/* Efeito de clique finalizado para "Recusar" */
button[aria-label="❌ Recusar"].pressed {
    background-color: #a71d2a !important;
    border-color: #721c24 !important;
    box-shadow: 0px 0px 15px rgba(220, 53, 69, 0.9) !important;
}
</style>
"""