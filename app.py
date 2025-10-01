import itertools
import random
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from ai.analysis import analysis_with_ai, generate_summary, print_games
from logic.scheduler import schedule_games
from logic.stats import count_doubles_by_player, count_duels_by_player
from logic.utils import generate_doubles_matrix, generate_opponents_matrix

st.title("🎾 Tennis Match Scheduler")

# Player inputs
players_input = st.text_area("Nomes dos jogadores (um por linha)").splitlines()
players = [p.strip() for p in players_input if p.strip()]

# Validate duplicates
duplicates = set([nome for nome in players if players.count(nome) > 1])

# Time and court inputs
col1, col2, col3, col4 = st.columns(4)
with col1:
    match_time = st.number_input("⏱️ Duração de cada jogo (minutos)", min_value=15, max_value=180, value=15, step=5)
with col2:
    total_time = st.number_input("🕒 Tempo total por campo (minutos)", min_value=match_time, max_value=720, value=180, step=10)
with col3:
    start_time_input = st.time_input("🕰️ Escolha a hora de início dos jogos", value=datetime.strptime("18:00", "%H:%M").time())
with col4:
    courts = st.number_input("🔖 Número de campos disponíveis", min_value=1, max_value=7, value=3)

# Convert start_time_input to datetime
start_time = datetime.combine(datetime.today(), start_time_input)

# Schedule Section
st.header("📅 Gerar calendário de jogos")

if len(players) < 4:
    st.warning("Tens de introduzir pelo menos 4 jogadores.")
else:
    if duplicates:
        st.warning(f"Nomes duplicados encontrados: {', '.join(duplicates)}")
    else:
        if st.button("Gerar Calendário"):

            st.write(f"Total de jogadores: {len(players)}")

            # Clean AI state
            st.session_state['ai_analysis'] = None

            # Create all possible doubles
            duplas = list(itertools.combinations(players, 2))

            # Create all possible matches (avoiding repeating the same player in each double)
            matches = []
            for d1, d2 in itertools.combinations(duplas, 2):
                if set(d1).isdisjoint(d2):
                    matches.append((d1, d2))
            random.shuffle(matches)

            # Create available slots
            slots_by_court = total_time // match_time
            total_slots = slots_by_court * courts
            slots = []
            for slot_index in range(total_slots):
                court = (slot_index % courts) + 1
                time_in_mins = (slot_index // courts) * match_time
                time = start_time + timedelta(minutes=time_in_mins)
                slots.append((court, f"{time.strftime('%H:%M')}"))
            schedule, games_by_player = schedule_games(matches, slots)

            st.session_state['schedule'] = schedule
            st.session_state['games_by_player'] = games_by_player
            st.session_state['players'] = players

# If schedule is visible
if 'schedule' in st.session_state:

    schedule = st.session_state['schedule']
    games_by_player = st.session_state['games_by_player']

    # Show schedule
    df_agenda = pd.DataFrame(schedule)
    st.dataframe(df_agenda)

    # show number of games for each player
    games_counter_toggle = st.toggle("🤝 Número de jogos que cada jogador fez")
    if games_counter_toggle:
        df_counter = pd.DataFrame(
            sorted(
                [(j, games_by_player.get(j, 0)) for j in players],
                key=lambda x: x[0]
            ),
            columns=["Jogador", "Nº de Jogos"]
        )
        st.dataframe(df_counter)

    # show number of games with each partner
    show_doubles_toggle = st.toggle("🤝 Número de vezes que jogadores fizeram dupla entre si")
    if show_doubles_toggle:
        doubles = count_doubles_by_player(schedule)
        doubles_matrix = generate_doubles_matrix(doubles, players)
        st.dataframe(doubles_matrix)

    # show number of games against each player
    show_duels_toggle = st.toggle("⚔️ Número de vezes que jogadores jogaram um contra o outro")
    if show_duels_toggle:
        duels = count_duels_by_player(schedule)
        duels_matrix = generate_opponents_matrix(duels, players)
        st.dataframe(duels_matrix)

# AI Section
if 'schedule' in st.session_state:
    st.header("🤖 Análise da agenda com IA")

    schedule = st.session_state['schedule']
    players = st.session_state['players']

    if st.button("Analisar com IA"):
        with st.spinner("A IA está a analisar..."):
            summary = generate_summary(match_time, total_time, start_time, courts)
            summary_games = print_games(schedule)
            analysis, prompt = analysis_with_ai(summary, summary_games)
            #st.write(prompt)
        st.session_state['ai_analysis'] = analysis

    if 'ai_analysis' in st.session_state and st.session_state['ai_analysis'] is not None:
        st.markdown("### 🧠 Resumo da IA")
        st.markdown(st.session_state['ai_analysis'])
