import socket
from utils import len_to_64b, envia_arquivo, envia_string, recebe_string, recebe_arquivo

from manager import Manager
"adicionar comentarios"

class Cliente():


    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((host,port))

        self.usuario = None

    def start(self):
        pass


    def login(self, usuario, senha):

        self.sock.send('01'.encode()) #código login

        #usuario senha
        dados = "%s %s"%(usuario,senha)

        #self.sock.send(dados.encode('utf-8'))
        envia_string(self.sock, dados)
        res  = self.sock.recv(1)
        res = int(res.decode('utf-8'))
        if (res):
            print('logado com sucesso.')
            self.usuario = usuario
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

        texto = recebe_string(self.sock)

        print(texto)

    def _envia_arquivo(self, nome_arq):

        self.sock.send("04".encode())

        envia_string(self.sock, nome_arq)
        envia_arquivo(self.sock, nome_arq)




    def _baixa_arquivo(self, nome_arq):
        """ baixa arquivo do servidor.."""
        self.sock.send("05".encode())

        print(f'entrou baixa_arquivo {nome_arq}')
        envia_string(self.sock, nome_arq)

        parts = recebe_arquivo(self.sock)

        file = open(nome_arq.split('/')[-1], "wb")

        for part in parts:
            file.write(part)
        file.close()

        return




    def verifica_downloads(self):
        "verifica se há downloads a serem feitos"

        ip, port = self.sock.getsockname()
        man = Manager()
        rows = man.verifica_downloads(self.usuario, ip,port)

        if len(rows) > 0 :
            for row in rows:
                self._baixa_arquivo(row[0])
        else:
            print('não há downloads pendentes')






if __name__ == "__main__":

    clt  = Cliente('localhost',4000)
    clt.start()
    clt.login('wagner','wagner')
    #clt.create_user('leticia','vitoria')
    #clt._lista_pasta_atual()
    clt._envia_arquivo('a.tgz')
    input("insira algo.")
    clt.verifica_downloads()
