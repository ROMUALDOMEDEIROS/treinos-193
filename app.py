import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

# Page configuration
st.set_page_config(page_title="193 Treinos", layout="wide", initial_sidebar_state="collapsed")

# Styles
st.markdown("""
<style>
:root {
    --primary-color: #EF4444;
    --secondary-color: #1F2937;
    --text-color: #FFFFFF;
    --bg-color: #111827;
    --card-bg: #1F2937;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'role' not in st.session_state:
    st.session_state.role = None
if 'athlete_email' not in st.session_state:
    st.session_state.athlete_email = None
if 'athletes' not in st.session_state:
    st.session_state.athletes = {}
if 'app_logo' not in st.session_state:
    st.session_state.app_logo = None

# Constants
COACH_PASSWORD = 'Romo$2228'
DAYS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
TRAINING_TYPES = ['Contínuo', 'Intervalado', 'Fartlek', 'Rodagem Leve', 'Longão']
ZONES = ['Z1', 'Z2', 'Z3', 'Z4']
PERIODS = ['Manhã', 'Tarde', 'Noite']
METRICS = ['PSE', 'Pace', 'Km/h', 'Zonas', 'Frequência Cardíaca']
VAM_TESTS = ['1600m', '3000m', 'TAF']

# VAM Zone Configuration
VAM_ZONE_CONFIG = {
    'Z1': (60, 70),
    'Z2': (71, 85),
    'Z3': (86, 95),
    'Z4': (96, 100)
}

def get_monday(date):
    """Get the Monday of the week for a given date"""
    return date - timedelta(days=date.weekday())

def calculate_current_microcycle(athlete):
    """Calculate the current microcycle number"""
    if 'start_date' not in athlete or not athlete['start_date']:
        return 1
    start_date = datetime.fromisoformat(athlete['start_date'])
    today = datetime.now()
    days_diff = (today - start_date).days
    return max(1, (days_diff // 7) + 1)

def get_empty_plan():
    """Create an empty training plan"""
    return {day: [] for day in range(7)}

def display_home():
    """Display the home screen"""
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown('<div style="text-align: center; padding: 40px;"><div style="border: 3px solid #EF4444; border-radius: 20px; padding: 30px; display: inline-block; background-color: #1F2937;">', unsafe_allow_html=True)
        if st.session_state.app_logo:
            st.image(st.session_state.app_logo, width=150)
        else:
            st.markdown('<h1 style="color: #EF4444; font-size: 48px;">193</h1><p style="color: #FFFFFF;">TREINOS</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 style="text-align: center; color: #FFFFFF;">ACESSE SEU TREINO</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #EF4444; font-size: 20px; font-style: italic;">193 treinos</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #EF4444; font-size: 16px; font-style: italic;">Romualdo.run</p>', unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏃 Sou Atleta")
        athlete_email = st.text_input("Seu e-mail de atleta", key="athlete_login_email")
        if st.button("Acessar Meus Treinos", key="athlete_login_btn", use_container_width=True):
            if athlete_email and athlete_email in st.session_state.athletes:
                st.session_state.role = 'athlete'
                st.session_state.athlete_email = athlete_email
                st.rerun()
            else:
                st.error("E-mail não encontrado")
    
    with col2:
        st.subheader("🎯 Sou Treinador")
        password = st.text_input("Senha do Treinador", type="password", key="coach_login_password")
        if st.button("Acessar Painel", key="coach_login_btn", use_container_width=True):
            if password == COACH_PASSWORD:
                st.session_state.role = 'coach'
                st.rerun()
            else:
                st.error("Senha incorreta")

def display_athlete_dashboard():
    """Display athlete dashboard"""
    athlete = st.session_state.athletes[st.session_state.athlete_email]
    
    st.title(f"Treinos - {athlete['name']}")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("← Voltar"):
            st.session_state.role = None
            st.session_state.athlete_email = None
            st.rerun()
    
    # Microcycle selection
    current_mc = calculate_current_microcycle(athlete)
    st.info(f"🏃 Microciclo {current_mc} (Semana Atual)")
    
    plans = athlete.get('plans', {})
    mc_num = st.number_input("Selecione o Microciclo", min_value=1, value=current_mc)
    
    if str(mc_num) not in plans:
        plans[str(mc_num)] = get_empty_plan()
    
    plan = plans[str(mc_num)]
    
    # Display weekly grid
    st.subheader("Treinos da Semana")
    
    for day_idx, day_name in enumerate(DAYS):
        with st.expander(f"{day_name}", expanded=False):
            workouts = plan.get(day_idx, [])
            
            if workouts:
                for i, workout in enumerate(workouts):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{workout.get('type', 'Treino')}** - {workout.get('period', 'Período')}")
                        st.write(f"Aquecimento: {workout.get('warmup', '-')}")
                        st.write(f"Principal: {workout.get('main', '-')}")
                        st.write(f"Volta à Calma: {workout.get('cooldown', '-')}")
                        st.write(f"Zona: {workout.get('main_zone', '-')}")
                    
                    with col2:
                        completed = st.checkbox(
                            "Realizado",
                            value=workout.get('completed', False),
                            key=f"completed_{day_idx}_{i}"
                        )
                        workout['completed'] = completed
                    
                    with col3:
                        if st.button("✏️", key=f"edit_{day_idx}_{i}"):
                            st.session_state.editing_workout = (day_idx, i)
                            st.rerun()
            else:
                st.info("Nenhum treino planejado para este dia")
    
    # Save athletes data
    st.session_state.athletes[st.session_state.athlete_email] = athlete

def display_coach_panel():
    """Display coach panel"""
    st.title("🎯 Painel do Treinador")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🚪 Sair"):
            st.session_state.role = None
            st.rerun()
    
    # Coach menu
    menu = st.selectbox("Menu", ["Atletas", "Cadastrar Novo Atleta", "Personalizar Marca"])
    
    if menu == "Atletas":
        display_athletes_list()
    elif menu == "Cadastrar Novo Atleta":
        display_athlete_registration()
    elif menu == "Personalizar Marca":
        display_branding()

def display_athletes_list():
    """Display list of registered athletes"""
    st.subheader("Atletas Registrados")
    
    if st.session_state.athletes:
        for email, athlete in st.session_state.athletes.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{athlete['name']}** ({email})")
                if 'vam_info' in athlete:
                    st.caption(f"VAM: {athlete['vam_info'].get('vam_value', '-')} km/h ({athlete['vam_info'].get('test_type', '-')})")
            with col2:
                if st.button("Editar", key=f"edit_athlete_{email}"):
                    st.session_state.editing_athlete = email
                    st.rerun()
            with col3:
                if st.button("Ver Treinos", key=f"view_athlete_{email}"):
                    st.session_state.role = 'athlete_view'
                    st.session_state.viewing_athlete = email
                    st.rerun()
    else:
        st.info("Nenhum atleta cadastrado")

def display_athlete_registration():
    """Display athlete registration form"""
    st.subheader("Cadastrar Novo Atleta")
    
    with st.form("athlete_registration"):
        name = st.text_input("Nome do Atleta")
        email = st.text_input("E-mail")
        
        st.write("**Teste de VAM**")
        test_type = st.selectbox("Tipo de Teste", VAM_TESTS)
        vam_value = st.number_input("VAM (km/h)", min_value=0.0, step=0.1)
        
        submitted = st.form_submit_button("Registrar Atleta", use_container_width=True)
        
        if submitted:
            if name and email:
                st.session_state.athletes[email] = {
                    'name': name,
                    'email': email,
                    'start_date': datetime.now().isoformat(),
                    'vam_info': {
                        'test_type': test_type,
                        'vam_value': vam_value
                    },
                    'plans': {'1': get_empty_plan()}
                }
                st.success(f"Atleta {name} registrado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha todos os campos")

def display_branding():
    """Display branding customization"""
    st.subheader("Customizar Marca")
    
    uploaded_file = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg", "svg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file)
        if st.button("Salvar Logo"):
            import base64
            bytes_data = uploaded_file.getvalue()
            b64_string = base64.b64encode(bytes_data).decode()
            st.session_state.app_logo = f"data:image/{uploaded_file.type};base64,{b64_string}"
            st.success("Logo atualizada!")
            st.rerun()

# Main app logic
if st.session_state.role is None:
    display_home()
elif st.session_state.role == 'athlete':
    display_athlete_dashboard()
elif st.session_state.role == 'coach':
    display_coach_panel()
elif st.session_state.role == 'athlete_view':
    athlete = st.session_state.athletes.get(st.session_state.viewing_athlete)
        st.session_state.athlete_email = st.session_state.viewing_athlete
    if athlete:
        st.title(f"Visualizando Treinos - {athlete['name']}")
        if st.button("← Voltar ao Painel"):
            st.session_state.role = 'coach'
            st.rerun()
        display_athlete_dashboard()
    else:
        st.error("Atleta não encontrado")
