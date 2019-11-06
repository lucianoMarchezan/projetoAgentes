# agente_incendiario.py
# Implementação do agente incendiário!
from pade.behaviours.protocols import TimedBehaviour
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
from random import randrange


class ComportTemporal(TimedBehaviour):
    def __init__(self, agent, time):
        super(ComportTemporal, self).__init__(agent, time)

    def on_time(self):
        super(ComportTemporal, self).on_time()
        casa = randrange(4)
        display_message(self.agent.aid.localname, 'Moveu para' + casa)
        fogo = randrange(10)
        if fogo < 4:
            display_message(self.agent.aid.localname, 'Tacou fogo na casa')


class AgenteIncendiario(Agent):
    def __init__(self, aid):
        super(AgenteIncendiario, self).__init__(aid=aid)
        comp_temp = ComportTemporal(self, 2.0)
        self.behaviours.append(comp_temp)
