import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date, datetime, timedelta
from auth import supabase_client
from utils.user_utils import get_user_info
from utils.date_utils import format_date


# 📜 Função para listar os pacientes que estejam vinculados a um profissional.
@st.cache_data(ttl=10)
def get_linked_patients(professional_id):
    """Retorna uma lista de pacientes vinculados a um profissional."""
    try:
        # Buscar os vínculos aceitos entre o profissional e pacientes
        response = supabase_client.from_("professional_patient_link") \
            .select("patient_id, status") \
            .eq("professional_id", professional_id) \
            .eq("status", "accepted") \
            .execute()  # 🔹 Agora está corretamente alinhado

        if hasattr(response, "error") and response.error:
            return [], f"Erro ao buscar pacientes vinculados: {response.error.message}"

        if not response.data:
            return [], "Nenhum vínculo encontrado."

        # Obter IDs de pacientes vinculados
        patient_ids = [item["patient_id"] for item in response.data]

        # Buscar os dados dos pacientes vinculados
        patients = []
        for patient_id in patient_ids:
            patient_info = get_user_info(patient_id, by_email=False, full_profile=False)  # 🔹 Forçando busca por ID
            if patient_info and patient_info.get("auth_user_id"):
                patients.append({
                    "id": patient_id,
                    "name": f"{patient_info['display_name']} ({patient_info['email']})"
                })
            else:
                st.warning(f"⚠️ Paciente com ID {patient_id} não encontrado no banco!")  # Log para debug

        return patients, None

    except Exception as e:  # 🔹 Certifique-se de que está na mesma indentação do `try`
        return [], f"Erro inesperado: {str(e)}"
    

# 💎 Função para adicionar metas.
def add_goal_to_patient(professional_id, patient_email, goal, timeframe):
    """Adiciona uma meta para um paciente vinculado a um profissional."""
    try:
        # 🔍 Buscar ID do paciente pelo email
        patient_info = get_user_info(patient_email, by_email=True, full_profile=True)
        if not patient_info or not patient_info.get("auth_user_id"):
            return False, "Paciente não encontrado."

        patient_id = patient_info["auth_user_id"]

        # 🔗 Buscar link_id do vínculo entre profissional e paciente
        link_response = supabase_client.from_("professional_patient_link") \
            .select("id") \
            .eq("professional_id", professional_id) \
            .eq("patient_id", patient_id) \
            .eq("status", "accepted") \
            .execute()

        if not link_response.data:
            return False, "Nenhum vínculo ativo encontrado com este paciente."

        link_id = link_response.data[0]["id"]

        # 📝 Criar a meta
        data = {
            "link_id": link_id,
            "goal": goal,
            "timeframe": timeframe
        }
        response = supabase_client.from_("goals").insert(data).execute()

        if hasattr(response, "error") and response.error:
            return False, f"Erro ao adicionar meta: {response.error.message}"

        return True, "Meta adicionada com sucesso!"
    
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


# ⛏️ Função para registrar o progresso de uma meta.
def update_goal_progress(goal_id, link_id, completed):
    """
    Atualiza ou insere o progresso da meta para o paciente no dia atual.

    Fluxo:
        1. Verifica se já existe um registro para essa meta (`goal_id`) no dia atual.
        2. Se existir, atualiza o campo `completed` (marcando ou desmarcando a meta).
        3. Se não existir, insere um novo registro no banco de dados.
        4. Garante que apenas um registro seja feito por dia por meta.

    Args:
        goal_id (str): ID da meta.
        link_id (str): ID do vínculo paciente-profissional.
        completed (bool): Status da meta (True para cumprida, False para não cumprida).

    Returns:
        bool, str: Sucesso da operação e mensagem de erro/sucesso.

    Calls:
        Supabase → `goal_progress`
    """

    today = date.today().isoformat()  # Obtém a data atual no formato YYYY-MM-DD

    try:
        # 🔍 Verifica se já existe um registro para essa meta no dia atual
        response = supabase_client.from_("goal_progress") \
            .select("id") \
            .eq("goal_id", goal_id) \
            .eq("date", today) \
            .execute()

        if hasattr(response, "error") and response.error:
            return False, f"Erro ao verificar progresso: {response.error.message}"

        if response.data:  # Se já existir um registro, faz um update
            progress_id = response.data[0]["id"]
            update_response = supabase_client.from_("goal_progress") \
                .update({"completed": completed}) \
                .eq("id", progress_id) \
                .execute()

            if hasattr(update_response, "error") and update_response.error:
                return False, f"Erro ao atualizar progresso: {update_response.error.message}"
        else:  # Se não existir, cria um novo registro
            insert_response = supabase_client.from_("goal_progress") \
                .insert({"goal_id": goal_id, "link_id": link_id, "date": today, "completed": completed}) \
                .execute()

            if hasattr(insert_response, "error") and insert_response.error:
                return False, f"Erro ao registrar progresso: {insert_response.error.message}"

        return True, "Progresso atualizado com sucesso!"

    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"
    

