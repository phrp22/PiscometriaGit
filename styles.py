BUTTON_STYLE = """
<style>
    /* Estilização geral para todos os botões */
    div.stButton > button:first-child,
    section[data-testid="stSidebar"] div.stButton > button:first-child {
        background-color: #7159c1;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border: 2px solid #836fff;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s ease-in-out;
        width: 100%;
        padding: 12px 24px;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(113, 89, 193, 0.5);
        outline: none !important; /* Remove contorno de foco */
    }

    /* Efeito hover */
    div.stButton > button:first-child:hover,
    section[data-testid="stSidebar"] div.stButton > button:first-child:hover {
        background-color: #5e47b0;
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7);
    }

    /* Efeito ao clicar (ativo) */
    div.stButton > button:first-child:active,
    section[data-testid="stSidebar"] div.stButton > button:first-child:active {
        background-color: #5e47b0 !important;
        border-color: #7159c1 !important;
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7);
        transform: scale(0.98);
        color: white !important; /* Garante que o texto não fique vermelho */
    }

    /* Remove borda vermelha de foco após o clique */
    div.stButton > button:first-child:focus,
    section[data-testid="stSidebar"] div.stButton > button:first-child:focus {
        outline: none !important;
        box-shadow: 0px 0px 15px rgba(113, 89, 193, 0.5) !important;
    }
</style>
"""


SIDEBAR_BUTTON_STYLE = """
<style>
    /* Estiliza os botões da sidebar */
    section[data-testid="stSidebar"] div.stButton > button:first-child {
        background-color: #7159c1;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border: 2px solid #836fff;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s ease-in-out;
        width: 100%;
        padding: 10px 20px;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(113, 89, 193, 0.5);
    }
    section[data-testid="stSidebar"] div.stButton > button:first-child:hover {
        background-color: #5e47b0;
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7);
    }
    section[data-testid="stSidebar"] div.stButton > button:first-child:active {
        background-color: #d32f2f !important;
        border-color: #a82828 !important;
        box-shadow: 0px 0px 10px rgba(211, 47, 47, 0.8);
        transform: scale(0.98);
    }
</style>
"""