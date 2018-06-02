import socket






class Cliente():


    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        self.sock.connect((host,port))


    def start(self):
        pass


    def _login(self, usuario, senha):

        self.sock.send('01'.encode()) #código login

        #usuario senha
        dados = "%s %s"%(usuario,senha)

        self.sock.send(dados.encode('utf-8'))

        res  = self.sock.recv(1)
        res = int(res.decode('utf-8'))
        if (res):
            print('logado com sucesso.')
            return True
        else:
            print('não logado')
            return False

    def _create_user(self, login, senha):

        self.sock.send("02".encode())

        dados = "%s %s"%(login,senha)
        self.sock.send(dados.encode('utf-8'))

        res  = self.sock.recv(1)
        res = int(res.decode('utf-8'))
        if (res):
            print('usuário criado com sucesso.')
            return True
        else:
            print('não criado o usuário')
            return False






clt  = Cliente('localhost',4000)
clt.start()
#clt._login('wagner','wagner')
clt._create_user('leticia','vitoria')
