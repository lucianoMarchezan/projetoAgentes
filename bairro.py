from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from casa import *

class Bairro():
    
    COLUMN_NUMBER = 10 #número de colunas da matrix do bairro
    LINE_NUMBER = 10 #nnúmero de linhas da matrix do bairro

    casas = []
    grid = QGridLayout()
    window = None


    def __init__(self):     
        self.configLayout()

    def configLayout(self):
        self.window = QWidget()
        self.grid = QGridLayout()
        self.grid.setObjectName("gridBairro")

        self.criarCasas()

        self.window.setLayout(self.grid)
        self.window.show()

    
    def criarCasas(self):
        for i in range(self.LINE_NUMBER):
            linha = []
            for j in range(self.COLUMN_NUMBER):
                nome = "Casa " + str(i) + " " + str(j)
                novaCasa = Casa(nome)
                linha.append(novaCasa)
                self.grid.addWidget(novaCasa.casaWidgets, i, j)
            self.casas.append(linha)



    #def teste1(self):
        #teste.setStyleSheet("QGroupBox#teste { background-color: #00CF91;}")



#x = threading.Thread(target=teste1, args=(1,))
#x.start()

#app.exec_()
