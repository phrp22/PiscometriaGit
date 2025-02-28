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

GLOBAL_FONT_STYLE = """
<style>
/* Importe a fonte do Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

/* Aplica a fonte em todos os elementos da página */
html, body, [class*="css"]  {
    font-family: 'Open Sans', sans-serif;
}
</style>
"""

PAGE_BG_STYLE = """
<style>
    /* Fundo da página no estilo azul marinho */
    .stApp {
        background-color: #1B2B48 !important; /* Ajuste esse tom se quiser mais claro ou mais escuro */
        color: #FFFFFF !important;
    }
    /* Ajusta a cor de textos padrões (labels, parágrafos, etc.) */
    h2, h3, h4, h5, h6, p, label, div, span, .css-1cpxqw2, .css-14xtw13 {
        color: #FFFFFF !important;
    }
    /* Destaque laranja para a frase */
    .orange-text {
        color: #FFA500 !important; /* Laranja */
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
"""


