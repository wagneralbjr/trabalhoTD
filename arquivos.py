import os

class Arquivos():

    working_path = None
    arquivos = dict()

    def __init__(self, pasta = "arquivos" ):
        directory = os.path.dirname(os.path.abspath(__file__))
        directory = os.path.join(directory,pasta)
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except Exception as e:
            print(e)

        self.working_path = directory

    def atualiza_arquivos(self):
        """Cria uma dicionário com os arquivos e pastas do diretório
            de trabalho"""
        self.arquivos = dict()
        for arq in os.listdir(self.working_path):

            result = dict()
            caminho = os.path.join(self.working_path, arq)
            result['pasta'] = os.path.isdir(caminho)

            infos = os.stat(caminho)
            result['ultima_mod'] = infos[8]
            result['tam'] = infos[6]

            self.arquivos[arq] = result

    def cria_diretorio(self, nome = None, pasta_raiz = None):
        """ cria um diretório."""

        if (nome is None):
            print("Erro : Nome não pode ser vazio ao criar um diretório")
            return

        if (pasta_raiz is None):
            pasta_raiz = self.working_path

        if ( os.path.exists(os.path.join(pasta_raiz, nome)) ):
            print('Já existe um arquivo ou pasta com esse nome : %s na pasta %s.'%(nome,pasta_raiz))
            return

        try:
            os.makedirs(os.path.join(pasta_raiz, nome) )
        except Exception as e:
            print(e)
            print("não foi possível criar a pasta '%s' no diretório '%s'"%(nome,pasta_raiz))

    def apaga_diretorio(self, nome= None, pasta_raiz = None):
        """ apaga um diretório """

        if (nome is None):
            print("Erro : Nome não pode ser vazio ao criar um diretório")
            return

        if (pasta_raiz is None):
            pasta_raiz = self.working_path

        #to-do : apagar a pasta.
        return

    def muda_pasta(self, nome = None, pasta_abs = None):
        '''muda a pasta atual '''
        # se passar a pasta_abs, ignorar o nome e usar a pasta_abs
        if(nome is None):
            return

        if(nome == '..'):
            # acho q essa lógica só vai funcionar em unix
            try:
                _ = self.working_path.split('/')[:-1]
            except Exception as e:
                print(e)
            #print(_)
            self.working_path = "/".join(_)
            return
        caminho = pasta_abs or os.path.join(self.working_path, nome)

        if ( os.path.isdir(caminho)):
            self.working_path = caminho
            return

        return




if __name__ == "__main__":
    obj = Arquivos()
    obj.atualiza_arquivos()
    print(obj.arquivos)
    obj.muda_pasta('..')
    obj.atualiza_arquivos()
    print(obj.arquivos)
