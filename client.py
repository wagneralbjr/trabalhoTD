import socket






class Cliente():


    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        self.sock.connect((host,port))


    def start(self):
        pass


    def login(self, usuario, senha):

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

    def create_user(self, login, senha):

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


    def _lista_pasta_atual(self):

        self.sock.send("03".encode())

        dados = self.sock.recv(64).decode('utf-8')
        tam = int(dados)

        texto = self.sock.recv(tam).decode('utf-8')
        
        print(texto)











clt  = Cliente('localhost',4000)
clt.start()
clt.login('wagner','wagner')
#clt.create_user('leticia','vitoria')
clt._lista_pasta_atual()
clt._lista_pasta_atual()
clt._lista_pasta_atual()
clt._lista_pasta_atual()
clt._lista_pasta_atual()
