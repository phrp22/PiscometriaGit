import streamlit as st
from datetime import date
from auth import supabase_client
from utils.user_utils import get_user_info
from utils.goals_utils import get_linked_patients

def get_available_scales():
    """
    Obtém a lista de escalas psicométricas disponíveis no sistema.

    Fluxo:
        1. Consulta a tabela 'available_scales' para recuperar todas as escalas cadastradas.
        2. Retorna a lista de escalas como dicionários com campos como id, scale_name e description.

    Args:
        None.

    Returns:
        tuple: (lista de escalas, mensagem de erro ou None)

    Calls:
        Supabase → Tabela 'available_scales'
    """
    try:
        response = supabase_client.from_("available_scales").select("*").execute()
        if hasattr(response, "error") and response.error:
            return [], f"Erro ao buscar escalas disponíveis: {response.error.message}"
        return response.data, None
    except Exception as e:
        return [], f"Erro inesperado: {str(e)}"


def assign_scale_to_patient(professional_id, patient_id, scale_id):
    """
    Atribui uma escala psicométrica a um paciente.

    Fluxo:
        1. Verifica o vínculo entre o profissional e o paciente na tabela 'professional_patient_link'.
        2. Busca a escala disponível na tabela 'available_scales' para obter o scale_name.
        3. Insere um registro na tabela 'scales' associando o scale_id, scale_name e o link_id do vínculo.

    Args:
        professional_id (str): ID do profissional.
        patient_id (str): ID do paciente.
        scale_id (str): ID da escala (disponível na tabela available_scales).

    Returns:
        tuple: (bool, mensagem) – True se bem-sucedido; caso contrário, False e mensagem de erro.
    """
    try:
        st.write("DEBUG: assign_scale_to_patient chamado com:")
        st.write(" - professional_id:", professional_id)
        st.write(" - patient_id:", patient_id)
        st.write(" - scale_id:", scale_id)

        # 1. Verifica o vínculo entre profissional e paciente
        link_response = supabase_client.from_("professional_patient_link") \
            .select("id") \
            .eq("professional_id", professional_id) \
            .eq("patient_id", patient_id) \
            .eq("status", "accepted") \
            .execute()

        st.write("DEBUG: link_response data:", link_response.data)
        
        if not link_response.data:
            return False, "Nenhum vínculo ativo encontrado com este paciente."
        link_id = link_response.data[0]["id"]

        # 2. Busca o scale_name da tabela available_scales
        scale_response = supabase_client.from_("available_scales") \
            .select("scale_name") \
            .eq("id", scale_id) \
            .execute()

        st.write("DEBUG: scale_response data:", scale_response.data)

        if not scale_response.data:
            return False, "Escala não encontrada no catálogo."
        scale_name = scale_response.data[0]["scale_name"]

        st.write("DEBUG: scale_name obtido:", scale_name)

        # 3. Insere o registro na tabela 'scales'
        data = {
            "link_id": link_id,
            "scale_id": scale_id,
            "scale_name": scale_name
        }

        st.write("DEBUG: Dados que serão inseridos em 'scales':", data)

        insert_response = supabase_client.from_("scales").insert(data).execute()

        st.write("DEBUG: insert_response data:", insert_response.data)
        if hasattr(insert_response, "error") and insert_response.error:
            return False, f"Erro ao atribuir a escala: {insert_response.error.message}"
        
        return True, "Escala atribuída com sucesso!"

    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def get_assigned_scales(patient_id):
    """
    Obtém as escalas psicométricas atribuídas a um paciente.

    Fluxo:
        1. Busca o vínculo ativo do paciente na tabela 'professional_patient_link' (status='accepted').
        2. Extrai o 'link_id' desse vínculo.
        3. Consulta a tabela 'scales' para recuperar os registros associados ao 'link_id' do paciente,
           incluindo 'id, scale_id, link_id, scale_name, created_at'.
        4. Ordena os resultados por 'created_at' em ordem decrescente.

    Args:
        patient_id (str): ID do paciente (usado para encontrar o vínculo ativo).

    Returns:
        tuple: (list, str or None)
            - (scales_data, None) se a consulta for bem-sucedida e existirem escalas atribuídas.
            - ([], "Nenhuma escala atribuída encontrada.") se não houver registros.
            - ([], <mensagem_de_erro>) se ocorrer algum erro ou o vínculo não for encontrado.

    Calls:
        Supabase → Tabela 'professional_patient_link' (para obter o 'link_id')
        Supabase → Tabela 'scales' (para buscar escalas atribuídas ao paciente)
    """
    try:
        link_response = supabase_client.from_("professional_patient_link") \
            .select("id") \
            .eq("patient_id", patient_id) \
            .eq("status", "accepted") \
            .execute()

        if not link_response.data:
            return [], "Nenhum vínculo ativo encontrado."
        link_id = link_response.data[0]["id"]

        # Incluímos 'scale_name' para evitar erro de chave inexistente ao acessar scale["scale_name"]
        scales_response = supabase_client.from_("scales") \
            .select("id, scale_id, link_id, scale_name, created_at") \
            .eq("link_id", link_id) \
            .order("created_at", desc=True) \
            .execute()

        if hasattr(scales_response, "error") and scales_response.error:
            return [], f"Erro ao buscar escalas atribuídas: {scales_response.error.message}"

        if not scales_response.data:
            return [], "Nenhuma escala atribuída encontrada."

        return scales_response.data, None

    except Exception as e:
        return [], f"Erro inesperado: {str(e)}"



