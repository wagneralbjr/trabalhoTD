import threading
import socket
import time
from authentication import Authentication

TELNET_ESCAPE = 0

class ThreadedServer(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind((self.host,self.port))

        self.logado = False

        self.autentica = Authentication()
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
                try:
                    print(codigo)
                    codigo = int(codigo.decode('utf-8'))
                    print('o código recebido de função foi : ',codigo)

                    # se não está logado e o código eh 1, o cliente quer logar.
                    if (not self.logado and codigo == 1):
                        self._login(client,address)

                    if (not self.logado and codigo  == 2):
                        self._create_user(client,address)

                except Exception as e:
                    print(e)

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
            print('logou')
        else:
            print('nao logou')

        #verifica se logou e responde o usuário
        if(self.logado):
            msg = "1"
        else:
            msg = "0"
        client.send(msg.encode())


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







if __name__ == "__main__":
    #port_num = input("Port?")

    #port_num = int(port_num)
    port_num = 4000



    ThreadedServer('',port_num).listen()
