import socket
from utils import len_to_64b, envia_arquivo, envia_string, recebe_string, recebe_arquivo

from manager import Manager
import os


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

        #self.sock.send('01'.encode()) #código login
        envia_string(self.sock, "01")

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

        #self.sock.send("02".encode())
        envia_string(self.sock, "02")

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

        #self.sock.send("03".encode())
        envia_string(self.sock, "03")

        texto = recebe_string(self.sock)

        print(texto)

    def _envia_arquivo(self, nome_arq):

        #self.sock.send("04".encode())
        envia_string(self.sock, "04")

        envia_string(self.sock, nome_arq)
        envia_arquivo(self.sock, nome_arq)




    def _baixa_arquivo(self, nome_arq):
        """ baixa arquivo do servidor.."""
        #self.sock.send("05".encode())
        envia_string(self.sock, "05")

        print(f'entrou baixa_arquivo {nome_arq}\n\n')
        envia_string(self.sock, nome_arq)

        parts = recebe_arquivo(self.sock)

        file = open(os.path.join("recebidos", nome_arq.split('/')[-1]), "wb")

        for part in parts:
            file.write(part)
        file.close()

        return




    def verifica_downloads(self):
        "verifica se há downloads a serem feitos"

        ip, port = self.sock.getsockname()
        man = Manager()
        rows = man.verifica_downloads(self.usuario, ip,port)

        print(rows)
        if len(rows) > 0 :
            for row in rows:
                self._baixa_arquivo(row[0])
	        #deletar arquivos que faltaram ser baixados.
            man.deletar_pedidos(self.usuario, ip,port)
        else:
            print('não há downloads pendentes')





if __name__ == "__main__":

    clt  = Cliente('localhost',4000)
    clt.start()
    opcao = 99
    logado = 0
    while (opcao != 0):

        print("""\n\n\nBem vindo ao seu dropbox: \n
            1 - Logar.
            2 - Criar conta.
            3 - Mostrar arquivos.
            4 - Verificar downloads pendentes.
            5 - Enviar arquivo.
            6 - Baixar aquivo.
            """)
        opcao = int(input())
        if (opcao == 1):
            if (not logado):
                print("""Digite seu nome de usuario:""")
                username = input()
                print("Digite sua senha:")
                password = input()
                logado = clt.login(username, password)
            else:
                print('você já está logado.')
        elif (opcao == 2):
            usuario = input("digite um novo usuario")
            senha = input("digite a senha senha.")
            if ( clt.create_user(usuario,senha)):
                print('usuario criado com sucesso.')
            else:
                print('usuario não foi criado.')
        elif (opcao == 3):
            if (logado):
                clt._lista_pasta_atual()
            else:
                print("você deve estar logado para acessar essa opção.")
        elif (opcao == 4):
            if(logado):
                clt.verifica_downloads()
            else:
                print("você deve estar logado para acessar essa opção.")
        elif(opcao == 5):
            if(logado):
                nome_arquivo = input("Digite o nome do arquivo na sua pasta:")
                clt._envia_arquivo(nome_arquivo)
            else:
                print("você deve estar logado para acessar essa opção")
        elif(opcao == 6):
            #if(not logado):
                arquivo = input("insira o nome do arquivo a ser baixado.")
                clt._baixa_arquivo('wagner/a.tar.gz')

            #else:
                print("você deve estar logado para acessar essa opção")
