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

class ComportTemporal(TimedBehaviour):
    def __init__(self, agent, time):
        super(ComportTemporal, self).__init__(agent, time)

    def on_time(self):
        super(ComportTemporal, self).on_time()
        display_message(self.agent.aid.localname, 'Botando Fogo!')
        mensagem = {
            "tipoMensagem":"mudaCor",
            "mensagem":self.geraPosicaoCasa()
        }
        r = requests.post("http://localhost:9000/AgenteTeste", json=mensagem)

    def geraPosicaoCasa(self):
        linha = random.randint(0,9)
        coluna = random.randint(0,9)
        return ""+str(linha)+str(coluna)


class AgenteHelloWorld(Agent):

    def __init__(self, aid):
        super(AgenteHelloWorld, self).__init__(aid=aid, debug=False)


        comp_temp = ComportTemporal(self, 5.0)

        self.behaviours.append(comp_temp)

    def react(self, message):
        display_message(self.aid.localname, 'Mensagem recebida')
        if(message == "Processo Morto"):
            sys.exit()


def iniciarAgente():
    agents_per_process = 1
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = int(20000 + c)
        agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
        agente_hello = AgenteHelloWorld(AID(name=agent_name))
        agents.append(agente_hello)
        c += 1000

    start_loop(agents)

if __name__ == '__main__':
    iniciarAgente()