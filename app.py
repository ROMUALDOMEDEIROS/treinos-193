import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="193 Treinos", layout="wide")

# Custom CSS
st.markdown("""
<style>
.container { text-align: center; padding: 20px; background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%); border-radius: 15px; color: white; margin-bottom: 20px; }
.container h1 { margin: 0; font-size: 48px; font-weight: bold; }
.container p { margin: 5px 0; font-size: 16px; }
.card { background: #f0f0f0; padding: 15px; border-radius: 10px; border-left: 4px solid #c41e3a; margin: 10px 0; }
.zone { display: inline-block; padding: 8px 12px; border-radius: 5px; margin: 5px; color: white; font-weight: bold; font-size: 12px; }
.z1 { background-color: #0099ff; }
.z2 { background-color: #66cc33; }
.z3 { background-color: #ffcc00; color: black; }
.z4 { background-color: #ff6633; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'athletes' not in st.session_state:
    st.session_state.athletes = {}
if 'workouts' not in st.session_state:
    st.session_state.workouts = {}
if 'current_athlete' not in st.session_state:
    st.session_state.current_athlete = None
if 'app_logo' not in st.session_state:
    st.session_state.app_logo = None

COACH_PASSWORD = "Romo$2228"

# VAM Zones Configuration
VAM_ZONE_CONFIG = {
    'Z1': {'min': 0.01, 'max': 0.65, 'label': 'Z1 - Base', 'color': '#0099ff'},
    'Z2': {'min': 0.65, 'max': 0.80, 'label': 'Z2 - Produtivo', 'color': '#66cc33'},
    'Z3': {'min': 0.80, 'max': 1.0, 'label': 'Z3 - Lactato', 'color': '#ffcc00'},
    'Z4': {'min': 1.0, 'max': 1.2, 'label': 'Z4 - AnAerobic', 'color': '#ff6633'},
}

def calculate_vam_zones(vam_value)
:training zones based on VAM"""
    zones = {}
    for zone_name, config in VAM_ZONE_CONFIG.items():
        min_speed = vam_value * config['min']
        max_speed = vam_value * config['max']
        zones[zone_name] = {
            'speed': f"{min_speed:.1f} - {max_speed:.1f} km/h",
            'pace': f"{60/max_speed:.2f} - {60/min_speed:.2f} min/km"
        }
    return zones

def calculate_microcycle(athlete):
    """Calculate current microcycle based on start date"""
    if 'start_date' not in athlete:
        return 1
    start = datetime.strptime(athlete['start_date'], '%Y-%m-%d')
    today = datetime.now()
    days_diff = (today - start).days
    return (days_diff // 7) + 1

if st.session_state.page == 'home':
    # Home page
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(
            '<div class="container"><h1>193 TREINOS</h1><p>Romualdo.run</p></div>',
            unsafe_allow_html=True
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏃 Sou Atleta")
        email = st.text_input("Email:")
        if st.button("Ver Treino"):
            if email in st.session_state.athletes:
                st.session_state.current_athlete = email
                st.session_state.page = 'athlete_view'
                st.rerun()
            else:
                st.error("Atleta não encontrado!")
    
    with col2:
        st.subheader("🏆 Sou Treinador")
        password = st.text_input("Senha do Treinador:", type="password")
        if st.button("Acessar Painel"):
            if password == COACH_PASSWORD:
                st.session_state.page = 'coach_panel'
                st.rerun()
            else:
                st.error("Senha incorreta!")

elif st.session_state.page == 'coach_panel':
    st.title("🏆 Painel do Treinador")
    
    coach_menu = st.tabs(["Cadastrar Atleta", "Planejar Treino", "Visualizar Atletas"])
    
    with coach_menu[0]:
        st.subheader("Cadastro de Novo Atleta")
        athlete_name = st.text_input("Nome do Atleta")
        athlete_email = st.text_input("Email do Atleta")
        vam_test = st.selectbox("Teste VAM", ["1600m", "3000m", "TAF"])
        vam_value = st.number_input("Valor VAM (km/h)", min_value=10.0, max_value=25.0, value=15.0)
        
        if st.button("Cadastrar Atleta"):
            if athlete_email not in st.session_state.athletes:
                st.session_state.athletes[athlete_email] = {
                    'name': athlete_name,
                    'email': athlete_email,
                    'vam_test': vam_test,
                    'vam_value': vam_value,
                    'start_date': datetime.now().strftime('%Y-%m-%d'),
                    'zones': calculate_vam_zones(vam_value),
                }
                st.success(f"Atleta {athlete_name} cadastrado com sucesso!")
            else:
                st.error("Esse email já está cadastrado!")
    
    with coach_menu[1]:
        st.subheader("Planejar Treino")
        selected_athlete = st.selectbox("Selecionar Atleta", 
                                        list(st.session_state.athletes.keys()) if st.session_state.athletes else ["Nenhum atleta"])
        
        if selected_athlete and selected_athlete != "Nenhum atleta":
            athlete = st.session_state.athletes[selected_athlete]
            microcycle = calculate_microcycle(athlete)
            
            st.info(f"Atleta: {athlete['name']} | Microciclo Atual: {microcycle}")
            
            days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            
            cols = st.columns(7)
            for day_idx, (col, day) in enumerate(zip(cols, days)):
                with col:
                    st.subheader(day)
                    
                    # Add workout
                    if st.button(f"+ Treino", key=f"add_{day_idx}"):
                        st.session_state.page = f"edit_workout_{selected_athlete}_{day_idx}"
                        st.rerun()
    
    with coach_menu[2]:
        st.subheader("Atletas Cadastrados")
        if st.session_state.athletes:
            for email, athlete in st.session_state.athletes.items():
                with st.expander(f"{athlete['name']} ({email})"):
                    st.write(f"**VAM:** {athlete['vam_value']} km/h ({athlete['vam_test']})")
                    st.write(f"**Data de Cadastro:** {athlete['start_date']}")
                    st.write(f"**Microciclo Atual:** {calculate_microcycle(athlete)}")
        else:
            st.info("Nenhum atleta cadastrado ainda.")

elif st.session_state.page == 'athlete_view':
    athlete_email = st.session_state.current_athlete
    athlete = st.session_state.athletes[athlete_email]
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            '<div class="container"><h1>193 TREINOS</h1><p>Romualdo.run</p></div>',
            unsafe_allow_html=True
        )
    
    st.title(f"Olá {athlete['name']}!")
    
    if st.button("← Voltar"):
        st.session_state.page = 'home'
        st.rerun()
    
    microcycle = calculate_microcycle(athlete)
    st.info(f"Microciclo {microcycle} - Semana de {athlete['start_date']}")
    
    st.subheader("Suas Zonas de Treino (VAM)")
    zones_df = pd.DataFrame([
        {
            'Zona': zone,
            'Velocidade': athlete['zones'][zone]['speed'],
            'Pace': athlete['zones'][zone]['pace']
        }
        for zone in ['Z1', 'Z2', 'Z3', 'Z4']
    ])
    st.dataframe(zones_df, use_container_width=True)
    
    st.subheader("Seus Treinos da Semana")
    st.info("Treinos serão exibidos aqui quando o treinador planejar.")
    
else:
    st.title("193 Treinos")
    st.write("Bem-vindo ao sistema de planejamento de treinos!")
