import streamlit as st
import pandas as pd
from datetime import datetime
import json

st.set_page_config(page_title="193 Treinos", layout="wide")

st.markdown("""
<style>
.logo-container {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%);
    border-radius: 15px;
    color: white;
    margin-bottom: 20px;
}
.logo-container h1 { margin: 0; font-size: 48px; }
.logo-container p { margin: 5px 0; font-size: 16px; }
.training-card {
    background: #f0f0f0;
    padding: 15px;
    border-radius: 10px;
    border-left: 4px solid #c41e3a;
    margin: 10px 0;
}
.zone-box {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 5px;
    margin: 5px;
    color: white;
    font-weight: bold;
}
.z1 { background-color: #0099ff; }
.z2 { background-color: #66cc33; }
.z3 { background-color: #ffcc00; color: black; }
.z4 { background-color: #ff6633; }
</style>
""", unsafe_allow_html=True)

if 'athletes' not in st.session_state:
    st.session_state.athletes = {}
if 'view' not in st.session_state:
    st.session_state.view = 'home'

COACH_PASSWORD = "Romo$2228"
TRAINING_TYPES = ["CONTINUO", "INTERVALADO", "FARTLEK", "RODAGEM LEVE", "LONGAO"]
ZONES = ["Z1", "Z2", "Z3", "Z4"]

if st.session_state.view == 'home':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="logo-container">
            <h1>193 TREINOS</h1>
            <p>Romualdo.run</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏃 Sou Atleta")
        athlete_email = st.text_input("Email do Atleta:")
        if st.button("Ver Meu Treino"):
            if athlete_email in st.session_state.athletes:
                st.session_state.current_athlete = athlete_email
                st.session_state.view = 'athlete'
                st.rerun()
            else:
                st.error("Atleta nao encontrado!")
    
    with col2:
        st.subheader("👨‍🏫 Sou Treinador")
        password = st.text_input("Senha:", type="password")
        if st.button("Acessar Painel"):
            if password == COACH_PASSWORD:
                st.session_state.view = 'coach'
                st.rerun()
            else:
                st.error("Senha errada!")

elif st.session_state.view == 'coach':
    st.title("👨‍🏫 Painel do Treinador")
    if st.button("Sair"):
        st.session_state.view = 'home'
        st.rerun()
    
    tab1, tab2 = st.tabs(["Cadastrar Atleta", "Planejar Treinos"])
    
    with tab1:
        st.subheader("Cadastrar Novo Atleta")
        with st.form("athlete_form"):
            name = st.text_input("Nome:")
            email = st.text_input("Email:")
            vam = st.number_input("VAM (km/h):", min_value=0.0)
            
            if st.form_submit_button("Cadastrar"):
                st.session_state.athletes[email] = {
                    'name': name,
                    'vam': vam,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'workouts': {}
                }
                st.success("Atleta cadastrado!")
    
    with tab2:
        st.subheader("Planejar Treino")
        emails = list(st.session_state.athletes.keys())
        if emails:
            select_email = st.selectbox("Atleta:", emails)
            day = st.selectbox("Dia:", ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"])
            
            with st.form("workout_form"):
                type_w = st.selectbox("Tipo:", TRAINING_TYPES)
                warm = st.text_input("Aquecimento:", value="2 km")
                main = st.text_input("Principal:", value="10 km")
                cool = st.text_input("Volta a Calma:", value="2 km")
                zone = st.selectbox("Zona:", ZONES)
                
                if st.form_submit_button("Salvar"):
                    if day not in st.session_state.athletes[select_email]['workouts']:
                        st.session_state.athletes[select_email]['workouts'][day] = []
                    
                    st.session_state.athletes[select_email]['workouts'][day].append({
                        'type': type_w,
                        'warm': warm,
                        'main': main,
                        'cool': cool,
                        'zone': zone
                    })
                    st.success("Treino salvo!")
        else:
            st.info("Nenhum atleta cadastrado ainda.")

elif st.session_state.view == 'athlete':
    if st.button("<- Voltar"):
        st.session_state.view = 'home'
        st.rerun()
    
    athlete = st.session_state.athletes.get(st.session_state.current_athlete, {})
    st.title(f"Treinos de {athlete.get('name', 'Atleta')}")
    
    workouts = athlete.get('workouts', {})
    if workouts:
        for day, day_workouts in workouts.items():
            st.write(f"**{day}**")
            for workout in day_workouts:
                st.markdown(f"""
                <div class="training-card">
                    <b>{workout['type']}</b><br>
                    Aquecimento: {workout['warm']} | Principal: {workout['main']} | Volta a Calma: {workout['cool']}<br>
                    <span class="zone-box z{workout['zone'][-1]}">{workout['zone']}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum treino cadastrado ainda.")
