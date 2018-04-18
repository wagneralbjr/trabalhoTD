
class Usuario():
    
    ip_cliente = []
    logado = False

    def __init__(login,ip_cliente = None):

        self.login = login
        self.cliente = ip_cliente if ip_cliente is not None else []

    
    @property
    def logado(): 
        return self.logado 
    
              
