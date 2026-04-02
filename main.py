import json
from modelagem import calcular_probabilidade_implicita, calcular_ev, estimar_probabilidade_vitoria

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


try:
    # 1. O Python abre o arquivo JSON no modo leitura ('r' = read)
    with open('jogos.json', 'r', encoding='utf-8') as arquivo:
        jogos_do_dia = json.load(arquivo)

    # 2. Manda os dados lidos para o nosso motor de cálculos
    meus_resultados = analisar_apostas(jogos_do_dia)

    # 3. Exibe o relatório
    print("\n--- RELATÓRIO DE APOSTAS ---")
    for res in meus_resultados:
        status = "VALOR" if res['tem_valor'] else "SEM VALOR"
        print(f"{status} | {res['nome']} | Odd: {res['odd']:.2f} | Prob. Real: {res['prob_real']:.2%} | EV: R${res['ev']:.2f}")
    print("----------------------------\n")

except FileNotFoundError:
    print("Erro: O arquivo 'jogos.json' não foi encontrado. Verifique se ele está na mesma pasta.")
except json.JSONDecodeError:
    print("Erro: O arquivo 'jogos.json' está formatado incorretamente.")
