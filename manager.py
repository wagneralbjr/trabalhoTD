import psycopg2




class Manager:

    def __init__ (self):
        try:
            self.conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
        except Exception as e:
            print(e)

        self.cursor = self.conn.cursor()


    def clientes_ativos(self,user,ip , port):
        "retorna todos os endereços dos clientes ativos com aquele login"
        sql = """select ip, port_num from online_users where login = '%s' and
            port_num != %s
        """ % (user, port)
        self.cursor.execute(sql)

        return self.cursor.fetchall()

    def insere_fila(self, path, user, ip ,port):
        """ insere arquivo na lista de downloads pendentes"""
        users = self.clientes_ativos(user, ip , port)

        print('entrou no manager.')
        for row in users:

            sql = """insert into files_download(login,ip,port,caminho,concluido)
                                 values('%s', '%s', %s, '%s',0)""" %(
                                    user, row[0], row[1], path
                                 )
            self.cursor.execute(sql)

        self.conn.commit()

        return

    def verifica_downloads(self, user, ip, port):
        "verifica se há downloads pendentes"



        sql = """select caminho from files_download where login = '%s' and  ip = '%s'
                and port = '%s' and concluido = 0
                """%(user, ip, port)
        print(sql)
        self.cursor.execute(sql)

        return self.cursor.fetchall()
