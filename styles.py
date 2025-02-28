# styles.py

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
    div.stButton > button:first-child:hover {
        background-color: #5e47b0;
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7);
    }
    div.stButton > button:first-child:active {
        background-color: #d32f2f !important;
        border-color: #a82828 !important;
        box-shadow: 0px 0px 10px rgba(211, 47, 47, 0.8);
        transform: scale(0.98);
    }
</style>
"""

TITLE_STYLE = """
<style>
    h1 {
        font-size: 42px;
        font-weight: bold;
        text-align: left; 
        color: #ffffff !important; /* Caso queira o título em branco */
    }
</style>
"""

ORANGE_TEXT_STYLE = """
<style>
    /* Aumenta o tamanho da frase em laranja */
    .orange-text {
        color: #FFA500 !important;
        font-weight: bold;
        font-size: 2rem; /* Aumente conforme desejar */
    }
</style>
"""

# Se você tinha algo como PAGE_BG_STYLE definindo o fundo, remova-o ou comente-o.


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
