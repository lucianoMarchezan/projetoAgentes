# agent_example_1.py
# A simple hello agent in PADE!

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import civil, bombeiro, incendiario



if __name__ == '__main__':
    agents_per_process = 3
    agents = list()

    port = 20001
    agent_name = 'incendiario'.format(port, port)
    agente2 = incendiario.Incendiario(AID(name=agent_name))
    agents.append(agente2)

    port = 20003
    agent_name = 'bombeiro'.format(port, port)
    nomeBombeiro = AID(name=agent_name)
    agente3 = bombeiro.Bombeiro(nomeBombeiro)
    agents.append(agente3)

    port = 20002
    agent_name = 'agent_civil'.format(port, port)
    agente1 = civil.Civil(AID(name=agent_name), nomeBombeiro)
    agents.append(agente1)

    start_loop(agents)