import json
from modelagem import calcular_probabilidade_implicita, calcular_ev, estimar_probabilidade_vitoria

# 1. Adicionamos a importação da nossa nova função da API
from api_client import buscar_odds_ao_vivo

def analisar_apostas(lista_de_jogos):
    resultados = []
    
    for jogo in lista_de_jogos:
        nome = jogo["nome"]
        odd = jogo["odd"]
        
        prob_real = estimar_probabilidade_vitoria(jogo["media_gols_casa"], jogo["media_gols_fora"])
        prob_implicita = calcular_probabilidade_implicita(odd)
        ev = calcular_ev(odd, prob_real)
        
        analise = {
            "nome": nome,
            "odd": odd,
            "prob_real": prob_real,
            "prob_implicita": prob_implicita,
            "ev": ev,
            "tem_valor": prob_real > prob_implicita
        }
        resultados.append(analise)
    
    return resultados

def extrair_dados_api(dados_brutos, casa_preferida='bet365'):
    jogos_limpos = []
    
    for evento in dados_brutos:
        time_casa = evento['home_team']
        time_fora = evento['away_team']
        nome_jogo = f"{time_casa} vs {time_fora}"
        
        try:
            odd_encontrada = 0
            # O código agora varre as casas de aposta procurando a Bet365
            for bookmaker in evento['bookmakers']:
                if bookmaker['key'] == casa_preferida:
                    # Achou a Bet365! Agora procura o mercado de vencedor da partida (h2h)
                    for market in bookmaker['markets']:
                        if market['key'] == 'h2h':
                            # Pega a odd da vitória do time da casa
                            for outcome in market['outcomes']:
                                if outcome['name'] == time_casa:
                                    odd_encontrada = outcome['price']
                                    break
                    break # Como já achamos a Bet365 e pegamos a odd, paramos de procurar
            
            # Se a Bet365 ofereceu odd para esse jogo, nós adicionamos na lista
            if odd_encontrada > 0:
                jogos_limpos.append({
                    "nome": nome_jogo,
                    "odd": odd_encontrada,
                    "media_gols_casa": 1.5, # Mantemos os fictícios por enquanto
                    "media_gols_fora": 1.1  # Mantemos os fictícios por enquanto
                })
        except (IndexError, KeyError):
            continue
            
    return jogos_limpos

# ==========================================
# --- PARTE ANTIGA (ARQUIVO LOCAL) DESLIGADA
# ==========================================
# try:
#     with open('jogos.json', 'r', encoding='utf-8') as arquivo:
#         jogos_do_dia = json.load(arquivo)
#
#     meus_resultados = analisar_apostas(jogos_do_dia)
#
#     print("\n--- RELATÓRIO DE APOSTAS ---")
#     for res in meus_resultados:
#         status = "VALOR" if res['tem_valor'] else "SEM VALOR"
#         print(f"{status} | {res['nome']} | Odd: {res['odd']:.2f} | Prob. Real: {res['prob_real']:.2%} | EV: R${res['ev']:.2f}")
#     print("----------------------------\n")
#
# except FileNotFoundError:
#     print("Erro: O arquivo 'jogos.json' não foi encontrado. Verifique se ele está na mesma pasta.")
# except json.JSONDecodeError:
#     print("Erro: O arquivo 'jogos.json' está formatado incorretamente.")


# ==========================================
# --- PARTE NOVA: TESTE DA API
# ==========================================
# ==========================================
# --- MOTOR PRINCIPAL: API + ANÁLISE
# ==========================================
print("Iniciando a busca na API...")
dados_da_api = buscar_odds_ao_vivo()

if dados_da_api:
    print("Dados recebidos! Processando...\n")
    
    # 1. Traduz o JSON gigante para a nossa listinha organizada
    jogos_formatados = extrair_dados_api(dados_da_api)
    
    # 2. Roda as suas fórmulas matemáticas!
    meus_resultados = analisar_apostas(jogos_formatados)
    
    # 3. Imprime o relatório final
    print("--- RELATÓRIO DE APOSTAS (AO VIVO) ---")
    for res in meus_resultados:
        status = "VALOR" if res['tem_valor'] else "SEM VALOR"
        print(f"{status} | {res['nome']} | Odd: {res['odd']:.2f} | Prob. Real: {res['prob_real']:.2%} | EV: R${res['ev']:.2f}")
    print("--------------------------------------")
else:
    print("\nFalha ao buscar dados na API.")