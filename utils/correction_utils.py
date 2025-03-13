import streamlit as st
import json
from auth import supabase_client
from utils.user_utils import get_user_info
from correction_config import correction_config  # Nosso módulo de configuração com funções e dados normativos


def get_completed_scales(patient_id):
    """
    Consulta a tabela scale_progress para obter os registros de escalas concluídas (completed = True)
    para o paciente, utilizando o link_id do vínculo.

    Fluxo:
        1. Consulta a tabela professional_patient_link para obter o link_id do paciente (status='accepted').
        2. Consulta a tabela scale_progress para buscar registros com esse link_id e completed=True.
    
    Args:
        patient_id (str): ID do paciente.

    Returns:
        tuple: (lista de registros de escala completados, mensagem de erro ou None)
    
    Calls:
        Supabase → Tabela 'professional_patient_link'
        Supabase → Tabela 'scale_progress'
    """
    try:
        # Obtém o vínculo ativo
        link_resp = supabase_client.from_("professional_patient_link") \
            .select("id") \
            .eq("patient_id", patient_id) \
            .eq("status", "accepted") \
            .execute()
        if not link_resp.data:
            return [], "Nenhum vínculo ativo encontrado."
        link_id = link_resp.data[0]["id"]
        
        # Busca registros em scale_progress com completed = True para esse link_id
        progress_resp = supabase_client.from_("scale_progress") \
            .select("id, scale_id, link_id, answers, completed, date") \
            .eq("link_id", link_id) \
            .eq("completed", True) \
            .order("date", desc=True) \
            .execute()
        if hasattr(progress_resp, "error") and progress_resp.error:
            return [], f"Erro ao buscar escalas completadas: {progress_resp.error.message}"
        return progress_resp.data, None
    except Exception as e:
        return [], f"Erro inesperado: {str(e)}"

def render_scale_correction_section(user_id):
    """
    Renderiza a seção de correção de escalas para o paciente, permitindo que ele selecione de uma lista
    qual escala (já respondida) deseja ver a correção automatizada.

    Fluxo:
        1. Obtém os registros de progresso (escala respondida e concluída) para o paciente usando get_completed_scales().
        2. Se não houver registros, exibe uma mensagem informando que não há escalas para corrigir.
        3. Caso haja, exibe um selectbox para que o paciente escolha a escala que deseja corrigir.
        4. Com base na escolha, identifica o tipo de escala (por exemplo, "BIS-11") e, se houver uma configuração
           em correction_config, chama a função de correção associada passando as respostas armazenadas e os dados normativos.\n
        5. Exibe o relatório de correção.
    
    Args:
        user_id (str): ID do paciente autenticado.
    
    Returns:
        None (apenas renderiza a interface).
    
    Calls:
        get_completed_scales()
        correction_config (módulo de configuração com dados e funções de correção)
    """
    st.header("📊 Correção de Escalas")
    
    # 1. Obter escalas completadas para o paciente
    completed_scales, err = get_completed_scales(user_id)
    if err:
        st.error(err)
        return
    if not completed_scales:
        st.info("Nenhuma escala respondida encontrada para correção.")
        return

    # 2. Cria uma lista de opções para o selectbox.
    # Aqui vamos exibir o scale_id e a data de resposta (ou se preferir, exiba scale_name se ele estiver disponível em scale_progress).
    options = {}
    for record in completed_scales:
        # Tentamos obter scale_name; se não houver, usamos o scale_id
        scale_label = record.get("scale_name", record["scale_id"]) if record.get("scale_name") else record["scale_id"]
        # Acrescenta a data para ajudar o paciente a identificar
        scale_label += f" - {record.get('date', '')}"
        options[scale_label] = record

    selected_option = st.selectbox("Selecione a escala para correção:", list(options.keys()))
    selected_record = options[selected_option]

    # 3. Identifica qual escala foi respondida e qual função de correção usar.
    # Aqui, assumimos que o campo scale_name (ou outro identificador) pode ser usado para mapear em correction_config.
    # Por exemplo, se scale_name for "Escala de Impulsividade de Barrat" e esse for o nome chave em correction_config:
    scale_type = selected_record.get("scale_name", None)
    if not scale_type:
        st.error("Não foi possível identificar o tipo da escala para correção.")
        return

    if scale_type not in correction_config:
        st.info("Correção automatizada não disponível para essa escala.")
        return

    # 4. Obtém as respostas armazenadas e chama a função de correção
    answers = selected_record.get("answers", {})
    config = correction_config[scale_type]
    correction_function = config.get("correction_function")
    normative_table = config.get("normative_table")
    percentile_indices = config.get("percentile_indices")
    
    if not correction_function:
        st.error("Função de correção não definida para essa escala.")
        return

    # Chama a função de correção e exibe o relatório
    report = correction_function(answers, normative_table, percentile_indices)
    st.subheader("Relatório de Correção")
    st.json(report)