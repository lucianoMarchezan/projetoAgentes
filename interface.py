from PyQt5.QtWidgets import *

app = QApplication([])
window = QWidget()
linhaHorizontal1 = QWidget(window)
linhaHorizontal2 = QWidget(window)
matrix = QVBoxLayout()


linha1 = QHBoxLayout()
linha1.addWidget(QPushButton('Casa 1'))
linha1.addWidget(QPushButton('Casa 2'))
linha1.addWidget(QPushButton('Casa 3'))
linha1.addWidget(QPushButton('Casa 4'))
linhaHorizontal1.setLayout(linha1)


matrix = QVBoxLayout()

linha2 = QHBoxLayout()
linha2.addWidget(QPushButton('Casa 1'))
linha2.addWidget(QPushButton('Casa 2'))
linha2.addWidget(QPushButton('Casa 3'))
linha2.addWidget(QPushButton('Casa 4'))
linhaHorizontal2.setLayout(linha2)


matrix.addWidget(linhaHorizontal1)
matrix.addWidget(linhaHorizontal2)

window.setLayout(matrix)

for test in window.children():
    print(test)

window.show()
app.exec_()