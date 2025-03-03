BUTTON_STYLE = """
<style>
/* --- RESET STREAMLIT PADRÃO --- */
button {
    all: unset !important;
}

/* --- BOTÕES PADRÃO (ROXO) --- */
button:not([data-testid="stBaseButton-secondary"]) {
    background-color: #7159c1 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #836fff !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    padding: 12px 24px !important;
    text-align: center !important;
    box-shadow: 0px 5px 10px rgba(113, 89, 193, 0.5) !important;
    transition: transform 0.2s, background-color 0.3s, box-shadow 0.2s !important;
}

/* Hover dos botões roxos */
button:not([data-testid="stBaseButton-secondary"]):hover {
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(113, 89, 193, 0.7) !important;
}

/* Pressão dos botões roxos */
button:not([data-testid="stBaseButton-secondary"]):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(113, 89, 193, 0.5) !important;
}

/* --- BOTÃO "ACEITAR" (VERDE) --- */
button[data-testid="stBaseButton-secondary"]:has(p:contains("✅ Aceitar")) {
    background-color: #28a745 !important;
    color: white !important;
    border: 2px solid #218838 !important;
    box-shadow: 0px 5px 10px rgba(40, 167, 69, 0.5) !important;
    transition: all 0.3s ease-in-out !important;
}

/* Hover do botão "Aceitar" */
button[data-testid="stBaseButton-secondary"]:has(p:contains("✅ Aceitar")):hover {
    background-color: #218838 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(40, 167, 69, 0.7) !important;
}

/* Pressão do botão "Aceitar" */
button[data-testid="stBaseButton-secondary"]:has(p:contains("✅ Aceitar")):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(40, 167, 69, 0.5) !important;
}

/* --- BOTÃO "RECUSAR" (VERMELHO) --- */
button[data-testid="stBaseButton-secondary"]:has(p:contains("❌ Recusar")) {
    background-color: #dc3545 !important;
    color: white !important;
    border: 2px solid #c82333 !important;
    box-shadow: 0px 5px 10px rgba(220, 53, 69, 0.5) !important;
    transition: all 0.3s ease-in-out !important;
}

/* Hover do botão "Recusar" */
button[data-testid="stBaseButton-secondary"]:has(p:contains("❌ Recusar")):hover {
    background-color: #c82333 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(220, 53, 69, 0.7) !important;
}

/* Pressão do botão "Recusar" */
button[data-testid="stBaseButton-secondary"]:has(p:contains("❌ Recusar")):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(220, 53, 69, 0.5) !important;
}
</style>

"""