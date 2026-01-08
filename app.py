import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="193 Treinos", layout="wide")

st.markdown("""
<style>
.container { text-align: center; padding: 20px; background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%); border-radius: 15px; color: white; margin-bottom: 20px; }
.container h1 { margin: 0; font-size: 48px; }
.container p { margin: 5px 0; font-size: 16px; }
.card { background: #f0f0f0; padding: 15px; border-radius: 10px; border-left: 4px solid #c41e3a; margin: 10px 0; }
.zone { display: inline-block; padding: 8px 12px; border-radius: 5px; margin: 5px; color: white; font-weight: bold; }
.z1 { background-color: #0099ff; }
.z2 { background-color: #66cc33; }
.z3 { background-color: #ffcc00; color: black; }
.z4 { background-color: #ff6633; }
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'athletes' not in st.session_state:
    st.session_state.athletes = {}
if 'workouts' not in st.session_state:
    st.session_state.workouts = {}

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
    athlete_email = st.session_state.email
    if athlete_email in st.session_state.workouts:
        for day, day_workouts in st.session_state.workouts[athlete_email].items():
            st.write(f"**{day}**")
            for workout in day_workouts:
                st.markdown(f"""
                <div class="card">
                    <b>{workout['type']}</b><br>
                    Aquecimento: {workout.get('warm', '0')} | Principal: {workout.get('main', '0')} | Volta à Calma: {workout.get('cool', '0')}<br>
                    <span class="zone z{workout.get('zone', 'z1')[-1]}">{workout.get('zone', 'Z1')}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum treino cadastrado ainda.")

elif st.session_state.page == 'coach':
    if st.button("Sair"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.title("👨‍🏫 Painel do Treinador")
    
    tab1, tab2 = st.tabs(["Cadastrar Atleta", "Planejar Treino"])
    
    with tab1:
        st.subheader("Cadastrar Novo Atleta")
        with st.form("athlete_form"):
            name = st.text_input("Nome do Atleta:")
            email = st.text_input("Email:")
            if st.form_submit_button("Cadastrar"):
                st.session_state.athletes[email] = {'name': name, 'email': email}
                if email not in st.session_state.workouts:
                    st.session_state.workouts[email] = {}
                st.success(f"Atleta {name} cadastrado!")
    
    with tab2:
        st.subheader("📝 Planejar Treino Semanal")
        if st.session_state.athletes:
            athlete_email = st.selectbox("Selecione o Atleta:", list(st.session_state.athletes.keys()), format_func=lambda x: st.session_state.athletes[x]['name'])
            day = st.selectbox("Dia da Semana:", ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"])
            
            with st.form("workout_form"):
                st.write("**Tipo de Treino:**")
                training_type = st.selectbox("Escolha:", ["CONTÍNUO", "INTERVALADO", "FARTLEK", "RODAGEM LEVE", "LONGÃO"])
                
                st.write("**Estrutura do Treino:**")
                warmup = st.text_input("Aquecimento (ex: 2 km):", value="2 km")
                main = st.text_input("Treino Principal (ex: 10 km):", value="10 km")
                cooldown = st.text_input("Volta à Calma (ex: 2 km):", value="2 km")
                
                st.write("**Zona de Intensidade:**")
                zone = st.selectbox("Zona:", ["Z1", "Z2", "Z3", "Z4"])
                
                if st.form_submit_button("💾 Salvar Treino"):
                    if day not in st.session_state.workouts[athlete_email]:
                        st.session_state.workouts[athlete_email][day] = []
                    
                    st.session_state.workouts[athlete_email][day].append({
                        'type': training_type,
                        'warm': warmup,
                        'main': main,
                        'cool': cooldown,
                        'zone': zone
                    })
                    st.success(f"Treino adicionado para {day}!")
        else:
            st.warning("Nenhum atleta cadastrado. Cadastre um atleta primeiro!")
