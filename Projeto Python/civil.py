from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage, AID
from casa import Casa, State, Matriz
import requests
import random
import json
import pickle
import socket

class Passear(TimedBehaviour):

    
    def __init__(self, agent, time):
        super(Passear, self).__init__(agent, time)

    
    def on_time(self):
        super(Passear, self).on_time()
        display_message(self.agent.aid.localname, 'Civil Decidindo!')
        proximaCasa = self.desireAndarProximaCasa()
        casaBytes = pickle.dumps(proximaCasa.returnJsonObject())
        
        if(self.beliefVerificarCasa(proximaCasa)):
            display_message(self.agent.aid.localname, 'Civil andando!')
            self.actionAndar(proximaCasa)
            display_message(self.agent.aid.localname, proximaCasa.nameId)
        else:
            self.agent.mandarMensagem(self.agent.bombeiro.getPort(), self.agent.bombeiro.getHost(), casaBytes)
            display_message(self.agent.aid.localname, 'FOOOOGOOOOOOOO!')
        


    def desireAndarProximaCasa(self):
        linha = self.agent.casaAtual.linha
        coluna = self.agent.casaAtual.coluna
        proximaLinha = 0
        proximaColuna = 0
        colunas = Matriz.COLUNAS.value
        linhas = Matriz.LINHAS.value

        if(coluna + 1 >= colunas):#Quando a linha tiver acabado
            if(not (linha + 1 >= linhas)):#Quando o cenário não tiver acabado
                proximaLinha = linha + 1
        else:
            proximaColuna = coluna + 1
            proximaLinha = linha
                

        return Casa(proximaLinha, proximaColuna)

    
    #Verifica a situação da próxima casa
    def beliefVerificarCasa(self, proximaCasa):
        mensagem = {
            "tipoMensagem":"verificarCasa",
            "mensagem": json.dumps(proximaCasa.returnJsonObject())
        }
        casa = requests.post("http://localhost:9000/VerificarCasa", json=mensagem)

        casa = json.loads(casa.content)

        if(casa['state'] == State.INCENDIARIO.value):
            return False
        elif(casa['state'] == State.FOGO.value):
            return False
        else:
            return True

    def actionAndar(self, proximaCasa):
        mensagem = {
            "tipoMensagem":"andar",
            "proximaCasa": json.dumps(proximaCasa.returnJsonObject()),
            "casaAtual": json.dumps(self.agent.casaAtual.returnJsonObject()),
            "state": State.CIVIL.value
        }

        resposta = requests.post("http://localhost:9000/Andar", json=mensagem)

        if(resposta.text == "Movimento bem-sucedido!"):
            self.agent.casaAtual = proximaCasa


class Civil(Agent):

    casaAtual = Casa(9,9)
    bombeiro = None

    def __init__(self, aid, bombeiro):
        super(Civil, self).__init__(aid=aid, debug=False)

        self.bombeiro = bombeiro

        comp_temp = Passear(self, 1.0)

        self.behaviours.append(comp_temp)

    
    def mandarMensagem(self, port, host, casa):
        s = socket.socket()
        s.connect((host, port))
        s.send(casa)
        s.close()