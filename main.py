from modelagem import calcular_probabilidade_implicita, calcular_ev

def analisar_apostas(lista_de_jogos):
    resultados = []
    
    for jogo in lista_de_jogos:
        nome = jogo["nome"]
        odd = jogo["odd"]
        prob_real = jogo["prob_real"]
        
        prob_implicita = calcular_probabilidade_implicita(odd)
        ev = calcular_ev(odd, prob_real)
        
        # resultado guardados em um dicionário para fácil acesso posterior
        analise = {
            "nome": nome,
            "odd": odd,
            "prob_implicita": prob_implicita,
            "ev": ev,
            "tem_valor": prob_real > prob_implicita
        }
        resultados.append(analise)
    
    return resultados

# Simulação dos dados
apostas = [
    {"nome": "Time A vs Time B", "odd": 2.10, "prob_real": 0.55},
    {"nome": "Time C vs Time D", "odd": 1.80, "prob_real": 0.50},
    {"nome": "Time E vs Time F", "odd": 3.00, "prob_real": 0.40},
]

# Execução e Exibição
meus_resultados = analisar_apostas(apostas)

for res in meus_resultados:
    status = "VALOR" if res['tem_valor'] else "SEM VALOR"
    print(f"[{status}] {res['nome']} | Odd: {res['odd']} | EV: R${res['ev']:.2f}")
