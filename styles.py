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
        font-size: 60px;
        font-weight: bold;
        text-align: left;
        background: linear-gradient(90deg, #ffffff, #b3a0ff, #7159c1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 10px rgba(255, 255, 255, 0.7);
        animation: glowTitle 4s infinite alternate ease-in-out;
    }

    @keyframes glowTitle {
        0% {
            text-shadow: 3px 3px 10px rgba(255, 255, 255, 0.7);
        }
        100% {
            text-shadow: 5px 5px 15px rgba(255, 255, 255, 0.9);
        }
    }
</style>
"""

