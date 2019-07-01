def classify(data):
    pontual = []
    distribuida = []
    triangular = []
    apoio1 = []
    apoio2 = []
    for d in data:
        if 'pontual' in str(d[0]):
            pontual.append(d)
        elif 'distr' in str(d[0]):
            distribuida.append(d)
        elif 'triang' in str(d[0]):
            triangular.append(d)
        elif 'apoio 1' in str(d[0]):
            apoio1.append(d)
        elif 'apoio 2' in str(d[0]):
            apoio2.append(d)
    return apoio1, apoio2, pontual, distribuida, triangular