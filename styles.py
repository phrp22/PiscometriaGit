BUTTON_STYLE = """
<style>
/* Estilo global para botões (pode manter, mas evite usar :first-child se tiver vários botões) */
div.stButton > button {
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
</style>
"""

ACCEPT_BUTTON_STYLE = """
<style>
/* Força um seletor mais específico que o global */
.accept-container div.stButton > button {
    background-color: #28a745 !important; /* verde */
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #218838 !important;
    border-radius: 8px !important;
    transition: 0.3s !important;
    padding: 10px 20px !important;
    width: 100% !important;
    text-align: center !important;
    cursor: pointer !important;
}
.accept-container div.stButton > button:hover {
    background-color: #218838 !important;
    transform: scale(1.05) !important;
}
</style>
"""

REJECT_BUTTON_STYLE = """
<style>
/* Força um seletor mais específico que o global */
.reject-container div.stButton > button {
    background-color: #dc3545 !important; /* vermelho */
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: 2px solid #c82333 !important;
    border-radius: 8px !important;
    transition: 0.3s !important;
    padding: 10px 20px !important;
    width: 100% !important;
    text-align: center !important;
    cursor: pointer !important;
}
.reject-container div.stButton > button:hover {
    background-color: #c82333 !important;
    transform: scale(1.05) !important;
}
</style>
"""