import streamlit as st
import json
from auth import supabase_client
from .correction_config import correction_config
from utils.user_utils import get_user_info


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
        3. Caso haja registros, cria um selectbox para que o paciente escolha a escala a corrigir.
           - O rótulo de cada opção é composto pelo scale_name (obtido via join) e pela data, se disponível.
        4. Após a seleção, identifica a escala a ser corrigida e, com base no tipo (por exemplo, BIS‑11),
           busca na configuração (correction_config) a função de correção e os dados normativos apropriados.
        5. Chama a função de correção, passando as respostas armazenadas e os dados normativos, e exibe o relatório.

    Args:
        user_id (str): ID do paciente autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        Supabase (join entre 'scale_progress' e 'scales')
        correction_config (módulo de configuração com dados e funções de correção)
    """
    st.header("📊 Correção de Escalas")
    
    # 1. Obter os registros de escalas concluídas para o paciente (join entre scale_progress e scales)
    completed_scales, err = get_completed_scales(user_id)
    if err:
        st.error(err)
        return
    if not completed_scales:
        st.info("Nenhuma escala respondida encontrada para correção.")
        return

    # 2. Cria uma lista de opções para o selectbox com rótulos adequados
    options = {}
    for record in completed_scales:
        # Como 'scale_name' vem dentro do objeto 'scales', usamos:
        if record.get("scales") and record["scales"].get("scale_name"):
            scale_label = record["scales"]["scale_name"] + f" - {record.get('date', '')}"
        else:
            scale_label = f"Escala (ID: {record['id']})"
        options[scale_label] = record

    # Exibe um selectbox para o paciente escolher a escala a corrigir
    selected_option = st.selectbox("Selecione a escala para correção:", list(options.keys()))
    selected_record = options[selected_option]

    # 3. Identifica a escala (tipo) para correção
    # Aqui, assumimos que o 'scale_name' identifica o tipo de escala
    if selected_record.get("scales") and selected_record["scales"].get("scale_name"):
        scale_type = selected_record["scales"]["scale_name"]
    else:
        st.error("Não foi possível identificar o tipo da escala para correção.")
        return

    # Se você tem a configuração de correção para essa escala no correction_config:
    from utils.correction_config import correction_config  # Importa o dicionário de configuração
    if scale_type not in correction_config:
        st.info("Correção automatizada não disponível para essa escala.")
        return

    config = correction_config[scale_type]
    correction_function = config.get("correction_function")
    normative_table = config.get("normative_table")
    percentile_indices = config.get("percentile_indices")
    
    if not correction_function:
        st.error("Função de correção não definida para essa escala.")
        return

    # 4. Obtém as respostas armazenadas do registro (campo 'answers')
    answers = selected_record.get("answers", {})
    
    # 5. Chama a função de correção e exibe o relatório
    report = correction_function(answers, normative_table, percentile_indices)
    st.subheader("Relatório de Correção")
    st.json(report)
