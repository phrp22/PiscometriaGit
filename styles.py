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
    div.stButton > button:first-child:hover {
        background-color: #5e47b0;
        transform: scale(1.05);
        box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7);
    }
</style>
"""

TITLE_STYLE = """
<style>
    h1 {
        font-size: 44px;
        font-weight: bold;
        text-align: left;
        background: linear-gradient(90deg, #e6e0f8, #9b88cc, #7159c1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 1px 1px 4px rgba(113, 89, 193, 0.4);
        animation: softGlow 6s infinite alternate ease-in-out;
    }

    @keyframes softGlow {
        0% {
            text-shadow: 1px 1px 4px rgba(113, 89, 193, 0.4);
        }
        100% {
            text-shadow: 2px 2px 6px rgba(113, 89, 193, 0.5);
        }
    }
</style>
"""



