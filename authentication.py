import psycopg2

class Authentication:



    def __init__ (self):
        try:
            self.conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
        except Exception as e:
            print(e)

        self.cursor = self.conn.cursor()


    def create_database(self):
        #to-do
        pass


    def create_user(self,usuario, senha):
        try:
            sql = "insert into usuarios(nome,senha) values('%s','%s')"%(usuario,senha)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False


        return True

    def login(self,usuario,senha):

        sql = "select nome,senha from usuarios where nome = '%s'"% (usuario)

        self.cursor.execute(sql)
        row = self.cursor.fetchone()


        if row is not None:
            if(senha == row[1]):
                return True
            else:
                return False
        else:
            return False

    def registra_login(self, usuario, address):
        """ registra login do usuario"""
        ip, port  = address

        sql = "insert into online_users(login,ip,port_num) values ('%s','%s','%s')"% (usuario, ip,port)
        self.cursor.execute(sql)

        self.conn.commit()

        return
