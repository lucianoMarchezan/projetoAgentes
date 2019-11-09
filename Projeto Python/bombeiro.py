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

        if(self.agent.respondendoChamado):
            self.moverAteLocal()
        else:
            display_message(self.agent.aid.localname, 'Esperando chamado!')

        
    def moverAteLocal(self):
        proximaCasa = self.escolherProximaCasa()
        jsonCasa = json.dumps(proximaCasa.returnJsonObject())

        if (self.beliefVerificarCasa(proximaCasa)):
            requests.post("http://localhost:9000/ApagarFogo", json=jsonCasa)

        if self.verificarFimChamado(proximaCasa):
            self.agent.respondendoChamado = False
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

        if(casa['state'] == State.VAZIO.value):
            return False
        elif(casa['state'] == State.FOGO.value):
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

class Bombeiro(Agent):

    casaAtual = Casa(9,8)
    respondendoChamado = True #True para testar
    casaChamado = Casa(9,9)

    def __init__(self, aid):
        super(Bombeiro, self).__init__(aid=aid, debug=False)

        comp_temp = ResponderChamado(self,1.0)

        self.behaviours.append(comp_temp)
    
    
    def react(self, message):
        display_message("Bombeiro", "Recebi a mensagem")
        casa = pickle.loads(message.content)
        self.casaChamado = Casa(casa.linha, casa.coluna)
        self.respondendoChamado = True

    
        