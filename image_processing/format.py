import copy

def format(apoio1, apoio2, pontuais_data, distribuidas_data, triangulares_data):

    apoios = []
    for a in apoio2:
        apoios.append([1, {"posicao": a[1]}])
        apoios = copy.copy(apoios)

    for a in apoio1:
        apoios.append([0, {"posicao": a[1]}])
        apoios = copy.copy(apoios)

    cargas_pontuais = []
    for c in pontuais_data:
        cargas_pontuais.append([{"posicao": c[1], "modulo": c[2]}])

    cargas_distribuidas = []
    for c in distribuidas_data:
        cargas_distribuidas.append([{"posicao_i": c[1], "posicao_f": c[2], "modulo": c[3]}])

    cargas_triangulares = []
    for c in triangulares_data:
        cargas_triangulares.append([{"posicao_i": c[1], "posicao_f": c[2], "modulo": c[3]}])

    return apoios, cargas_pontuais, cargas_distribuidas, cargas_triangulares