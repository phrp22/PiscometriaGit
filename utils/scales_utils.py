import streamlit as st
from datetime import date
from auth import supabase_client
from utils.user_utils import get_user_info

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
        2. Insere um registro na tabela 'scales' associando o scale_id ao link_id do vínculo.
    
    Args:
        professional_id (str): ID do profissional.
        patient_id (str): ID do paciente.
        scale_id (str): ID da escala escolhida (da tabela available_scales).

    Returns:
        tuple: (bool, mensagem) - True se a operação for bem-sucedida; caso contrário, False e mensagem de erro.

    Calls:
        Supabase → Tabela 'professional_patient_link'
        Supabase → Tabela 'scales'
    """
    try:
        # Verifica o vínculo entre profissional e paciente
        link_response = supabase_client.from_("professional_patient_link") \
            .select("id") \
            .eq("professional_id", professional_id) \
            .eq("patient_id", patient_id) \
            .eq("status", "accepted") \
            .execute()
        if not link_response.data:
            return False, "Nenhum vínculo ativo encontrado com este paciente."
        link_id = link_response.data[0]["id"]

        # Insere o registro na tabela 'scales'
        data = {
            "link_id": link_id,
            "scale_id": scale_id  # Aqui 'scale_id' refere-se à escala escolhida
        }
        response = supabase_client.from_("scales").insert(data).execute()
        if hasattr(response, "error") and response.error:
            return False, f"Erro ao atribuir a escala: {response.error.message}"
        return True, "Escala atribuída com sucesso!"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def get_assigned_scales(patient_id):
    """
    Obtém as escalas psicométricas atribuídas a um paciente.

    Fluxo:
        1. Busca o vínculo ativo do paciente na tabela 'professional_patient_link'.
        2. Consulta a tabela 'scales' para recuperar as escalas associadas ao link_id.
    
    Args:
        patient_id (str): ID do paciente.

    Returns:
        tuple: (lista de escalas atribuídas, mensagem de erro ou None).

    Calls:
        Supabase → Tabela 'professional_patient_link'
        Supabase → Tabela 'scales'
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

        scales_response = supabase_client.from_("scales") \
            .select("id, scale_id, created_at") \
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
    Atualiza as respostas de uma escala psicométrica no registro de progresso.

    Fluxo:
        1. Recebe as respostas em formato de dicionário.
        2. Atualiza o campo 'answers' na tabela 'scale_progress' para o registro indicado.
    
    Args:
        scale_progress_id (str): ID do registro na tabela 'scale_progress'.
        answers (dict): Dicionário com as respostas da escala.

    Returns:
        tuple: (bool, mensagem) - Sucesso da operação e mensagem de erro/sucesso.

    Calls:
        Supabase → Tabela 'scale_progress'
    """
    try:
        response = supabase_client.from_("scale_progress").update({"answers": answers}).eq("id", scale_progress_id).execute()
        if hasattr(response, "error") and response.error:
            return False, f"Erro ao atualizar respostas: {response.error.message}"
        return True, "Respostas salvas com sucesso!"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def render_patient_scales(user_id):
    """
    Renderiza as escalas psicométricas atribuídas ao paciente e permite que ele responda.

    Fluxo:
        1. Obtém as escalas atribuídas ao paciente via get_assigned_scales().
        2. Para cada escala, verifica se já existe um registro de progresso para o dia atual.
           Se não existir, chama initialize_scale_progress() para criá-lo.
        3. Exibe a escala com um formulário para o paciente inserir suas respostas.
        4. Ao submeter o formulário, as respostas (em formato de dicionário) são salvas usando update_scale_answers().

    Args:
        user_id (str): ID do paciente autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        scales_utils.py → get_assigned_scales()
        scales_utils.py → initialize_scale_progress()
        scales_utils.py → update_scale_answers()
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

    # Para cada escala, exibe um formulário para responder
    for scale in assigned_scales:
        st.markdown(f"### {scale['scale_id']}")  # Exiba o nome/título da escala conforme necessário
        
        # 2. Inicializa o registro de progresso para hoje (se não existir)
        init_success, scale_progress_id_or_msg = initialize_scale_progress(scale["id"], scale.get("link_id"))
        if not init_success:
            st.error(scale_progress_id_or_msg)
            continue
        scale_progress_id = scale_progress_id_or_msg
        
        # Exibe o formulário para inserir respostas
        with st.form(key=f"form_scale_{scale['id']}"):
            st.write("Responda a escala abaixo:")
            # Exemplo: considere que a escala tem duas perguntas (você pode adaptar conforme a escala real)
            resposta1 = st.text_input("Pergunta 1: Como você se sente hoje?")
            resposta2 = st.text_input("Pergunta 2: Você tem conseguido lidar com suas atividades?")
            
            submitted = st.form_submit_button("Salvar Respostas")
            if submitted:
                # Cria um dicionário com as respostas
                answers = {
                    "pergunta_1": resposta1,
                    "pergunta_2": resposta2
                }
                success, msg = update_scale_answers(scale_progress_id, answers)
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
