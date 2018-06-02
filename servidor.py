import threading
import socket
import time

TELNET_ESCAPE = 0

class ThreadedServer(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind((self.host,self.port))

        self.logado = False

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




                except ValueError as e:
                    print(e)
                    print('cod não númerico.')
                #client.send(('envie um código numérico').encode('utf-8'))

        return


    def _login(self,client,address):
        """ trata o login do usuário"""
        print('entrou login')
        dados = client.recv(64 + TELNET_ESCAPE).decode('utf-8')
        login, senha = (dados.split(' '))

        print(login ,"\n",senha)





if __name__ == "__main__":
    port_num = input("Port?")

    port_num = int(port_num)



    ThreadedServer('',port_num).listen()
