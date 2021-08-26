#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import random
from random import seed, randint

from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth
from pip._vendor import requests
import sys, socket


class dados:
    coordenador = False

    replicas_salvas = []
    historicoAcoes = []
    dadosTemporarios = dict()
    semente = 123456
    contas = [
        {
            'conta': 1234,
            'saldo': 100,
        },
        {
            'conta': 4345,
            'saldo': 50,
        },
        {
            'conta': 5678,
            'saldo': 250,
        },
    ]


    def __init__(self):
        pass

    def setReplicas(self, replicas):
        self.replicas_salvas = replicas

    def getReplicas(self):
        return self.replicas_salvas

    def setContas(self, contas):
        self.contas = contas

    def getContas(self):
        return self.contas

    def setCoordenador(self, boleano):
        self.coordenador = boleano

    def getCoordenador(self):
        return self.coordenador

    def setHistico(self, id, status):
        self.historicoAcoes.append({'id':id, 'status': status})

    def getHistico(self):
        return self.historicoAcoes

    def setDadosTemporario(self, id, acao):
        self.dadosTemporarios.update({id: acao})

    def removeDadoTemporario(self, id):
        del self.dadosTemporarios[id]

    def getDadosTemporario(self):
        return self.dadosTemporarios

    def setSemente(self, semente):
        self.semente = semente

    def getSemente(self):
        return self.semente


aux = dados()
auth = HTTPBasicAuth()

app = Flask(__name__)

livros = [
    {
        'id': 1,
        'titulo': 'Linguagem de Programacao C',
        'autor': 'Dennis Ritchie'
    },
    {
        'id': 2,
        'titulo': 'Java como programar',
        'autor': 'Deitel & Deitel'
    }
]


@app.route('/replicas', methods=['POST'])
def carregar_lista_replicas():
    if not request.json or not 'replicas' in request.json:
        abort(400)
    aux.setCoordenador(True)
    aux.setReplicas(request.json['replicas'])

    # livros.append(livro)
    return jsonify({'resultado': True}), 201


@app.route('/replicas', methods=['DELETE'])
def excluir_replicas():
    aux.setReplicas([])

    if len(aux.getReplicas()) != 0:
        abort(404)

    return jsonify({'resultado': True}), 200


@app.route('/replicas', methods=['GET'])
def listar_replicas():
    return jsonify(aux.getReplicas()), 200


@app.route('/contas', methods=['GET'])
def listar_contas():
    return jsonify(aux.getContas()), 200


@app.route('/historico', methods=['GET'])
def listar_historico():
    return jsonify(aux.getHistico()), 200


@app.route('/acoes', methods=['POST'])
def enviar_Acao():

    aux.setDadosTemporario(request.json['id'], request.json)

    if (aux.getCoordenador()):
        yes = 0
        no = 0
        ack = 0

        for resultado in aux.getReplicas():
            res = requests.post(resultado['endpoint'] + '/' + 'acoes', json=request.json)
            if (res.status_code == 200):
                yes = yes + 1
            elif (res.status_code == 403):
                no = no + 1
        if (yes == 2):
            persistirDados(aux.getDadosTemporario()[request.json['id']])
            aux.removeDadoTemporario(request.json['id'])
            for resultado in aux.getReplicas():
                res = requests.put(resultado['endpoint'] + '/' + 'decisao', json={'id': request.json['id']})
                if (res.status_code == 200):
                    ack = ack + 1
            if (ack == 2):
                aux.setHistico(request.json['id'], "success")
                return jsonify({'resultado': True}), 201
            else:
                aux.setHistico(request.json['id'], "fail")
                return jsonify({'resultado': False}), 403

        else:
            aux.removeDadoTemporario(request.json['id'])
            for resultado in aux.getReplicas():
                res = requests.delete(resultado['endpoint'] + '/' + 'decisao', json={'id': request.json['id']})
                if (res.status_code == 200):
                    ack = ack + 1
            if (ack == 2):
                aux.setHistico(request.json['id'], "fail")
                return jsonify({'resultado': False}), 403
            else:
                aux.setHistico(request.json['id'], "fail")
                return jsonify({'resultado': False}), 403
    else:
        prob = randint(0, 10)
        if (prob >= 3):
            return jsonify({'resultado': True}), 200
        else:
            return jsonify({'resultado': True}), 403


@app.route('/decisao', methods=['PUT', 'DELETE','POST'])
def enviar_decisao():
    if(aux.getCoordenador()):
        return jsonify({'resultado': False}), 404
    else:
        if(request.method == 'PUT'):
            validaAcao = persistirDados(aux.getDadosTemporario()[request.json['id']])
            aux.removeDadoTemporario(request.json['id'])
            if(validaAcao == 201):
                return jsonify({'resultado': True}), 200
            else:
                return jsonify({'resultado': True}), 403
        elif(request.method == 'DELETE'):
            aux.removeDadoTemporario(request.json['id'])
            return jsonify({'resultado': True}), 200
        else:
            return jsonify({'resultado': False}), 404


@app.route('/persistir', methods=['PUT', 'DELETE'])
def persistirDados(dados):
    resultado = [resultado for resultado in aux.getContas() if resultado['conta'] == dados['conta']]
    if len(resultado) == 0:
        abort(404)
    if not dados:
        abort(400)
    if 'conta' in dados and type(dados['conta']) != int:
        abort(400)
    if 'operacao' in dados and type(dados['operacao']) is not str:
        abort(400)
    if 'valor' in dados and type(dados['valor']) is not float:
        abort(400)

    if (dados['operacao'] == 'debito'):
        if ((resultado[0]['saldo'] - dados['valor']) > 0):
            resultado[0]['saldo'] = (resultado[0]['saldo'] - dados['valor'])
            return 201
        else:
            return 403
    elif (dados['operacao'] == 'credito'):
        resultado[0]['saldo'] = resultado[0]['saldo'] + dados['valor']
        return 201



@app.route('/semente', methods=['POST'])
def carregar_semente():
    aux.setSemente(request.json['seed'])

    return jsonify({'resultado': True}), 201

@app.route('/teste', methods=['get'])
def teste():
    res = requests.get('http://localhost:5000/acoes')
    if (res.status_code == 200):
        print("200")
    elif (res.status_code == 403):
        print("403")

    return jsonify({'resultado': True}), 200


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'erro': 'Acesso Negado'}), 403)


# Para apresentar erro 404 HTTP se tentar acessar um recurso que nao existe
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'erro': 'Recurso Nao encontrado'}), 404)


if __name__ == "__main__":

    if (len(sys.argv) <= 2):
            print("Informe hostName e port")
    else:
        port = sys.argv[1]
        hostName = sys.argv[2]

    print("Servidor no ar!")
    #app.run(port=5000, host="127.0.0.1")
    app.run(port=port, host=socket.gethostbyname(hostName), debug=True)
