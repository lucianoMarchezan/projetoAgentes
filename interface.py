from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import schedule
import threading
from bairro import Bairro
from multiprocessing import Lock, Process, Queue, current_process
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.behaviours.protocols import TimedBehaviour
from sys import argv

lock = Lock()

def j():    
    app = QApplication(sys.argv)
    teste = Bairro()
    app.exec()


class ComportTemporal(TimedBehaviour):
    def __init__(self, agent, time):
        super(ComportTemporal, self).__init__(agent, time)

    def on_time(self):
        super(ComportTemporal, self).on_time()
        display_message(self.agent.aid.localname, 'Hello World!')


class AgenteHelloWorld(Agent):
    def __init__(self, aid):
        super(AgenteHelloWorld, self).__init__(aid=aid, debug=False)

        comp_temp = ComportTemporal(self, 1.0)

        self.behaviours.append(comp_temp)


def iniciarAgente():
    agents_per_process = 2
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = 20000 + c
        agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
        agente_hello = AgenteHelloWorld(AID(name=agent_name))
        agents.append(agente_hello)
        c += 1000

    start_loop(agents)


if __name__ == '__main__':
    p2 = Process(target=iniciarAgente, args=())
    p2 .start()
    p = Process(target=j, args=())
    p .start()

    p.join()
    p2.join()




#x = threading.Thread(target=j, args=(), daemon=True)
#x.start()
