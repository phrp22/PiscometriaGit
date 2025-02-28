# gender_utils.py

def adjust_gender_ending(text: str, genero: str) -> str:
    genero = genero.strip()  # remove espaços
    SUBSTITUICOES = {
        "Masculino":   {"o": "o", "os": "os"},  # sem mudança
        "Feminino":    {"o": "a", "os": "as"},
        "Não-binário": {"o": "e", "os": "es"},
    }

    # Se o gênero não estiver no dicionário, retorna sem mexer
    if genero not in SUBSTITUICOES:
        return text

    if text.endswith("os"):
        return text[:-2] + SUBSTITUICOES[genero]["os"]
    elif text.endswith("o"):
        return text[:-1] + SUBSTITUICOES[genero]["o"]
    else:
        return text
