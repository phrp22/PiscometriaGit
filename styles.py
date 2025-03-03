BUTTON_STYLE = """

<style>
/* --- ANIMAÇÃO PULSANTE PARA BOTÕES --- */
@keyframes pulse {
    0% {
        box-shadow: 0 0 10px rgba(113, 89, 193, 0.5);
    }
    50% {
        box-shadow: 0 0 20px rgba(113, 89, 193, 0.8);
    }
    100% {
        box-shadow: 0 0 10px rgba(113, 89, 193, 0.5);
    }
}

/* --- ESTILIZAÇÃO GERAL PARA TODOS OS BOTÕES (ROXO) --- */
div.stButton > button {
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

/* Hover para todos os botões */
div.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0px 8px 15px rgba(113, 89, 193, 0.7) !important;
}

/* Pressão (efeito ao clicar) */
div.stButton > button:active {
    transform: scale(0.95) !important;
    box-shadow: 0px 2px 5px rgba(113, 89, 193, 0.5) !important;
}
</style>


"""