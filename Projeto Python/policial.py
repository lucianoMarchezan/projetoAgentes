from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from pade.behaviours.protocols import FipaRequestProtocol
from pade.acl.messages import ACLMessage, AID
from casa import Casa, State, Matriz
from collections import deque
import requests
import random
import json
import pickle
import threading
import sys
from comunicacao import ComunicacaoServer
class ProcurarPolicial(TimedBehaviour):

    
    def __init__(self, agent, time):
        super(ProcurarPolicial, self).__init__(agent, time)
        mensagem = {
            "state": State.POLICIAL.value,
            "casaAtual": json.dumps(self.agent.casaAtual.returnJsonObject())
        }
        requests.post("http://localhost:9000/PosicaoInicial", json=mensagem)

    
    def on_time(self):
        super(ProcurarPolicial, self).on_time()
        display_message(self.agent.aid.localname, 'Pocial Decidindo!')

        if(self.agent.casaChamado != None):
            self.moverAteLocal()
        elif(not (len(self.agent.chamados) == 0)):
            casaNova = self.agent.chamados.popleft()
            self.agent.casaChamado = Casa(casaNova['linha'], casaNova['coluna'])
        else:
            display_message(self.agent.aid.localname, 'Esperando chamado!')

        
    def moverAteLocal(self):
        proximaCasa = self.escolherProximaCasa()

        if (proximaCasa != None and self.beliefVerificarCasa(proximaCasa)):
            requests.get("http://localhost:9000/PrenderIncendiario")
        if proximaCasa != None and self.verificarFimChamado(proximaCasa):
            self.agent.casaChamado = None 
        else:
            self.actionAndar(proximaCasa)
            display_message(self.agent.aid.localname, 'Movendo para!' + proximaCasa.nameId)


    def verificarFimChamado(self, proximaCasa):
        if(proximaCasa.linha == self.agent.casaChamado.linha):
            if(proximaCasa.coluna == self.agent.casaChamado.coluna):
                return True
        return False

    def actionAndar(self, proximaCasa):
        mensagem = {
            "tipoMensagem":"andar",
            "proximaCasa": json.dumps(proximaCasa.returnJsonObject()),
            "casaAtual": json.dumps(self.agent.casaAtual.returnJsonObject()),
            "state": State.POLICIAL.value
        }

        resposta = requests.post("http://localhost:9000/Andar", json=mensagem)

        if(resposta.text == "Movimento bem-sucedido!"):
            self.agent.casaAtual = proximaCasa               

    
    def beliefVerificarCasa(self, proximaCasa):
        mensagem = {
            "tipoMensagem":"verificarCasa",
            "mensagem": json.dumps(proximaCasa.returnJsonObject())
        }
        casa = requests.post("http://localhost:9000/VerificarCasa", json=mensagem)

        casa = json.loads(casa.content)

        if(casa['state'] == State.VAZIO.value):
            return False
        elif(casa['state'] == State.INCENDIARIO.value):
            return True

    def escolherProximaCasa(self):
        colunaCasaAtual = self.agent.casaAtual.coluna
        colunaCasaChamado = self.agent.casaChamado.coluna
        colunaProximaCasa = colunaCasaAtual
        linhaCasaAtual = self.agent.casaAtual.linha
        linhaCasaChamado = self.agent.casaChamado.linha
        linhaProximaCasa = linhaCasaAtual
        
        if(colunaCasaChamado - colunaCasaAtual < 0):
            colunaProximaCasa = colunaCasaAtual - 1
        elif(colunaCasaChamado - colunaCasaAtual > 0):
            colunaProximaCasa = colunaCasaAtual + 1
        elif(linhaCasaChamado - linhaCasaAtual < 0):
            linhaProximaCasa = linhaCasaAtual - 1
        elif(linhaCasaChamado - linhaCasaAtual > 0):
            linhaProximaCasa = linhaCasaAtual + 1

        return Casa(linhaProximaCasa, colunaProximaCasa)

class Policial(Agent):

    casaAtual = Casa(9,0)
    respondendoChamado = True #True para testar
    casaChamado = None
    comunicacao = None
    chamados = deque([])

    def __init__(self, aid, portC):
        super(Policial, self).__init__(aid=aid, debug=False)

        comp_temp = ProcurarPolicial(self,0.3)

        self.behaviours.append(comp_temp)

        self.comunicacao = ComunicacaoServer(portC)
        thread = threading.Thread(target=self.ligarServidor, args=())
        thread.start()

    
    def ligarServidor(self):
        while True:
            casa = self.comunicacao.ouvirCliente()
         
            if(casa not in self.chamados):
                self.chamados.append(casa)


    def getPort(self):
        return self.comunicacao.port

    def getHost(self):
        return self.comunicacao.host