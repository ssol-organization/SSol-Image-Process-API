from flask import Flask, jsonify, send_file, request
from os import environ 
from image_processing.decode import *
import io, base64
from PIL import Image
from image_processing.format import *
import cv2
import requests

app = Flask(__name__)



#global que guarda a imagem
stringIm = ""

@app.route('/receive', methods=['GET','POST'])
def receive_image():
  
  #Retorna erro caso o parametro "foto" não seja recebido ou seja recebido vazio
  if not 'foto' in request.files or not request.files.get('foto'):
    return jsonify({'erro':'nenhum arquivo'}),400
  
  #define que utilizaremos essa global
  global stringIm
  
  #recebe o arquivo
  file = request.files.get('foto')

  #Imagem salva em variável estática "img"
  img = io.BytesIO()
  file.save(img)
  img.seek(0)
   
  #grava a imagem na nossa variavel global em b64
  stringIm = base64.b64encode(img.read())

  return "Sucesso"


@app.route('/espreceive', methods=['GET','POST'])
def receive_esp():
  
  #define que utilizaremos essa global
  global stringIm

  if environ.get("espurl"):
    URL = environ.get("espurl") 
  else:
    URL = "https://www.skikelly.com/sf/liveview/?rand=123456789"
  
  #recebe a imagem
  response = requests.get(URL)
  img = Image.open(io.BytesIO(response.content))

  #Converte para JPG
  img.save('/tmp/temp.jpg')  
  pilImage = Image.open('/tmp/temp.jpg')
  
  #grava a imagem na nossa variavel global em b64
  buffered = io.BytesIO()
  pilImage.save(buffered, format="JPG")
  stringIm = base64.b64encode(buffered.getvalue())

  return "Sucesso"


@app.route('/current_image', methods=['GET'])
def see_image():
  
    global stringIm
    
    #Convertendo nossa string b64 para um arquivo de imagem

    imagemF = io.BytesIO(base64.b64decode(stringIm))

    imagemF.seek(0)    

    return send_file(imagemF, mimetype="image/jpg")  



@app.route('/', methods=['GET'])

def get_info():
    try:

        #conversão da string para imagem e salvamento em diretorio temporario para leitura posterior
        imagemF = io.BytesIO(base64.b64decode(stringIm))
        pilImage = Image.open(imagemF)
        pilImage.save('/tmp/current.jpg')
        
        image = cv2.imread('/tmp/current.jpg')
        #image = cv2.imread('img/capture (1) - boa.jpg')
        a1, a2, p, d, t = decode(image)
        apoios, cargas_p, cargas_d, cargas_t = format(a1, a2, p, d, t)
        return jsonify(apoios = apoios, cargasP = cargas_p, cargasD = cargas_d, cargasT = cargas_t)

    except:
        return "Erro ao extrair informações da viga."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)