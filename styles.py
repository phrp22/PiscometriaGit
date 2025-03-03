BUTTON_STYLE = """
<style>
/* Estilo global para botões - NÃO AFETA botões dentro de .accept-container e .reject-container */
div.stButton > button:not(.accept-button):not(.reject-button) {
    background-color: #7159c1 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: 2px solid #836fff !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out !important;
    width: 100% !important;
    padding: 12px 24px !important;
    text-align: center !important;
    box-shadow: 0px 0px 10px rgba(113, 89, 193, 0.5) !important;
    outline: none !important;
}

/* Efeito de hover */
div.stButton > button:not(.accept-button):not(.reject-button):hover {
    transform: scale(1.05) !important;
}

/* Efeito ao clicar */
div.stButton > button:not(.accept-button):not(.reject-button):active {
    background-color: #5e47b0 !important;
    border-color: #7159c1 !important;
    box-shadow: 0px 0px 15px rgba(130, 94, 255, 0.7) !important;
    transform: scale(0.98) !important;
    color: white !important;
}
</style>
"""


ACCEPT_BUTTON_STYLE = """
<style>
div.stButton > button.accept-button {
    background-color: #28a745 !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #218838 !important;
    border-radius: 8px !important;
    transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out !important;
    padding: 10px 20px !important;
    width: 100% !important;
    text-align: center !important;
    cursor: pointer !important;
}

/* Efeito de hover */
div.stButton > button.accept-button:hover {
    background-color: #218838 !important;
    transform: scale(1.1) !important;
}
</style>
"""

REJECT_BUTTON_STYLE = """
<style>
div.stButton > button.reject-button {
    background-color: #dc3545 !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #c82333 !important;
    border-radius: 8px !important;
    transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out !important;
    padding: 10px 20px !important;
    width: 100% !important;
    text-align: center !important;
    cursor: pointer !important;
}

/* Efeito de hover */
div.stButton > button.reject-button:hover {
    background-color: #c82333 !important;
    transform: scale(1.1) !important;
}
</style>
"""
