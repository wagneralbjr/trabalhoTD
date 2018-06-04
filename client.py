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

    def _envia_arquivo(self, nome_arq):

        self.sock.send("04".encode())


        file = open(nome_arq, "rb")
        buffer = file.read()

        tam_nome_arq =  str(len(nome_arq)).rjust(64,'0')
        print(tam_nome_arq)
        self.sock.send(tam_nome_arq.encode())

        self.sock.send(nome_arq.encode())

        tam_arquivo = str(len(buffer)).rjust(64,'0')

        self.sock.send(tam_arquivo.encode())

        print('tamanho em bytes', tam_arquivo)
        # divide o arquivo e manda em pedaços
        # loucura loucura

        tam_arquivo = int(len(buffer))
        chunk_size = 1024
        qtd_packages = int(tam_arquivo / chunk_size)

        for i in range(0 , qtd_packages):
            self.sock.send(buffer[i * chunk_size : (i+1) * chunk_size])

        self.sock.send(buffer[(qtd_packages+1) * chunk_size : ])

        #self.sock.send(buffer)

clt  = Cliente('localhost',4000)
clt.start()
clt.login('wagner','wagner')
#clt.create_user('leticia','vitoria')
#clt._lista_pasta_atual()
clt._envia_arquivo('a.sh')
