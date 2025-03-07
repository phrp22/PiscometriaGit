# gender_utils.py

def adjust_gender_ending(text: str, genero: str) -> str:
    """
    Ajusta o final de 'text' de acordo com o gênero informado.
    Espera que 'genero' seja:
      - "M" para Masculino (não altera o texto)
      - "F" para Feminino (troca "o" por "a" e "os" por "as")
      - "N" para Não-binário (troca "o" por "e" e "os" por "es")
    Se o texto não terminar em "o" ou "os", retorna o texto original.
    """
    genero = genero.strip().upper()  # garante que esteja em maiúsculas sem espaços

    SUBSTITUICOES = {
        "M": {"o": "o", "os": "os"},  # Mantém como está
        "F": {"o": "a", "os": "as"},
        "N": {"o": "e", "os": "es"}
    }

    if genero not in SUBSTITUICOES:
        return text

    if text.endswith("os"):
        return text[:-2] + SUBSTITUICOES[genero]["os"]
    elif text.endswith("o"):
        return text[:-1] + SUBSTITUICOES[genero]["o"]
    else:
        return text
