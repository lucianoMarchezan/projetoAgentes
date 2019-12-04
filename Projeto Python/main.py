# agent_example_1.py
# A simple hello agent in PADE!

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import civil, bombeiro, incendiario, policial



if __name__ == '__main__':
    agents_per_process = 3
    agents = list()

    port = 20001
    agent_name = 'incendiario'.format(port, port)
    agenteIncendiario = incendiario.Incendiario(AID(name=agent_name))
    agents.append(agenteIncendiario)

    port = 20003
    nomeBombeiro = 'bombeiro_{}@localhost:{}'.format(port, port)
    agenteBombeiro = bombeiro.Bombeiro(AID(name=nomeBombeiro), portC=10000)
    agents.append(agenteBombeiro)

    port = 20004
    nomeBombeiro = 'policial_{}@localhost:{}'.format(port, port)
    agentePolicial = policial.Policial(AID(name=nomeBombeiro), portC=10010)
    agents.append(agentePolicial)

    port = 20002
    agent_name = 'agent_civil_{}@localhost:{}'.format(port, port)
    agenteCivil = civil.Civil(AID(name=agent_name), agenteBombeiro, agentePolicial)
    agents.append(agenteCivil)

    agenteBombeiro.policial = agentePolicial
    agentePolicial.bombeiro = agenteBombeiro

    

    start_loop(agents)