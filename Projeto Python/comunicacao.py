import socket
import pickle

class ComunicacaoServer():
    port = 0
    host = ""
    socket = None

    def __init__(self, port):
        self.socket = socket.socket()
        self.port = port
        self.host = "localhost"
        self.socket.bind((self.host, port))

    def ouvirCliente(self):
        self.socket.listen(5)

        while True:
            c, addr = self.socket.accept()
            print ('Got connection from', addr)
            msg = c.recv(1024)
            casa = pickle.loads(msg)
            c.close()
            return casa