# 🖨️ Função para buscar as metas designadas para um paciente.
@st.cache_data(ttl=10)
def get_patient_goals(patient_id):
    """Busca as metas designadas para o paciente."""
    try:
        # Buscar o vínculo do paciente com um profissional
        link_response = supabase_client.from_("professional_patient_link") \
            .select("id") \
            .eq("patient_id", patient_id) \
            .eq("status", "accepted") \
            .execute()

        if hasattr(link_response, "error") and link_response.error:
            return [], f"Erro ao buscar vínculo: {link_response.error.message}"

        if not link_response.data:
            return [], "Nenhum vínculo ativo encontrado."

        link_id = link_response.data[0]["id"]

        # Buscar metas associadas ao link_id
        goals_response = supabase_client.from_("goals") \
            .select("id, link_id, goal, timeframe, created_at") \
            .eq("link_id", link_id) \
            .order("created_at", desc=True) \
            .execute()



        if hasattr(goals_response, "error") and goals_response.error:
            return [], f"Erro ao buscar metas: {goals_response.error.message}"

        if not goals_response.data:
            return [], "Nenhuma meta encontrada."

        return goals_response.data, None

    except Exception as e:
        return [], f"Erro inesperado: {str(e)}"


# 📦 Função para agrupar metas na dashboard
def group_goals_by_timeframe(goals):
    """
    Agrupa a lista de metas por prazo (curto, medio, longo).

    Fluxo:
        1. Inicializa um dicionário com chaves "curto", "medio" e "longo".
        2. Percorre cada meta na lista.
        3. Se o campo "timeframe" da meta corresponder a uma das chaves, adiciona a meta à lista correspondente.

    Args:
        goals (list): Lista de dicionários com dados das metas.

    Returns:
        dict: Dicionário com as metas agrupadas por prazo.
    """
    grouped = {"curto": [], "medio": [], "longo": []}
    for goal in goals:
        if goal.get("timeframe") in grouped:
            grouped[goal["timeframe"]].append(goal)
    return grouped


# 🖥️ Função para renderizar a seção "Adicionar Meta para Paciente".
def render_add_goal_section(user):
    """
    Renderiza a seção de adição de metas para um paciente vinculado.

    Fluxo:
        1. Obtém a lista de pacientes vinculados ao profissional autenticado.
        2. Se não houver pacientes vinculados, exibe uma mensagem e retorna.
        3. Caso existam pacientes, exibe um selectbox para escolher um paciente.
        4. Permite ao profissional inserir uma meta e selecionar um prazo válido.
        5. Envia os dados para o banco de dados ao clicar no botão "Salvar Meta".

    Args:
        user (dict): Dicionário contendo os dados do usuário autenticado.

    Returns:
        None (apenas renderiza a interface).

    Calls:
        goals_utils.py → get_linked_patients()
        goals_utils.py → add_goal_to_patient()
    """

    st.markdown("### 🎯 Adicionar Meta para Paciente")

    # Buscar pacientes vinculados ao profissional
    patients, error_msg = get_linked_patients(user["id"])

    if error_msg:
        st.error(error_msg)
        return

    if not patients:
        st.warning("⚠️ Nenhum paciente vinculado encontrado.")
        return

    # Criar lista de nomes para exibição no selectbox
    patient_options = {p["name"]: p["id"] for p in patients}
    
    # Seleção do paciente vinculado
    selected_patient_name = st.selectbox("Selecione o paciente:", list(patient_options.keys()), key="select_patient")

    # Obtém o `patient_id` correspondente ao nome selecionado
    selected_patient_id = patient_options[selected_patient_name]

    # Campo para a meta
    goal_text = st.text_area("Descrição da meta:", key="goal_text")

    # Lista de prazos válidos com base na restrição do banco de dados
    valid_timeframes = {
        "Curto prazo (até 1 mês)": "curto",
        "Médio prazo (1 a 6 meses)": "medio",
        "Longo prazo (acima de 6 meses)": "longo"
    }

    # Selectbox com os nomes amigáveis
    selected_timeframe = st.selectbox("Selecione o prazo para a meta:", list(valid_timeframes.keys()), key="goal_timeframe")

    # Converte para o formato aceito pelo banco de dados
    timeframe = valid_timeframes[selected_timeframe]

    # Botão para salvar a meta
    if st.button("Salvar Meta", key="save_goal", use_container_width=True):
        if selected_patient_id and goal_text and timeframe:
            success, msg = add_goal_to_patient(user["id"], selected_patient_id, goal_text, timeframe)
            if success:
                st.success("✅ Meta adicionada com sucesso!")
            else:
                st.error(f"Erro: {msg}")
        else:
            st.warning("⚠️ Preencha todos os campos antes de salvar.")


