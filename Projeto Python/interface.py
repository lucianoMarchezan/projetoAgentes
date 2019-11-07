from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import threading
from bairro import Bairro
from multiprocessing import Lock, Process, Queue, current_process
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from sys import argv

lock = Lock()

def teste(fila):
    while True:
        objeto = fila.get()

def j(fila):    
    app.exec()
    x = threading.Thread(target=teste, args=([fila]), daemon=True)
    x.start()


class ComportTemporal(TimedBehaviour):

    def __init__(self, agent, time):
        super(ComportTemporal, self).__init__(agent, time)
        self.agente = agent

    def on_time(self):
        super(ComportTemporal, self).on_time()
        display_message(self.agent.aid.localname, 'Hello World!')
        self.agente.fila.put("Teste")
        


class AgenteHelloWorld(Agent):
    def __init__(self, aid, fila, filaCenario):
        super(AgenteHelloWorld, self).__init__(aid=aid, debug=False)

        self.fila = fila
        self.colunaAtual = 0
        self.linhaAtual = 0

        comp_temp = ComportTemporal(self, 1.0)

        self.behaviours.append(comp_temp)


def iniciarAgente(fila, filaCenario):
    agents_per_process = 2
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = 20000 + c
        agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
        agente_hello = AgenteHelloWorld(AID(name=agent_name), fila, filaCenario)
        agents.append(agente_hello)
        c += 1000

    start_loop(agents)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bairro = Bairro()
    bairroAgente = []
    fila = Queue()
    filaCenario = Queue()
    p2 = Process(target=iniciarAgente, args=([fila, filaCenario]))
    p2 .start()
    p = Process(target=j, args=([bairro]))
    p .start()

    p.join()
    p2.join()

