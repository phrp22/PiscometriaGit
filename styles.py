BUTTON_STYLE = """
<style>
    /* Aplica estilo para TODOS os botões, incluindo os da sidebar */
    div.stButton > button:first-child,
    section[data-testid="stSidebar"] div.stButton > button:first-child {
        background-color: #7159c1 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: 2px solid #836fff !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: 0.3s ease-in-out !important;
        width: 100% !important;
        padding: 12px 24px !important;
        text-align: center !important;
        box-shadow: 0px 0px 10px rgba(113, 89, 193, 0.5) !important;
        outline: none !important;
    }

    /* Remove borda vermelha após clique */
    div.stButton > button:first-child:focus,
    section[data-testid="stSidebar"] div.stButton > button:first-child:focus {
        outline: none !important;
        border-color: #836fff !important;
        box-shadow: 0px 0px 15px rgba(113, 89, 193, 0.5) !important;
    }

    /* Efeito hover */
    div.stButton > button:first-child:hover,
    section[data-testid="stSidebar"] div.stButton > button:first-child:hover {
        background-color: #5e47b0 !important;
        transform: scale(1.05) !important;
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7) !important;
    }

    /* Efeito ao clicar */
    div.stButton > button:first-child:active,
    section[data-testid="stSidebar"] div.stButton > button:first-child:active {
        background-color: #5e47b0 !important;
        border-color: #7159c1 !important;
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7) !important;
        transform: scale(0.98) !important;
        color: white !important;
    }

    /* Remove qualquer contorno vermelho do tema */
    div.stButton > button:first-child:focus-visible {
        outline: none !important;
        border: 2px solid #836fff !important;
        box-shadow: 0px 0px 15px rgba(113, 89, 193, 0.5) !important;
    }

</style>
"""