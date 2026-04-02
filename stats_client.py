import requests

API_KEY = 'SUA_CHAVE_AQUI'
def testar_conexao_estatisticas():
    url = "https://v3.football.api-sports.io/status"
    
    headers = {
        'x-apisports-key': API_KEY
    }
    
    try:
        print("--- PASSO 1: TESTE DE CONEXÃO ---")
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        dados = response.json() 
        
        if not dados.get('errors'):
            print("✅ Conexão bem-sucedida! Sua conta está ativa.")
            # O campo correto para ver requisições usadas é 'requests'
            try:
                usadas = dados['response']['requests']['current']
                total = dados['response']['requests']['limit_day']
                print(f"Requisições: {usadas}/{total} hoje.")
            except:
                print("Limite de requisições: Ok.")
            return True
        else:
            print(f"❌ Erro na API: {dados.get('errors')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def buscar_estatisticas_time(team_id, league_id, season=2025): 
    """
    Busca médias de gols. 
    Usa 2025 por padrão para garantir que haja dados consolidados.
    """
    url = "https://v3.football.api-sports.io/teams/statistics"
    querystring = {"league": str(league_id), "season": str(season), "team": str(team_id)}
    
    headers = {
        'x-apisports-key': API_KEY 
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        dados = response.json()
        
        # O "ESCUDO": Verifica se a API retornou dados reais ou uma lista vazia/erro
        if not dados.get('response') or isinstance(dados['response'], list) or not dados['response'].get('goals'):
            print(f"⚠️ Aviso: Sem dados para o time {team_id} na liga {league_id} (Temporada {season}).")
            return None
        
        # Extração segura das médias de gols marcados (for)
        media_gols_casa = dados['response']['goals']['for']['average']['home']
        media_gols_fora = dados['response']['goals']['for']['average']['away']
        
        return {
            "media_casa": float(media_gols_casa),
            "media_fora": float(media_gols_fora)
        }
        
    except Exception as e:
        print(f"❌ Erro ao processar dados do time {team_id}: {e}")
        return None

# Bloco de teste: Roda apenas se você executar o stats_client.py diretamente
if __name__ == "__main__":
    if testar_conexao_estatisticas():
        print("\n--- PASSO 2: TESTE DE BUSCA REAL ---")
        # Mudamos para 2023, que é o ano garantido que testamos mais cedo!
        print(f"Buscando médias do Flamengo em 2023...")
        stats = buscar_estatisticas_time(team_id=127, league_id=71, season=2023)
        
        if stats:
            print(f"✅ Média Casa: {stats['media_casa']}")
            print(f"✅ Média Fora: {stats['media_fora']}")
        else:
            print("Não foi possível obter os dados do time.")