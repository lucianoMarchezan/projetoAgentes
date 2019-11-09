from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enum import Enum


class State(Enum):
    VAZIO = "Vazio" #Casa está vazia
    FOGO = "Fogo" #Casa está em chamas
    POLICIAL = "Policial" #Casa está ocupada pelo policial
    BOMBEIRO = "Bombeiro"#Casa está ocupada pelo bombeiro
    INCENDIARIO = "Incediario"#Casa está ocupada pelo incendiário
    CIVIL = "Civil"#Casa está ocupada pelo civil


class Matriz(Enum):
    COLUNAS = 10 #Número de colunas da matriz
    LINHAS = 10 #Número de linhas da matriz


class Casa():

    nameId = ""
    state = State.VAZIO.value #Estado em que a casa está
    coluna = 0
    linha = 0

    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.nameId = "" + str(linha) + str(coluna)

    def returnJsonObject(self):
        jsonObject = {
            "nameId": self.nameId,
            "state": self.state,
            "linha": self.linha,
            "coluna": self.coluna
        }
        return jsonObject
        