#!coding=utf-8
# Hello world temporal in Pade!

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from sys import argv
import threading
import socket
import requests
import random
import sys
import json
from casa import Casa, State, Matriz
import pickle


class ComportTemporal(TimedBehaviour):
    def __init__(self, agent, time):
        super(ComportTemporal, self).__init__(agent, time)

    def on_time(self):
        super(ComportTemporal, self).on_time()
        proximaCasa = self.desireAndarProximaCasa()

        while(self.beliefVerificarCasa(proximaCasa)):
            proximaCasa = self.desireAndarProximaCasa()


        casaBytes = pickle.dumps(proximaCasa.returnJsonObject())

        display_message(self.agent.aid.localname,
                        'Incendiario andando para '+proximaCasa.nameId)

        tacar_fogo = random.randint(1,100)
        if tacar_fogo < 40:
            self.actionIncendiar(self.agent.casaAtual)

        self.actionAndar(proximaCasa)

    def geraPosicaoCasa(self, proximaCasa):
        linha = proximaCasa.linha
        coluna = proximaCasa.coluna
        return ""+str(linha)+str(coluna)

    def desireAndarProximaCasa(self):
        linha = self.agent.casaAtual.linha
        coluna = self.agent.casaAtual.coluna
        proximaLinha = random.randint(-1, 1) + linha
        proximaColuna = random.randint(-1, 1) + coluna
        colunas = Matriz.COLUNAS.value
        linhas = Matriz.LINHAS.value

        while ((proximaLinha == linha) and (proximaColuna==coluna)) or ((proximaColuna  >= colunas) or (proximaLinha >= linhas)):
            proximaLinha = random.randint(-1, 1) + linha
            proximaColuna = random.randint(-1, 1) + coluna
    

        return Casa(proximaLinha, proximaColuna)

    def beliefVerificarCasa(self, proximaCasa):

        mensagem = {
            "tipoMensagem": "verificarCasa",
            "mensagem": json.dumps(proximaCasa.returnJsonObject())
        }
        casa = requests.post(
            "http://localhost:9000/VerificarCasa", json=mensagem)

        casa = json.loads(casa.content)

        if(casa['state'] == State.VAZIO.value):
            return False
        else:
            return True

    def actionAndar(self, proximaCasa):

        mensagem = {
            "tipoMensagem": "andar",
            "proximaCasa": json.dumps(proximaCasa.returnJsonObject()),
            "casaAtual": json.dumps(self.agent.casaAtual.returnJsonObject()),
            "state": State.INCENDIARIO.value
        }

        resposta = requests.post(
            "http://localhost:9000/Andar", json=mensagem)

        if(resposta.text == "Movimento bem-sucedido!"):
            self.agent.casaAtual = proximaCasa

    def actionIncendiar(self, proximaCasa):
        
        display_message(self.agent.aid.localname, 'Botando Fogo na casa ' + proximaCasa.nameId)
        mensagem = {
            "tipoMensagem": "mudaCor",
            "mensagem": self.geraPosicaoCasa(proximaCasa)
        }

        r = requests.post("http://localhost:9000/Incendiario", json=mensagem)


class Incendiario(Agent):

    linha = random.randint(0, 9)
    coluna = random.randint(0, 9)
    casaAtual = Casa(linha, coluna)

    def __init__(self, aid):
        super(Incendiario, self).__init__(aid=aid, debug=False)

        comp_temp = ComportTemporal(self, 1.0)

        self.behaviours.append(comp_temp)

    def react(self, message):
        display_message(self.aid.localname, 'Mensagem recebida')
        if(message == "Processo Morto"):
            sys.exit()
