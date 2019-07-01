def find_viga(data):
    viga = [[], []]
    for d in data:
        if 'viga inicio' in str(d[0]):
            viga[0] = d[2]
        elif 'viga fim' in str(d[0]):
            viga[1] = d[2]
    return viga

def find_reta(data):
    viga = [[], []]
    for d in data:
        if 'viga inicio' in str(d[0]):
            viga[0] = d[3]
        elif 'viga fim' in str(d[0]):
            viga[1] = d[3]
    return viga