import threading
import socket
import time
from authentication import Authentication
from arquivos import Arquivos
import os

TELNET_ESCAPE = 0

class ThreadedServer(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind((self.host,self.port))

        self.logado = False

        self.username = None

        self.autentica = Authentication()

        self.arq = None

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient, args = (client,address)).start()

    def listenToClient(self,client,address):
        size = 2 + TELNET_ESCAPE #considerando q tá vindo o /r/n do telnet
        while True:
            codigo = client.recv(size)
            if codigo:
                #try:
                    print(codigo)
                    codigo = int(codigo.decode('utf-8'))
                    print('o código recebido de função foi : ',codigo)

                    # se não está logado e o código eh 1, o cliente quer logar.
                    if (not self.logado and codigo == 1):
                        self._login(client,address)
                    # permite o usuario deslogado criar um user.
                    if (not self.logado and codigo  == 2):
                        self._create_user(client,address)

                    #self permite o usuario logado listar suas pastas.
                    if (self.logado and codigo == 3):
                        self._lista_folders(client,address)

                    #envia arquivo.
                    if (self.logado and codigo == 4):
                        self._recebe_arquivo(client, address)


                #except Exception as e:
                #    print(e)

        return


    def _login(self,client,address):
        """ trata o login do usuário"""

        print('entrou login')
        dados = client.recv(64 + TELNET_ESCAPE).decode('utf-8')
        (login,senha) = (dados.split(' '))

        print(login)
        print(senha)


        if (self.autentica.login(login,senha)):
            self.logado = True
            self.username = login
            print('logou')
        else:
            print('nao logou')

        #verifica se logou e responde o usuário
        if(self.logado):
            msg = "1"
        else:
            msg = "0"
        client.send(msg.encode())

        # instancia a pasta do usuario no sv.
        if (self.logado):
            self.arq = Arquivos(self.username)


    def _create_user(self, client,address):
        """ Permite a criação de usuários"""
        print('entrou create_user')
        dados = client.recv(64 + TELNET_ESCAPE).decode('utf-8')
        (login,senha) = (dados.split(' '))


        if(self.autentica.create_user(login,senha)):
            print('usuario criado')
            msg = '1'
        else:
            print('usuario nao criado')
            msg = '0'

        client.send(msg.encode())

    def _lista_folders(self, client, address):
        if (not self.logado):
            print('deve estar logado para acessar os arquivos.')
            return False


        self.arq.atualiza_arquivos()

        #dados = str(arq.arquivos).encode()

        dados = ""
        dados += "NOME\t\t\t\tPASTA\n"
        for key,value in self.arq.arquivos.items():

            dados+= "%s\t\t\t"%(key)
            if(value):
                dados+="SIM"
            else:
                dados+="NAO"
            dados+="\n"

        dados+="\n"
        dados = dados.encode()

        print(dados)

        client.send(str(len(dados)).encode())
        client.send(dados)

    def _recebe_arquivo(self, client, address):

        if (not self.logado):
            client.send('0'.encode())
            return False

        # recebe nome do arquivo
        tamNome = int(client.recv(64).decode('utf-8'))
        nomeArq = client.recv(tamNome).decode('utf-8')

        # recebe arquivo
        tam_arquivo = int(client.recv(64))
        print(tam_arquivo)
        #arquivo = client.recv(tam_arquivo)

        chunk_size = 1024
        qtd_packages = int(tam_arquivo / chunk_size)

        arquivo = [] #buffer

        for i in range(0, qtd_packages):
            arquivo.append(client.recv(chunk_size))

        falta = tam_arquivo - (qtd_packages * chunk_size)
        if ( falta > 0 ):
            arquivo.append(client.recv(falta))



        file = open(os.path.join(self.arq.working_path,nomeArq),"wb")
        for elem in arquivo:
            file.write(elem)
        file.close()


if __name__ == "__main__":
    #port_num = input("Port?")

    #port_num = int(port_num)
    port_num = 4000



    ThreadedServer('',port_num).listen()
