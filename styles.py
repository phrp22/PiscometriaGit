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
        background-color: #d32f2f !important;  /* Vermelho uniforme */
        border-color: #a82828 !important;  /* Vermelho escuro para contraste */
        box-shadow: 0px 0px 10px rgba(211, 47, 47, 0.8);
        transform: scale(0.98);
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




