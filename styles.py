BUTTON_STYLE = """
<style>
/* --- RESTRINGE O ALCANCE DOS ESTILOS APENAS AO CONTEÚDO PRINCIPAL --- */
section.main div.stButton > button {
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
}

/* --- BOTÕES PADRÃO (ROXO) --- */
section.main div.stButton > button:not([data-testid="stBaseButton-secondary"]) {
    background-color: #7159c1 !important;
    color: white !important;
    border: 2px solid #836fff !important;
    box-shadow: 0px 5px 10px rgba(113, 89, 193, 0.5) !important;
}

/* Hover dos botões roxos */
section.main div.stButton > button:not([data-testid="stBaseButton-secondary"]):hover {
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(113, 89, 193, 0.7) !important;
}

/* Pressão dos botões roxos */
section.main div.stButton > button:not([data-testid="stBaseButton-secondary"]):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(113, 89, 193, 0.5) !important;
}

/* --- BOTÃO "ACEITAR" (VERDE) --- */
section.main button[data-testid="stBaseButton-secondary"]:has(p:contains("✅ Aceitar")) {
    background-color: #28a745 !important;
    color: white !important;
    border: 2px solid #218838 !important;
    box-shadow: 0px 5px 10px rgba(40, 167, 69, 0.5) !important;
}

/* Hover do botão "Aceitar" */
section.main button[data-testid="stBaseButton-secondary"]:has(p:contains("✅ Aceitar")):hover {
    background-color: #218838 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(40, 167, 69, 0.7) !important;
}

/* Pressão do botão "Aceitar" */
section.main button[data-testid="stBaseButton-secondary"]:has(p:contains("✅ Aceitar")):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(40, 167, 69, 0.5) !important;
}

/* --- BOTÃO "RECUSAR" (VERMELHO) --- */
section.main button[data-testid="stBaseButton-secondary"]:has(p:contains("❌ Recusar")) {
    background-color: #dc3545 !important;
    color: white !important;
    border: 2px solid #c82333 !important;
    box-shadow: 0px 5px 10px rgba(220, 53, 69, 0.5) !important;
}

/* Hover do botão "Recusar" */
section.main button[data-testid="stBaseButton-secondary"]:has(p:contains("❌ Recusar")):hover {
    background-color: #c82333 !important;
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(220, 53, 69, 0.7) !important;
}

/* Pressão do botão "Recusar" */
section.main button[data-testid="stBaseButton-secondary"]:has(p:contains("❌ Recusar")):active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(220, 53, 69, 0.5) !important;
}
</style>


"""