# 🖥️ Função para renderizar o checkbox de uma meta de curto prazo.
def render_goal_checkbox(goal):
    """
    Renderiza o checkbox para uma meta de curto prazo, permitindo marcar o progresso diário.

    Fluxo:
        1. Obtém a data atual no formato ISO (YYYY-MM-DD) e armazena em `today_str`.
        2. Consulta a tabela "goal_progress" para verificar se já existe um registro para a meta (goal["id"]) na data atual.
        3. Se existir um registro com completed=True para hoje, exibe um checkbox desabilitado com a mensagem "Meta concluída hoje".
        4. Caso contrário, exibe um checkbox interativo para o usuário marcar a meta como cumprida.
        5. Se o usuário marcar o checkbox, chama a função update_goal_progress() para registrar ou atualizar o progresso da meta.
    
    Args:
        goal (dict): Dicionário contendo os dados da meta, devendo incluir:
                     - "id": Identificador único da meta.
                     - "link_id": ID do vínculo entre o paciente e o profissional.
                     Exemplo:
                     {
                         "id": "abc123",
                         "link_id": "def456",
                         "goal": "Exemplo de meta",
                         ...
                     }

    Returns:
        None: A função apenas renderiza o componente (checkbox) na interface do Streamlit,
              sem retornar valor explícito.

    Calls:
        - supabase_client.from_("goal_progress"): Para consultar os registros de progresso da meta no banco de dados.
        - update_goal_progress(goal_id, link_id, completed): Função responsável por inserir ou atualizar o progresso
          da meta no banco de dados.
    """
    from datetime import date
    # 1. Obtém a data atual no formato ISO (YYYY-MM-DD)
    today_str = date.today().isoformat()

    # 2. Consulta a tabela "goal_progress" para verificar se já existe um registro para essa meta na data atual
    progress_response = supabase_client.from_("goal_progress") \
        .select("completed") \
        .eq("goal_id", goal["id"]) \
        .eq("date", today_str) \
        .execute()

    completed_today = False
    if progress_response.data:
        completed_today = progress_response.data[0]["completed"]

    # 3. Se a meta já estiver concluída hoje, exibe o checkbox desabilitado com uma chave única (usando today_str)
    if completed_today:
        st.checkbox("Meta concluída hoje", value=True, disabled=True, key=f"goal_{goal['id']}_done_{today_str}")
    else:
        # 4. Exibe um checkbox interativo para marcar a meta como cumprida, com uma chave única também
        checked = st.checkbox("Marcar como cumprida hoje", value=False, key=f"goal_{goal['id']}_{today_str}")
        # 5. Se o checkbox for marcado, chama a função update_goal_progress para atualizar o progresso
        if checked:
            success, msg = update_goal_progress(goal["id"], goal["link_id"], True)
            if success:
                st.success(msg)
            else:
                st.error(msg)



