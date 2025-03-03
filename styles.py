BUTTON_STYLE = """
<style>

/* --- BOTÕES PADRÃO (ROXO) --- */
:where(div.stButton) > button:not([aria-label="✅ Aceitar"]):not([aria-label="❌ Recusar"]) {
    all: unset !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    padding: 14px 28px !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    text-align: center !important;
    transition: transform 0.2s ease-in-out, background-color 0.3s ease-in-out, box-shadow 0.2s ease-in-out !important;
    background-color: #7159c1 !important;
    color: white !important;
    border: 2px solid #836fff !important;
    animation: pulse 2s infinite !important;
}

/* Hover dos botões roxos */
:where(div.stButton) > button:not([aria-label="✅ Aceitar"]):not([aria-label="❌ Recusar"]):hover {
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(113, 89, 193, 0.7) !important;
}

/* Pressão dos botões roxos */
:where(div.stButton) > button:not([aria-label="✅ Aceitar"]):not([aria-label="❌ Recusar"]):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(113, 89, 193, 0.5) !important;
}

/* --- BOTÃO "ACEITAR" (VERDE) --- */
:where(div.accept-container div.stButton) > button {
    background-color: #28a745 !important;
    color: white !important;
    border: 2px solid #218838 !important;
    box-shadow: 0px 5px 10px rgba(40, 167, 69, 0.5) !important;
    transition: all 0.3s ease-in-out !important;
}

/* Hover do botão "Aceitar" */
:where(div.accept-container div.stButton) > button:hover {
    background-color: #218838 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(40, 167, 69, 0.7) !important;
}

/* Pressão do botão "Aceitar" */
:where(div.accept-container div.stButton) > button:active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(40, 167, 69, 0.5) !important;
}

/* --- BOTÃO "RECUSAR" (VERMELHO) --- */
:where(div.reject-container div.stButton) > button {
    background-color: #dc3545 !important;
    color: white !important;
    border: 2px solid #c82333 !important;
    box-shadow: 0px 5px 10px rgba(220, 53, 69, 0.5) !important;
    transition: all 0.3s ease-in-out !important;
}

/* Hover do botão "Recusar" */
:where(div.reject-container div.stButton) > button:hover {
    background-color: #c82333 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(220, 53, 69, 0.7) !important;
}

/* Pressão do botão "Recusar" */
:where(div.reject-container div.stButton) > button:active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(220, 53, 69, 0.5) !important;
}
</style>
"""