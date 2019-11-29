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
from comunicacao import ComunicacaoServer
class ResponderChamado(TimedBehaviour):

    
    def __init__(self, agent, time):
        super(ResponderChamado, self).__init__(agent, time)
        mensagem = {
            "state": State.BOMBEIRO.value,
            "casaAtual": json.dumps(self.agent.casaAtual.returnJsonObject())
        }
        requests.post("http://localhost:9000/PosicaoInicial", json=mensagem)

    
    def on_time(self):
        super(ResponderChamado, self).on_time()
        display_message(self.agent.aid.localname, 'Bombeiro Decidindo!')

        if(self.agent.casaChamado != None):
            self.moverAteLocal()
        elif(not (len(self.agent.chamados) == 0)):
            casaNova = self.agent.chamados.popleft()
            self.agent.casaChamado = Casa(casaNova['linha'], casaNova['coluna'])
        else:
            display_message(self.agent.aid.localname, 'Esperando chamado!')

        
    def moverAteLocal(self):
        proximaCasa = self.escolherProximaCasa()
        casaBytes = pickle.dumps(proximaCasa.returnJsonObject())
        estadoProximaCasa = self.beliefVerificarCasa(proximaCasa)

        if(estadoProximaCasa == "Incendiario"):
            self.agent.mandarMensagem(self.agent.policial.getPort(), self.agent.policial.getHost(), casaBytes)
            display_message(self.agent.aid.localname, 'Bombeiro chamou policia')
        elif(estadoProximaCasa == "Fogo"):
            requests.post("http://localhost:9000/ApagarFogo", json=proximaCasa.returnJsonObject())
            display_message(self.agent.aid.localname, 'Apagando fogo!')
        else:
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
            "state": State.BOMBEIRO.value
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

        return casa['state']

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

class Bombeiro(Agent):

    casaAtual = Casa(9,8)
    respondendoChamado = True #True para testar
    casaChamado = None
    comunicacao = None
    chamados = deque([])

    def __init__(self, aid, portC):
        super(Bombeiro, self).__init__(aid=aid, debug=False)

        comp_temp = ResponderChamado(self,0.4)

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

    
        