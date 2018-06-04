
""" arquivo de funções utilitárias ."""

def len_to_64b(nome):

    return str(len(nome)).rjust(64,'0')




""" Esta função deve enviar tamanho e o arquivo somente."""
def envia_arquivo(socket, arquivo_path, chunk_size = 1024):

    buffer = open(arquivo_path, "rb").read()
    tam_arquivo = len_to_64b(buffer)

    print(tam_arquivo)
    socket.send(tam_arquivo.encode())

    tam_arquivo = len(buffer)

    qtd_packages = int( tam_arquivo / chunk_size)
    for i in range(0 , qtd_packages):
        socket.send(buffer[i * chunk_size : (i+1) * chunk_size])

    socket.send(buffer[(qtd_packages+1) * chunk_size : ])

    return


"""Envia um tamanho de string e o seu conteúdo."""
def envia_string(socket, string):

    tam_string = len_to_64b(string)
    socket.send(tam_string.encode())

    socket.send(string.encode())

    return

"""recebe uma string"""
def recebe_string(socket):

    tam_string = int(socket.recv(64).decode('utf-8'))
    string = socket.recv(tam_string).decode('utf-8')

    return string



""" recebe e retorna um arquivo dividido em pedaços"""
def recebe_arquivo(socket, chunk_size = 1024):


    tam_arquivo = int(socket.recv(64))
    qtd_packages = int(tam_arquivo / chunk_size)

    arquivo = []

    for i in range(0, qtd_packages):

        arquivo.append(socket.recv(chunk_size))

    falta = tam_arquivo - (qtd_packages)

    if (falta > 0):
        arquivo.append(socket.recv(falta))

    return arquivo
