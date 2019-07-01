def interpret_viga(viga):
    return [viga[0][0] + viga[0][2], viga[1][0]]


def interpret_distribuida(distribuida: list):
    forcas_distribuidas = []
    inicio = 0
    fim = 0
    if len(distribuida):
        if distribuida[0][2][0] > distribuida[1][2][0]:
            fim = distribuida[0][2][0] + distribuida[0][2][2]
            inicio = distribuida[1][2][0]
        else:
            fim = distribuida[1][2][0] + distribuida[1][2][2]
            inicio = distribuida[0][2][0]
        weight = str(distribuida[0][0]).replace("\'", "").split('w: ')
        forcas_distribuidas.append([int(weight[1]), inicio, fim])
    return forcas_distribuidas


def interpret_pontual(pontual):
    forcas_pontuais = []
    for p in pontual:
        weight = str(pontual[0][0]).replace("\'", "").split('w: ')
        forcas_pontuais.append([int(weight[1]), p[2][0], p[2][0] + p[2][2]])

    return forcas_pontuais


def interpret_triangular(triangular):
    triangular_10 = []
    triangular_6 = []
    triangular_3 = []
    forcas_triangulares = []
    for t in triangular:
        if 'w: 10' in str(t[0]):
            triangular_10.append(t[2])
        elif 'w: 6' in str(t[0]):
            triangular_6.append(t[2])
        elif 'w: 3' in str(t[0]):
            triangular_3.append(t[2])

    if len(triangular_10):
        mais_distante = 0
        mais_proximo = 0
        outro = 0
        width = 0
        mais_distante = max(triangular_10[0][0], triangular_10[1][0], triangular_10[2][0])
        mais_proximo = min(triangular_10[0][0], triangular_10[1][0], triangular_10[2][0])
        for t in triangular_10:
            if t[0] != mais_distante and t[0] != mais_proximo:
                outro = t[0]
            if t[0] == mais_distante:
                width = t[2]
        if abs(outro - mais_proximo) >= 50:
            forcas_triangulares.append([10, mais_proximo, mais_distante + width])
        else:
            forcas_triangulares.append([10, mais_distante + width, mais_proximo])

    if len(triangular_6):
        mais_distante = 0
        mais_proximo = 0
        outro = 0
        width = 0
        mais_distante = max(triangular_6[0][0], triangular_6[1][0], triangular_6[2][0])
        mais_proximo = min(triangular_6[0][0], triangular_6[1][0], triangular_6[2][0])
        for t in triangular_6:
            if t[0] != mais_distante and t[0] != mais_proximo:
                outro = t[0]
            if t[0] == mais_distante:
                width = t[2]
        if abs(outro - mais_proximo) >= 10:
            forcas_triangulares.append([6, mais_proximo, mais_distante + width])
        else:
            forcas_triangulares.append([6, mais_distante + width, mais_proximo])

    if len(triangular_3):
        mais_distante = 0
        mais_proximo = 0
        outro = 0
        width = 0
        mais_distante = max(triangular_3[0][0], triangular_3[1][0], triangular_3[2][0])
        mais_proximo = min(triangular_3[0][0], triangular_3[1][0], triangular_3[2][0])
        for t in triangular_3:
            if t[0] != mais_distante and t[0] != mais_proximo:
                outro = t[0]
            if t[0] == mais_distante:
                width = t[2]
        if abs(outro - mais_proximo) >= 10:
            forcas_triangulares.append([3, mais_proximo, mais_distante + width])
        else:
            forcas_triangulares.append([3, mais_distante + width, mais_proximo])

    return forcas_triangulares


def interpret_apoios(apoios):
    apoio_1 = []
    apoio_2 = []
    for a in apoios:
        if 'apoio 1' in str(a[0]):
            apoio_1.append([a[2][0], a[2][0] + a[2][2]])
        elif 'apoio 2' in str(a[0]):
            apoio_2.append([a[2][0], a[2][0] + a[2][2]])
    return apoio_1, apoio_2