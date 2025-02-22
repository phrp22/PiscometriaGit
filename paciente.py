import streamlit as st
import time
from database import listar_escalas_pendentes, salvar_respostas_escala, get_profissional_da_escala
from escalas import obter_perguntas_escala

def paciente_page():
    st.header("Área do Paciente")
    st.write(f"Bem-vindo, {st.session_state.username}!")

    # Obtém as escalas pendentes (ainda não respondidas)
    escalas_pendentes = listar_escalas_pendentes(st.session_state.username)

    if not escalas_pendentes:
        st.info("Você já respondeu todas as escalas enviadas. Aguarde seu profissional enviar novas escalas.")
        return  # ✅ Evita erro de variáveis indefinidas

    # O paciente seleciona a escala que deseja responder
    escala_selecionada = st.selectbox("Escolha uma escala para responder:", escalas_pendentes)

    if not escala_selecionada:
        return  # ✅ Evita erro caso a seleção esteja vazia

    # Obtém as perguntas da escala selecionada
    perguntas = obter_perguntas_escala(escala_selecionada)

    if not perguntas:
        st.error("Erro ao carregar perguntas da escala.")
        return

    st.subheader(f"Respondendo: {escala_selecionada}")

    # Criar dicionário para armazenar respostas
    respostas = {}

    # Exibir perguntas e capturar respostas
    for pergunta in perguntas:
        resposta = st.radio(pergunta, ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"])
        respostas[pergunta] = resposta

    if st.button("Enviar Respostas"):
        profissional_responsavel = get_profissional_da_escala(st.session_state.username, escala_selecionada)  # ✅ Busca o profissional responsável

        if profissional_responsavel:
            sucesso = salvar_respostas_escala(st.session_state.username, escala_selecionada, respostas)
            if sucesso:
                st.success("Respostas enviadas com sucesso!")
                time.sleep(3)  # ✅ Aguarda 2 segundos antes de recarregar
                st.rerun()  # ✅ Agora a interface só atualiza depois de mostrar a mensagem
            else:
                st.error("Erro ao enviar respostas. Tente novamente.")
        else:
            st.error("Erro: Profissional responsável não encontrado.")
