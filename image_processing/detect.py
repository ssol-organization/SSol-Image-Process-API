import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import copy

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
        cv2.line(img, (x1, y1 + 25), (x2, y2 + 25), (0, 0, 255), 2)
        cv2.line(img, (2, y1), (2, y1 + 25), (0, 0, 255), 2)
        cv2.line(img, (h - 2, y1), (h - 2, y1 + 25), (0, 0, 255), 2)
    # demarcação da viga
    xi = 0
    xf = w
    yi = y2
    yf = y2 + int(h/12)


    return [xi, xf, yi, yf]

def detect_viga_colors(img, xi, xf, yi, yf):
    h, w = img.shape[:2]
    i = 0
    colors_viga = {}
    while i < (w - 2):
        color = [abs(int(img[yi - 10][i + 1][0])), abs(int(img[yi - 10][i + 1][1])),
                 abs(int(img[yi - 10][i + 1][2]))]
        dif0 = abs(abs(int(img[yi - 10][i][0])) - abs(int(img[yi - 10][i + 1][0])))
        dif1 = abs(abs(int(img[yi - 10][i][1])) - abs(int(img[yi - 10][i + 1][1])))
        dif2 = abs(abs(int(img[yi - 10][i][2])) - abs(int(img[yi - 10][i + 1][2])))
        if ((dif0 >= 60 and dif1 >= 60) or (dif0 >= 60 and dif2 >= 60) or (dif1 >= 60 and dif2 >= 60)):
            colors_viga[int(i)] = color
            i+=5
        i += 1
    return colors_viga

def detect_qr_codes(qrcode, ranges):
    cut = {}
    data = []
    h, w = qrcode.shape[:2]
    our_ranges = [0] + ranges + [w-1]+[-1]
    position = 0
    for r in range(0, len(our_ranges) - 1):
        qr = copy.copy(qrcode)
        for i in range(0, w):
            if (i < our_ranges[position] or i > our_ranges[position + 1]):
                for j in range(0, h):
                    qr[j][i] = 0, 0, 0
        decodedObjects = pyzbar.decode(qr)
        if decodedObjects == []:
            data = []
        else:
            for code in decodedObjects:
                text = str(code[0])[2:2] + str(code[0])[2:]
                data.append(str(text)[:-1])
        cut[our_ranges[position]] = data
        print(our_ranges[position])
        data = []
        position += 1

    return cut