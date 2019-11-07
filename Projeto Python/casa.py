from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enum import Enum


class State(Enum):
    VAZIO = 0 #Casa está vazia
    IN_FIRE = 1 #Casa está em chamas
    FILLED = 2 #Casa está ocupada por alguém

class Casa():

    nameId = ""
    state = State.VAZIO #Estado em que a casa está
    occupant = None #Quem está ocupando a casa
    casaWidgets = None  #Elemento da Interface gráfica dessa casa

    def __init__(self, nameId: str):
        """
        Parameters
        ----------
        name : str
            Nome da casa que será usada para identificá-la
        parent : QWidget
            Parente que essa casa pertence
        """
        self.nameId = nameId
        self.casaWidgets = QGroupBox()
    
    
    def setState(self, state):
        if state == State.IN_FIRE:
            self.state = State.IN_FIRE
        elif state == State.FILLED:
            self.state = State.FILLED
        else:
            self.state = State.VAZIO