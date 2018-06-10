import threading
import multiprocessing as mp
import socket
import time
from authentication import Authentication
from arquivos import Arquivos
import os
from manager import Manager
from time import sleep
from utils import len_to_64b, recebe_string, recebe_arquivo

TELNET_ESCAPE = 0
PORT = 4000

class Cliente():

        def __init__(self):

            self.logado = False
            self.username = None
            self.autentica = Authentication()
            self.arq = None

        def _login(self,client,address):
            """ trata o login do usuário"""

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

            #salva na lista de usuarios,
            #print(client, address)
            self.autentica.registra_login(login, address)


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
            """ Refatorar essa função: ela deve retornar um arquivo, para poder enviar aos outros usuários"""
            if (not self.logado):
                client.send('0'.encode())
                return False

            # recebe nome do arquivo
            nomeArq = recebe_string(client)

            arquivo = recebe_arquivo(client)

            path = os.path.join(self.arq.working_path,nomeArq)
            file = open(path,"wb")
            for elem in arquivo:
                file.write(elem)
            file.close()

            #registrar o envio para os clientes.

            self._registra_envio(path, address)


            return

        def _envia_arquivo(self, client, address):
            #refatorando essa função.
            """ envia um arquivo para um cliente """

            tam_nome_arq = int(client.recv(64))

            nome_arq = client.recv(tam_nome_arq).decode('utf-8')


            return

        def _registra_envio(self, path, address):
            """ registra os envios a serem feitos para o usuarios"""
            ip , port = address
            man = Manager()
            man.insere_fila(path, self.username, ip , port)


            return


def servidor(socket, address):
    """ quando entrou aqui já fez o fork."""

    cliente = Cliente()
    size = 2
    while True:
        sleep(1)
        print(f'o cliente com ip : {address[0]} , porta : {address[1]}, entrou.')
        codigo = socket.recv(size)
        if (codigo):
            codigo = int(codigo.decode('utf-8'))
            print(f'recebido código:  {codigo} do cliente {address}')
            if (codigo == 1):
                cliente._login(socket,address)
            if (not cliente.logado and codigo  == 2):
                cliente._create_user(client,address)

            #cliente permite o usuario logado listar suas pastas.
            if (cliente.logado and codigo == 3):
                cliente._lista_folders(client,address)

            #envia arquivo.
            if (cliente.logado and codigo == 4):
                cliente._recebe_arquivo(client, address)

            if (cliente.logado and codigo == 5):
                cliente._envia_arquivo(client, address)


    return

if __name__ == "__main__":

    host = ''
    port = PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.bind((host,port))

    sock.listen(5)
    while True:
        client, address = sock.accept()
        client.settimeout(400)
        #threading.Thread(target = self.listenToClient, args = (client,address)).start()
        mp.Process(target = servidor, args = (client,address)).start()
