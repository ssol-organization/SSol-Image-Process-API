import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

def detect_viga(img):
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 50)
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.line(img, (x1, y1 - 20), (x2, y2 - 20), (0, 0, 255), 2)
        cv2.line(img, (2, y1), (2, y1 - 20), (0, 0, 255), 2)
        cv2.line(img, (w - 2, y1), (w - 2, y1 - 20), (0, 0, 255), 2)
    # demarcação da viga
    xi = 0
    xf = w
    yi = y2
    yf = y2 - 20
    return [xi, xf, yi, yf]

def detect_viga_colors(img, xi, xf, yi, yf):
    h, w = img.shape[:2]
    i = 1
    colors_viga = {}
    while i < (w - 4):
        color = [abs(int(img[yi - 10][i + 1][0])), abs(int(img[yi - 10][i + 1][1])),
                 abs(int(img[yi - 10][i + 1][2]))]
        dif0 = abs(abs(int(img[yi - 10][i][0])) - abs(int(img[yi - 10][i + 1][0])))
        dif1 = abs(abs(int(img[yi - 10][i][1])) - abs(int(img[yi - 10][i + 1][1])))
        dif2 = abs(abs(int(img[yi - 10][i][2])) - abs(int(img[yi - 10][i + 1][2])))
        if ((dif0 >= 8 and dif1 >= 8) or (dif0 >= 8 and dif2 >= 8) or (dif1 >= 8 and dif2 >= 8)):
            colors_viga[str(i)] = color
            i += 5
        i += 1
    return colors_viga

def detect_qr_codes(qrcode):
    decodedObjects = pyzbar.decode(qrcode)
    # Print results
    data = []
    for obj in decodedObjects:
        text = str(obj.data)[2:2] + str(obj.data)[2:]
        data.append(str(text)[:-1])
    return data
