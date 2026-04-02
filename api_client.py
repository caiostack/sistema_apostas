import requests

API_KEY = '3792b062aebdb2d4b712e4067a00ea7a' 
SPORT = 'soccer_brazil_campeonato' 
REGIONS = 'eu' 
MARKETS = 'h2h' 

URL = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}'

def buscar_odds_ao_vivo():
    """Conecta na API e retorna os dados das odds em formato JSON."""
    try:
        print("Conectando à API para buscar as odds...")
        response = requests.get(URL)
        
        response.raise_for_status() 
        
        dados_json = response.json()
        return dados_json
        
    except requests.exceptions.RequestException as erro:
        print(f"Erro ao conectar com a API: {erro}")
        return None