from flask import Flask, jsonify, send_file, request

from image_processing.pre_processing import *
from image_processing.process_viga import *
from image_processing.decode import *
import io
from image_processing.detect import *
from image_processing.classify import *
from image_processing.interpret import *

app = Flask(__name__)



@app.route('/receive', methods=['GET','POST'])
def receive_image():
  
  #Retorna erro caso o parametro "foto" não seja recebido ou seja recebido vazio
  if not 'foto' in request.files or not request.files.get('foto'):
    return jsonify({'erro':'nenhum arquivo'}),400

  #Imagem recebida, na variavel "file"
  file = request.files.get('foto')

  #Imagem salva em variável estática "img"
  img = io.BytesIO()
  file.save(img)
  img.seek(0)

  #Imagem retornada, para fins de teste. Pode retornar simplesmente "sucesso" quando o código for finalizado
  return send_file(img,mimetype='image/png')


@app.route('/', methods=['GET'])

def get_info():
    try:
        image = cv2.imread('img/pontual_4_new.png')[:, :, ::-1]
        image = pre_processing(image)
        data = decode(image)
        viga = find_viga(data)
        viga_reta = find_reta(data)
        image = process_image(viga_reta, image)
        all_data = decode_all(image)
        apoio1, apoio2, pontual, distribuida, triangular = classify(all_data)

        viga_data = interpret_viga(viga)
        apoios_data = interpret_apoios(apoio1 + apoio2)
        triangulares_data = interpret_triangular(triangular)
        pontuais_data = interpret_pontual(pontual)
        distribuidas_data = interpret_distribuida(distribuida)
        tipo1 = {}
        tipo2 = {}
        tipo1["tipo"] = 0
        tipo2["tipo"] = 1
        apoios = []
        for a in apoio2:
            print(a)
            apoios.append([tipo2, {"posicao_i": a[3][0][0]}, {"posicao_f": a[3][2][0]}])
            apoios = copy.copy(apoios)
        for a in apoio1:
            apoios.append([tipo1, {"posicao_i": a[3][0][0]}, {"posicao_f": a[3][2][0]}])
            apoios = copy.copy(apoios)
        cargas_pontuais = []
        for c in pontuais_data:
            cargas_pontuais.append([{"posicao_i":c[1], "posicao_f":c[2], "modulo": c[0]}])

        cargas_distribuidas = []
        for c in distribuidas_data:
            cargas_distribuidas.append([{"posicao_i":c[1], "posicao_f":c[2], "modulo": c[0]}])

        cargas_triangulares = []
        for c in triangulares_data:
            print(c)
            cargas_triangulares.append([{"posicao_i":c[1], "posicao_f":c[2], "modulo": c[0]}])

        return jsonify(PosicaoViga = [{"inicial":viga_data[0]}, {"final": viga_data[1]}], apoios = apoios, cargasP = cargas_pontuais, cargasD = cargas_distribuidas, cargasT = cargas_triangulares)
    except:
        return "Erro ao extrair informações da viga."

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)