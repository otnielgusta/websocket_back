import time

from flask import Flask
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class Mensagem:
  pessoa_nome:str
  id_pessoa:str
  id_mensagem:str
  texto:str

  def __init__(self, pessoa_nome, id_pessoa, id_mensagem, texto):
    self.pessoa_nome=pessoa_nome
    self.id_pessoa=id_pessoa
    self.id_mensagem=id_mensagem
    self.texto=texto

  @staticmethod
  def from_dict(json):
    return Mensagem(
      pessoa_nome=json.get("pessoa_nome"),
      id_pessoa=json.get("id_pessoa"),
      id_mensagem=json.get("id_mensagem"),
      texto=json.get("texto")
    )

  def to_json(self):
    return {
      "pessoa_nome": self.pessoa_nome,
      "id_pessoa": self.id_pessoa,
      "id_mensagem": self.id_mensagem,
      "texto": self.texto
    }


class Conversa:
  pessoa1:int
  pessoa2:int
  conversa:list[Mensagem] = []

# Define uma ação para ser executada quando um evento 'message' é recebido
@socketio.on('message')
def handle_message(data):
    print(data)
    mensagem = Mensagem.from_dict(data.get("mensagem"))
    pessoa = data.get("pessoa")
    Conversa.conversa.append(mensagem)
    if pessoa != mensagem.id_pessoa:
      resposta = mensagem.to_json()
      emit('getMessage', resposta, json=True)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    send(json, json=True)


if __name__ == '__main__':
  socketio.run(app)