# 🖥️ Função para renderizar o expander de metas.
def render_goal_expander(goal, prazo):
    """
    Renderiza o expander para uma meta, exibindo seus detalhes e, se for de curto prazo, o checkbox acima do expander.
    Além disso, se for meta de curto prazo, exibe dentro do expander o gráfico de progresso dos últimos 30 dias.

    Fluxo:
        1. Formata a data de criação da meta com a função format_date().
        2. Se o prazo for "curto":
            a. Chama render_goal_checkbox() para exibir o checkbox fora do expander.
        3. Cria um expander com o título da meta.
        4. Dentro do expander:
            a. Exibe a data formatada.
            b. Se a meta for de curto prazo, chama render_goal_progress_chart() para exibir o gráfico.
            c. Se não for curto, exibe uma mensagem informativa.
    
    Args:
        goal (dict): Dicionário contendo os dados da meta, incluindo 'goal' (descrição) e 'created_at' (data de atribuição).
        prazo (str): Tipo da meta ("curto", "medio" ou "longo").

    Returns:
        None: A função apenas renderiza componentes na interface.
    
    Calls:
        - format_date(): Para formatar a data da meta.
        - render_goal_checkbox(): Para exibir o checkbox (caso a meta seja de curto prazo).
        - render_goal_progress_chart(): Para renderizar o gráfico de progresso (para metas de curto prazo).
        - st.expander(): Para criar a seção expansível com os detalhes da meta.
    """
    dia, mes, ano = format_date(goal['created_at'])
    data_formatada = f"{dia:02d}/{mes:02d}/{ano}" if dia else "Data inválida"
    
    # Se a meta for de curto prazo, renderiza o checkbox fora do expander
    if prazo == "curto":
        render_goal_checkbox(goal)
    
    # Cria o expander para exibir os detalhes da meta
    with st.expander(f"📝 {goal['goal']}"):
        st.markdown(f"🕒 **Adicionada em:** {data_formatada}")
        if prazo == "curto":
            # Exibe o gráfico de progresso dos últimos 30 dias dentro do expander
            render_goal_progress_chart(goal)
        else:
            st.info("Essa meta não pode ser concluída a curto prazo.")



# 🖥️ Função para renderizar as metas de um paciente.
def render_patient_goals(user_id):
    """
    Renderiza as metas atribuídas ao paciente, permitindo que ele registre o progresso diário 
    (apenas para metas de curto prazo).

    Fluxo:
        1. Exibe um título grande e chamativo "Minhas Metas" com HTML customizado.
        2. Busca as metas do paciente a partir do banco de dados.
        3. Agrupa as metas por prazo (curto, médio e longo) utilizando group_goals_by_timeframe().
        4. Para cada grupo, exibe um cabeçalho (subtítulo) estilizado em laranja e, para cada meta,
           chama render_goal_expander() para exibir seus detalhes.
    
    Args:
        user_id (str): ID do paciente autenticado.
    
    Returns:
        None: A função apenas renderiza a interface.
    
    Calls:
        - get_patient_goals() para buscar as metas.
        - group_goals_by_timeframe() para agrupar as metas.
        - render_goal_expander() para exibir os detalhes de cada meta.
    """
    # Exibe o título "Minhas Metas" com estilo chamativo
    st.markdown(
        """
        <h2 style='color: white; font-size: 36px; font-weight: bold;'>
        🎯 Minhas Metas
        </h2>
        """,
        unsafe_allow_html=True
    )

    # 1. Buscar as metas do paciente
    goals, error_msg = get_patient_goals(user_id)
    if error_msg:
        st.error(error_msg)
        return
    if not goals:
        st.info("⚠️ Nenhuma meta foi designada para você ainda.")
        return

    # 2. Agrupar as metas por prazo
    grouped_goals = group_goals_by_timeframe(goals)
    prazo_labels = {
        "curto": "Metas de Curto Prazo",
        "medio": "Metas de Médio Prazo",
        "longo": "Metas de Longo Prazo"
    }
    
    # 3. Exibir cada grupo de metas com um subtítulo estilizado
    for prazo, metas in grouped_goals.items():
        if metas:
            st.markdown(
                f"""
                <h4 style='color: #FFA500; font-size: 24px; font-weight: bold; margin-top: 20px;'>
                {prazo_labels[prazo]}
                </h4>
                """,
                unsafe_allow_html=True
            )
            for goal in metas:
                render_goal_expander(goal, prazo)



