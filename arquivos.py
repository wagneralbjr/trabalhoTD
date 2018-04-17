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
        """Cria uma lista com os arquivos e pastas do diretório
            de trabalho"""
        for arq in os.listdir(self.working_path):

            result = dict()
            caminho = os.path.join(self.working_path, arq)
            result['pasta'] = os.path.isdir(caminho)

            infos = os.stat(caminho)
            result['ultima_mod'] = infos[8]
            result['tam'] = infos[6]  

            self.arquivos[arq] = result 

if __name__ == "__main__":
    obj = Arquivos()
    obj.atualiza_arquivos()
    print(obj.arquivos)
