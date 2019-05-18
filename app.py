from flask import Flask, jsonify

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar

app = Flask(__name__)

@app.route('/', methods=['GET'])

def get_info():
    try:
        #a leitura da imagem deve ser substituída pela imagem que será enviada como parâmetro
        image = cv2.imread('img/viga400px.jpg')
        #codigos de visão computacional:
            #encontrando retas
        pos_viga = []
        colors_viga = {}
        img = image
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        lines = cv2.HoughLines(edges,1,np.pi/180,50)
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.line(img,(x1,y1-20),(x2,y2-20),(0,0,255),2)
            cv2.line(img,(2,y1),(2,y1-20),(0,0,255),2)
            cv2.line(img,(w-2,y1),(w-2,y1-20),(0,0,255),2)
        #demarcação da viga
        xi = 0
        xf = w
        yi = y2
        yf = y2-20
        pos_viga.append(xi)
        pos_viga.append(xf)
        pos_viga.append(yi)
        pos_viga.append(yf)

        #detecção de cores:

        img2 = img[:,:,::-1]
        #serão necessárias alterações a depender das cores que serão utilizadas na viga
        i = 1
        while i < (w-4):
            color = [abs(int(img2[y1-10][i+1][0])), abs(int(img2[y1-10][i+1][1])), abs(int(img2[y1-10][i+1][2]))]
            dif0 = abs(abs(int(img2[y1-10][i][0])) - abs(int(img2[y1-10][i+1][0])))
            dif1 = abs(abs(int(img2[y1-10][i][1])) - abs(int(img2[y1-10][i+1][1])))
            dif2 = abs(abs(int(img2[y1-10][i][2])) - abs(int(img2[y1-10][i+1][2])))
            if((dif0 >= 8 and dif1 >= 8)  or (dif0 >= 8 and dif2 >= 8) or (dif1 >= 8 and dif2 >= 8)):
                colors_viga[str(i)] = color
                i+=5
            i+=1

        qrcode = cv2.imread("img/5.png")
        # Find barcodes and QR codes
        decodedObjects = pyzbar.decode(qrcode)
        
        # Print results
        data = []
        for obj in decodedObjects:
            data.append(obj.data)
        
        
        return jsonify(ImageSize = [w, h], VigaPosition = pos_viga, ColorsRGB = colors_viga, QRCodes = data)
    except:
        return "Erro ao extrair informações da viga."

    #exemplos de informações geradas
    

    #genApoio1 = 0;
    #genApoio2 = 2;
    #carga1 = 20;
    #posicaoApoio1=4;

    #retorna, em json, as informações adquiridas
    #return jsonify({"genApoio1": genApoio1, "genApoio2":genApoio2,"carga1":carga1,"posicaoApoio1":posicaoApoio1})
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
