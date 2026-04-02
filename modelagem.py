import math

def calcular_probabilidade_implicita(odd):
    try:
        return 1 / odd
    except ZeroDivisionError:
        return 0

def calcular_ev(odd, prob_real, stake=100):
    # EV = (Prob_Real * Lucro) - (Prob_Perda * Stake)
    lucro_potencial = stake * (odd - 1)
    prob_perda = 1 - prob_real
    return (prob_real * lucro_potencial) - (prob_perda * stake)

def calcular_poisson(media_esperada, gols):
    """Calcula a probabilidade de um time marcar exatamente 'x' gols"""
    return (math.exp(-media_esperada)* (media_esperada**gols)) /math.factorial(gols)

def estimar_probabilidade_vitoria(media_gols_time_a, media_gols_time_b):
    prob_vitoria_a = 0

    for gols_a in range(6):
        for gols_b in range(6):
            prob_placar = calcular_poisson(media_gols_time_a, gols_a) * calcular_poisson(media_gols_time_b, gols_b)

            if gols_a > gols_b:
                prob_vitoria_a += prob_placar

    return prob_vitoria_a