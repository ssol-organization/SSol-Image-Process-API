from flask import Flask, jsonify

import cv2
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_info(image):
    
    #codigos de visão computacional
    try:
        img = image
        w, h = img.shape[:2]
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
            cv2.line(img,(h-2,y1),(h-2,y1-20),(0,0,255),2)
        xi = 0
        xf = w
        yi = y1
        yf = y2
        detected = img
        return (detected[:,:,::-1])
    except:
        print("Erro na detecção da viga")

    #exemplos de informações geradas
    pos_viga = [xi, xf, yi, yf]
    """
    genApoio1 = 0;
    genApoio2 = 2;
    carga1 = 20;
    posicaoApoio1=4;
    """
    #retorna, em json, as informações adquiridas
    #return jsonify({"genApoio1": genApoio1, "genApoio2":genApoio2,"carga1":carga1,"posicaoApoio1":posicaoApoio1})
    return jsonify({"VigaPosition": pos_viga})


img = cv2.imread('img/viga400px.jpg')
get_info(img)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
