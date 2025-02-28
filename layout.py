import streamlit as st

def render_main_layout():
    """Renderiza a interface principal com título e botão de navegação."""
    
    # 📌 Nome do App
    st.title("Academia Diagnóstica 🧠")

    # 📌 Subtítulo
    st.subheader("Um sistema inteligente e adaptado para o novo paradigma dos transtornos mentais")

    # 📌 Criando um botão estilizado para abrir a sidebar
    col1, col2, col3 = st.columns([1, 3, 1])  # Layout centralizado

    with col2:  # Centraliza o botão
        if st.button("🚀 Explorar Agora", key="explore", use_container_width=True):
            st.session_state["show_sidebar"] = True  # 🚀 Ativa a sidebar
            st.rerun()  # 🔄 Recarrega a interface para mostrar a sidebar

    # 📌 Introdução com Markdown
    st.markdown(
        """
        #### **Como a Academia Diagnóstica pode transformar sua prática?**  
        
        - **Crie uma conta profissional** e acesse um ambiente especializado para profissionais da saúde mental.
        - **Cadastre pacientes e acompanhe sua trajetória clínica** com dados organizados e insights em tempo real.
        - **Aplique avaliações informatizadas** e obtenha resultados rápidos e padronizados.
        - **Utilize nossas correções automatizadas**, garantindo precisão na interpretação dos dados.
        - **Monitore a evolução longitudinalmente**, observando padrões de melhora ou agravamento ao longo do tempo.

        🎯 **Com a Academia Diagnóstica, você tem em mãos um sistema inteligente e baseado em evidências.**  
        
        🔍 **Eleve sua prática para um novo nível e ofereça aos seus pacientes um acompanhamento mais eficaz e personalizado.**  
        """
    )
