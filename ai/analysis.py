import ollama

def generate_summary(match_time, total_time, start_time, courts):

    summary = f"""
        Tenho um torneio de ténis de pares mistos. Tenho {courts} campos disponíveis e cada jogo demora
        {match_time} minutos num total de {total_time} minutos por campo. Os jogos começam às {start_time}.
        As regras aplicadas foram:
        - nenhum jogador pode estar em mais do que um campo ao mesmo tempo
        - nenhum jogador pode estar nas duas dupla no mesmo jogo 
        - evitar tanto quanto possível repetir parceiros e adversários
        - tentar tanto quanto possível que todos os jogadores joguem o mesmo número de jogos
        - campos sem jogos são assinalados com um '—'
    """
    return summary


def print_games(games):
    lines = []
    for game in games:
        court = game.get("Campo", "—")
        time = game.get("Hora", "—")
        dupla1 = game.get("Dupla 1", "—")
        dupla2 = game.get("Dupla 2", "—")

        lines.append(f"Campo: {court} | Hora: {time} | Dupla 1: {dupla1} | Dupla 2: {dupla2}")
    return lines

def analysis_with_ai(summary, schedule_summary):
    prompt = f"""
    
    {summary}
    
    O calendário de jogos é o seguinte:
    
    {schedule_summary}
    
    Faz uma análise e destaca os seguintes pontos:
    - Quem jogou menos que a média de jogos
    - Quem jogou mais que a média de jogos
    - Que jogadores têm jogos consecutivos e se são em campos diferentes
    - Que Jogadores não fizeram nenhum jogo
    - Houve algum campo que não teve qualquer jogo

    Dá a resposta em português de forma clara e estruturada.
    """

    output = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return output['message']['content'], prompt
