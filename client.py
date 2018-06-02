import socket






class Cliente():


    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        self.sock.connect((host,port))


    def start(self):
        while True:
            self.sock.send('01'.encode())
            self.sock.send('wagner junior'.encode())
            break




clt  = Cliente('localhost',4000)
clt.start()