def initialize_scale_progress(scale_id, link_id):
    """
    Inicializa o registro de progresso para uma escala psicométrica, criando um registro na tabela 'scale_progress'
    se ainda não existir para a data atual.

    Fluxo:
        1. Verifica se já existe um registro para a escala e a data atual.
        2. Se não existir, insere um novo registro com o campo 'answers' iniciado como um dicionário vazio.
    
    Args:
        scale_id (str): ID da escala atribuída.
        link_id (str): ID do vínculo paciente-profissional.

    Returns:
        tuple: (bool, scale_progress_id ou mensagem de erro).

    Calls:
        Supabase → Tabela 'scale_progress'
    """
    today = date.today().isoformat()
    try:
        response = supabase_client.from_("scale_progress") \
            .select("id") \
            .eq("scale_id", scale_id) \
            .eq("date", today) \
            .execute()
        if response.data:
            return True, response.data[0]["id"]
        insert_response = supabase_client.from_("scale_progress").insert({
            "scale_id": scale_id,
            "link_id": link_id,
            "date": today,
            "completed": False,
            "answers": {}  # Inicia com um dicionário vazio para as respostas
        }).execute()
        if hasattr(insert_response, "error") and insert_response.error:
            return False, f"Erro ao inicializar registro de escala: {insert_response.error.message}"
        return True, insert_response.data[0]["id"]
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def update_scale_answers(scale_progress_id, answers):
    """
    Atualiza as respostas de uma escala psicométrica no registro de progresso e marca a escala como concluída.

    Fluxo:
        1. Recebe as respostas em formato de dicionário.
        2. Atualiza os campos 'answers' e 'completed' (definindo como True) na tabela 'scale_progress'
           para o registro indicado.
    
    Args:
        scale_progress_id (str): ID do registro na tabela 'scale_progress'.
        answers (dict): Dicionário com as respostas da escala.
    
    Returns:
        tuple: (bool, mensagem) - True se a operação for bem-sucedida, ou False e mensagem de erro.
    
    Calls:
        Supabase → Tabela 'scale_progress'
    """
    try:
        data = {
            "answers": answers,
            "completed": True
        }
        response = supabase_client.from_("scale_progress").update(data).eq("id", scale_progress_id).execute()
        if hasattr(response, "error") and response.error:
            return False, f"Erro ao atualizar respostas: {response.error.message}"
        return True, "Respostas salvas com sucesso!"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"



import streamlit as st
from datetime import date
import json
from auth import supabase_client
from utils.date_utils import format_date
from utils.scales_utils import get_assigned_scales, initialize_scale_progress, update_scale_answers

