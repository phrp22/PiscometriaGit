# styles.py - Centraliza os estilos CSS

BUTTON_STYLE = """
<style>
    div.stButton > button:first-child {
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
    }

    /* Efeito Hover (passar o mouse) */
    div.stButton > button:first-child:hover {
        background-color: #5e47b0;
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7);
    }

    /* Efeito Active (quando pressionado) */
    div.stButton > button:first-child:active {
        background-color: #3cb371 !important;  /* Verde Encantado */
        border-color: #2e8b57 !important;  /* Verde mais escuro */
        box-shadow: 0px 0px 15px rgba(60, 179, 113, 0.7);
        transform: scale(0.98);
    }

    /* Estado Desativado (durante carregamento) */
    div.stButton > button:first-child:disabled, div.stButton > button:first-child[disabled] {
        background-color: #2e8b57 !important;  /* Verde escuro no carregamento */
        color: white !important;  /* Mantém o texto branco */
        border: 2px solid #3cb371 !important;
        box-shadow: 0px 0px 10px rgba(46, 139, 87, 0.5);
        opacity: 0.8;
    }
</style>
"""


TITLE_STYLE = """
<style>
    h1 {
        font-size: 38px;
        font-weight: bold;
        text-align: left;  /* Alinhado à esquerda */
        color: #5a69c9;  /* Tom roxo mais azulado e profissional */
        margin-bottom: 10px;  /* Pequeno espaçamento inferior */
    }
</style>
"""




