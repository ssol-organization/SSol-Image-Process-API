import pyzbar.pyzbar as pyzbar
def decode(image):

    triangulares = []
    pontuais = []
    distribuidas = []
    apoios1 = []
    apoios2 = []

    all_data = pyzbar.decode(image)
    for qr in all_data:
        a = str(qr[0]).replace("b\'", '').replace("\'", '').split(', ')
        if 'apoio1' in a[0]:
            apoios1.append(a)
        elif 'apoio2' in a[0]:
            apoios2.append(a)
        elif 'triangular' in a[0]:
            triangulares.append(a)
        elif 'distribuida' in a[0]:
            distribuidas.append(a)
        elif 'pontual' in a[0]:
            pontuais.append(a)

    return apoios1, apoios2, pontuais, distribuidas, triangulares