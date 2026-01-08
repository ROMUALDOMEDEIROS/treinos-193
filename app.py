import streamlit as st

st.set_page_config(page_title="193 Treinos", layout="wide")

st.markdown("""
<style>
.container { text-align: center; padding: 20px; background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%); border-radius: 15px; color: white; margin-bottom: 20px; }
.container h1 { margin: 0; font-size: 48px; }
.container p { margin: 5px 0; font-size: 16px; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown('<div class="container"><h1>193 TREINOS</h1><p>Romualdo.run</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏃 Sou Atleta")
        email = st.text_input("Email:")
        if st.button("Ver Treino"):
            st.session_state.email = email
            st.session_state.page = 'athlete'
            st.rerun()
    
    with col2:
        st.subheader("👨‍🏫 Sou Treinador")
        senha = st.text_input("Senha:", type="password")
        if st.button("Acessar Painel"):
            if senha == "Romo$2228":
                st.session_state.page = 'coach'
                st.rerun()
            else:
                st.error("Senha incorreta!")

elif st.session_state.page == 'athlete':
    if st.button("← Voltar"):
        st.session_state.page = 'home'
        st.rerun()
    st.title(f"Treinos - {st.session_state.email}")
    st.info("Nenhum treino cadastrado ainda.")

elif st.session_state.page == 'coach':
    if st.button("Sair"):
        st.session_state.page = 'home'
        st.rerun()
    st.title("👨‍🏫 Painel do Treinador")
    st.success("Bem-vindo!")
    st.write("Cadastre atletas e crie treinos semanais.")