def render_patient_scales(user_id):
    """
    Renderiza as escalas psicométricas atribuídas ao paciente e permite que ele responda aos itens da escala.
    Apenas escalas ainda não respondidas (não concluídas) serão exibidas. Se houver mais de uma escala pendente,
    exibe somente a primeira, de modo que, após o envio, a próxima apareça.

    Fluxo:
        1. Obtém as escalas atribuídas ao paciente via get_assigned_scales().
        2. Filtra os registros para manter somente as escalas cujo registro de progresso para a data atual não esteja concluído.
        3. Se não houver escalas pendentes, exibe uma mensagem informando que todas foram respondidas.
        4. Caso haja uma escala pendente, busca sua definição no catálogo (available_scales) para obter os itens (perguntas e opções).
        5. Inicializa (ou recupera) o registro de progresso para a data atual usando initialize_scale_progress().
        6. Exibe um formulário dinâmico para responder à escala:
           - Para cada item, utiliza um widget (st.radio) com um placeholder "Selecione..." seguido das opções (como as strings definidas).
        7. Ao submeter, valida se todas as perguntas foram respondidas (nenhum valor permanece "Selecione...").
        8. Se validado, salva as respostas via update_scale_answers() e a escala passa a ser considerada concluída, não sendo mais exibida.

    Args:
        user_id (str): ID do paciente autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        scales_utils.py → get_assigned_scales()
        scales_utils.py → initialize_scale_progress()
        scales_utils.py → update_scale_answers()
        Supabase → Tabela 'available_scales' (para buscar os itens da escala)
        date_utils.py → format_date()
    """
    st.header("📝 Minhas Escalas")

    # 1. Buscar as escalas atribuídas ao paciente
    assigned_scales, err = get_assigned_scales(user_id)
    if err:
        st.error(err)
        return
    if not assigned_scales:
        st.info("Nenhuma escala atribuída no momento.")
        return

    # 2. Filtra escalas que ainda não foram respondidas hoje
    pending_scales = []
    for scale in assigned_scales:
        # Verifica o registro de progresso para a escala
        progress_resp = supabase_client.from_("scale_progress") \
            .select("completed") \
            .eq("id", scale["id"]) \
            .execute()
        if progress_resp.data and progress_resp.data[0].get("completed") is True:
            continue  # Escala já respondida, não adiciona à lista
        else:
            pending_scales.append(scale)
    
    if not pending_scales:
        st.info("Você já respondeu todas as escalas.")
        return

    # 3. Seleciona a primeira escala pendente para exibição
    scale = pending_scales[0]
    st.markdown(f"## {scale['scale_name']}")

    # 4. Buscar a definição da escala no catálogo available_scales (para obter os itens)
    scale_id_catalogo = scale["scale_id"]  # Esse é o ID da escala no catálogo
    scale_info = supabase_client.from_("available_scales") \
        .select("items") \
        .eq("id", scale_id_catalogo) \
        .execute()
    if not scale_info.data:
        st.warning("Não foi possível encontrar os itens para essa escala.")
        return

    # Converte o campo 'items' para dicionário, se necessário
    escala_json = scale_info.data[0]["items"]
    if isinstance(escala_json, str):
        escala_json = json.loads(escala_json)
    lista_perguntas = escala_json.get("items", [])

    # 5. Inicializa o registro de progresso para hoje (se não existir)
    init_success, scale_progress_id_or_msg = initialize_scale_progress(scale["id"], scale.get("link_id"))
    if not init_success:
        st.error(scale_progress_id_or_msg)
        return
    scale_progress_id = scale_progress_id_or_msg

    # 6. Exibe o formulário para responder a escala
    with st.form(key=f"form_scale_{scale['id']}"):
        st.write("Responda a escala abaixo:")
        answers_dict = {}
        # Para cada pergunta, cria um widget radio com placeholder "Selecione..."
        for item_obj in lista_perguntas:
            question_id = item_obj["id"]
            question_text = item_obj["question"]
            options = ["Selecione..."] + item_obj.get("options", [])
            user_response = st.radio(
                label=f"{question_id}. {question_text}",
                options=options,
                key=f"{scale['id']}_{question_id}",
                index=0  # Garante que o placeholder seja o valor padrão
            )
            answers_dict[f"question_{question_id}"] = user_response

        submitted = st.form_submit_button("Salvar Respostas")
        # 7. Validação: Verifica se alguma resposta continua com o valor "Selecione..."
        incomplete = any(answer == "Selecione..." for answer in answers_dict.values())
        if submitted:
            if incomplete:
                st.error("Por favor, responda a todas as perguntas antes de enviar.")
            else:
                success, msg = update_scale_answers(scale_progress_id, answers_dict)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)




def render_add_scale_section(user):
    """
    Renderiza a seção de atribuição de escalas psicométricas para um paciente.

    Fluxo:
        1. Obtém a lista de escalas disponíveis via get_available_scales().
        2. Obtém os pacientes vinculados ao profissional via get_linked_patients().
        3. Permite que o profissional selecione uma escala e um paciente.
        4. Ao confirmar, chama assign_scale_to_patient() para atribuir a escala.

    Args:
        user (dict): Dados do profissional autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        scales_utils.py → get_available_scales()
        scales_utils.py → get_linked_patients()
        scales_utils.py → assign_scale_to_patient()
    """
    st.markdown("### 📊 Atribuir Escala para Paciente")

    # Obtém escalas disponíveis
    available_scales, err = get_available_scales()
    if err:
        st.error(err)
        return
    if not available_scales:
        st.info("Nenhuma escala disponível no momento.")
        return

    # Seleciona a escala
    scale_options = {f"{scale['scale_name']} - {scale.get('description', '')}": scale["id"] for scale in available_scales}
    selected_scale = st.selectbox("Selecione a escala:", list(scale_options.keys()), key="select_scale")
    scale_id = scale_options[selected_scale]

    # Obtém pacientes vinculados ao profissional
    patients, err = get_linked_patients(user["id"])
    if err:
        st.error(err)
        return
    if not patients:
        st.warning("Nenhum paciente vinculado encontrado.")
        return

    patient_options = {p["name"]: p["id"] for p in patients}
    selected_patient = st.selectbox("Selecione o paciente:", list(patient_options.keys()), key="select_patient_for_scale")
    patient_id = patient_options[selected_patient]

    if st.button("Atribuir Escala", key="assign_scale", use_container_width=True):
        success, msg = assign_scale_to_patient(user["id"], patient_id, scale_id)
        if success:
            st.success(msg)
        else:
            st.error(msg)