# 🖥️ Função para renderizar o gráfico de metas de curto prazo.
def render_goal_progress_chart(goal):
    """
    Renderiza um gráfico de linha interativo de 30 dias, mostrando o somatório cumulativo de True's (metas cumpridas)
    ao longo do período, começando na data em que a meta foi criada, utilizando a biblioteca Plotly para
    tornar a visualização mais dinâmica e com zoom.

    Fluxo:
        1. Verifica se o campo 'created_at' existe no dicionário da meta. Se não, exibe um aviso e retorna.
        2. Converte 'created_at' em um objeto date (usando apenas YYYY-MM-DD).
        3. Define o intervalo de 30 dias (data de início até data_início + 29 dias).
        4. Cria um dicionário (progress_dict) que mapeia cada dia do intervalo para 0 (inicialmente).
        5. Consulta a tabela "goal_progress" para obter todos os registros de progresso no intervalo.
        6. Para cada registro com completed=True, soma 1 no dia correspondente do progress_dict.
        7. Ordena as datas e calcula a soma cumulativa, criando um DataFrame pandas com as datas (convertidas para datetime)
           e a soma cumulativa.
        8. Cria um gráfico de linha interativo com Plotly, adicionando um range slider (sem os botões de seleção).
        9. Atualiza o layout do gráfico, aumentando a fonte do título e aplicando o template "seaborn".
        10. Renderiza o gráfico na interface do Streamlit usando st.plotly_chart().

    Args:
        goal (dict): Dicionário com os dados da meta, devendo incluir:
                     - "id": identificador único da meta
                     - "created_at": data em que a meta foi criada (no formato ISO, ex.: "YYYY-MM-DDTHH:MM:SS")

    Returns:
        None: A função apenas renderiza o gráfico na interface, sem retornar valor explícito.

    Calls:
        - supabase_client.from_("goal_progress") para buscar registros de progresso do banco de dados.
        - plotly.express (px) para criar e exibir o gráfico de linha.
        - st.plotly_chart(fig) para renderizar o gráfico na tela do Streamlit.
    """
    # 1. Verifica se 'created_at' existe
    if not goal.get("created_at"):
        st.warning("Data de criação da meta não disponível para exibir o gráfico.")
        return

    try:
        # 2. Converte a data de criação (apenas os 10 primeiros caracteres: YYYY-MM-DD)
        start_date = datetime.strptime(goal['created_at'][:10], "%Y-%m-%d").date()
    except Exception as e:
        st.error(f"Erro ao processar a data de criação: {e}")
        return

    # 3. Define o intervalo de 30 dias
    end_date = start_date + timedelta(days=29)

    # 4. Inicializa o dicionário com valor 0 para cada dia do intervalo
    progress_dict = {}
    current_date = start_date
    while current_date <= end_date:
        progress_dict[current_date.isoformat()] = 0
        current_date += timedelta(days=1)

    # 5. Consulta o banco para obter os registros de progresso dessa meta no intervalo
    response = supabase_client.from_("goal_progress") \
        .select("date, completed") \
        .eq("goal_id", goal["id"]) \
        .gte("date", start_date.isoformat()) \
        .lte("date", end_date.isoformat()) \
        .execute()

    # 6. Para cada registro com completed=True, soma 1 no dia correspondente
    if response and hasattr(response, "data") and response.data:
        for record in response.data:
            record_date = record["date"][:10]  # YYYY-MM-DD
            if record_date in progress_dict and record["completed"]:
                progress_dict[record_date] += 1

    # 7. Ordena as datas e calcula a soma cumulativa
    sorted_dates = sorted(progress_dict.keys())
    daily_counts = [progress_dict[d] for d in sorted_dates]

    cumulative_counts = []
    running_sum = 0
    for c in daily_counts:
        running_sum += c
        cumulative_counts.append(running_sum)

    # Constrói um DataFrame com as datas convertidas para datetime e a soma cumulativa
    df = pd.DataFrame({
        "Data": [datetime.strptime(d, "%Y-%m-%d") for d in sorted_dates],
        "Soma Cumulativa": cumulative_counts
    })

    # 8. Cria um gráfico de linha interativo com Plotly
    fig = px.line(
        df,
        x="Data",
        y="Soma Cumulativa",
        markers=True,
        title="Progresso Cumulativo da Meta"
    )

    # Adiciona zoom apenas com o range slider, sem botões de seleção de intervalo
    fig.update_layout(
        xaxis_title="Barra de Progresso 💎",
        yaxis_title="Esforço ⛏️",
        xaxis=dict(
            showgrid=False,
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(showgrid=True, rangemode="tozero")
    )
    fig.update_xaxes(tickformat="%d/%m", tickangle=45)
    
    # 9. Atualiza o layout para aplicar o template e aumentar a fonte do título
    fig.update_layout(
        title_font=dict(size=20, color="white")
    )

    # 10. Renderiza o gráfico na interface do Streamlit
    st.plotly_chart(fig, use_container_width=True)

