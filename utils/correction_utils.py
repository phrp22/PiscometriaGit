import streamlit as st
import json
from auth import supabase_client
from utils.user_utils import get_user_info
from correction_config import correction_config  # Nosso módulo de configuração com funções e dados normativos


def get_completed_scales(patient_id):
    """
    Retorna as escalas que foram concluídas (completed=True) pelo paciente especificado.

    Fluxo:
        1. Busca o 'link_id' do paciente na tabela 'professional_patient_link' (onde status='accepted').
        2. Faz um join com a tabela 'scales' ao consultar 'scale_progress', para trazer 'scale_name'.
           - Para isso, é preciso ter a FK (scale_id) em 'scale_progress' referenciando 'scales(id)'.
        3. Retorna os registros em que 'link_id' corresponde ao do paciente e 'completed' é True.
        4. Cada registro retorna, além dos campos de 'scale_progress', o campo 'scale_name' (via join).

    Args:
        patient_id (str): ID do paciente (usuário autenticado).

    Returns:
        tuple: (list, str or None)
            - (completed_scales, None) se a consulta foi bem-sucedida.
            - ([], 'mensagem_de_erro') se houver algum erro ou se não encontrar o vínculo.

    Observações:
        - Garanta que exista uma FOREIGN KEY em 'scale_progress(scale_id)' que referencie 'scales(id)'.
        - Garanta que o nome da tabela de escalas seja 'scales' e a coluna seja 'scale_name'.
        - Se a coluna tiver outro nome, ou a tabela tiver outro nome, adapte 'scales!inner(scale_name)'.
        - 'scales!inner' indica que estamos fazendo um join interno (inner join) via PostgREST.

    Exemplo de uso:
        completed_scales, err = get_completed_scales(user_id)
        if err:
            st.error(err)
        else:
            # processar completed_scales
    """
    try:
        # 1. Obtém o link_id do paciente
        link_resp = supabase_client.from_("professional_patient_link") \
            .select("id") \
            .eq("patient_id", patient_id) \
            .eq("status", "accepted") \
            .execute()
        if not link_resp.data:
            return [], "Nenhum vínculo ativo encontrado para este paciente."
        
        link_id_do_paciente = link_resp.data[0]["id"]

        # 2. Consulta 'scale_progress' com join na tabela 'scales'
        #    * Atenção: 'scales!inner(scale_name)' supõe que a tabela se chama 'scales'
        #      e a FK é 'scale_id' em 'scale_progress'.
        #    * Se o campo em 'scales' tiver outro nome, mude 'scale_name' para esse nome.
        response = supabase_client.from_("scale_progress") \
            .select("id, link_id, completed, answers, date, scales!inner(scale_name)") \
            .eq("link_id", link_id_do_paciente) \
            .eq("completed", True) \
            .order("date", desc=True) \
            .execute()

        if hasattr(response, "error") and response.error:
            return [], f"Erro ao buscar escalas completadas: {response.error.message}"
        
        if not response.data:
            return [], "Nenhuma escala concluída encontrada."
        
        # 3. Retorna os registros encontrados
        return response.data, None

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