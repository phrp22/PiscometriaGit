def listar_escalas():
    """Retorna uma lista de escalas psicométricas disponíveis"""
    return ["Escala de Depressão", "Escala de Ansiedade", "Escala de Estresse"]

def obter_perguntas_escala(escala):
    """Retorna perguntas fictícias com opções de resposta"""
    escalas = {
        "Escala de Depressão": [
            "1. Nos últimos dias, você se sentiu triste ou sem esperança?",
            "2. Você perdeu o interesse por atividades que antes gostava?",
            "3. Você se sentiu cansado(a) ou sem energia frequentemente?",
            "4. Você teve dificuldades para dormir ou dormiu mais do que o normal?",
            "5. Você teve pensamentos de inutilidade ou culpa excessiva?"
        ],
        "Escala de Ansiedade": [
            "1. Você tem sentido nervosismo ou inquietação frequente?",
            "2. Você tem dificuldades para relaxar mesmo em momentos de lazer?",
            "3. Você sente preocupação excessiva com coisas pequenas?",
            "4. Você tem sentido seu coração acelerado sem motivo aparente?",
            "5. Você tem dificuldades para controlar seus pensamentos ansiosos?"
        ],
        "Escala de Estresse": [
            "1. Nos últimos dias, você se sentiu sobrecarregado(a)?",
            "2. Você sentiu que não conseguia lidar com seus problemas?",
            "3. Você teve dificuldades para se concentrar devido ao estresse?",
            "4. Você teve dores de cabeça, tensão muscular ou outros sintomas físicos devido ao estresse?",
            "5. Você se sentiu irritado(a) ou impaciente frequentemente?"
        ]
    }
    
    return escalas.get(escala, [])  # Retorna as perguntas da escala escolhida
