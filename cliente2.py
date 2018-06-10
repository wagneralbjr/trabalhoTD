from client import Cliente






clt  = Cliente('localhost',4000)
clt.start()
clt.login('wagner','wagner')

input("continua?")

clt.verifica_downloads()
