import os
import psycopg2
import re
import urllib.parse as urlparse

class DataBase:

    DATABASE_URL = None
    conn = None
    cur = None
    # regex zalecany do użycia w RFC 5322 xD
    # valid_email_regex = """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|
    # "(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@
    # (?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2
    # [0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]
    # :(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""

    valid_email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


    def __init__(self):
        self.DATABASE_URL = os.environ['DATABASE_URL']
        self.url = urlparse.urlparse(os.environ['DATABASE_URL'])
        self.dbname = self.url.path[1:]
        self.user = self.url.username
        self.password = self.url.password
        self.host = self.url.hostname
        self.port = self.url.port
        
    def __db_connect__(self):
        if os.environ['USER'] == 'pawel' or os.environ['USER'] == 'postgres': # for local db purpose
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require', database='localdb', user='postgres', host='localhost', password='admin')
        else:
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require', dbname=self.dbname, user=self.user, password=self.password,
             host=self.host, port=self.port)
        self.cur = self.conn.cursor() 

    # def __db_close__(self):
    #     self.cur.close()
    #     self.conn.close()

    def select_users_points(self):
        resp = []
        try:
            self.__db_connect__()
            query = "SELECT user_name AS Gracz, points AS Punkty FROM users ORDER BY points DESC;"
            self.cur.execute(query)
            resp = self.cur.fetchall()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return resp

    def is_user_in_base(self, name):
        if not isinstance(name, str):
            return "name not string"
        resp = None
        try:
            self.__db_connect__()
            query = f"SELECT user_name FROM users WHERE user_name = '{name}';"
            self.cur.execute(query)
            resp = self.cur.fetchone()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return resp

    def is_email_in_base(self, email):
        if not isinstance(email, str):
            return "email not string"
        resp = None
        try:
            self.__db_connect__()
            query = f"SELECT mail FROM users WHERE mail = '{email}';"
            self.cur.execute(query)
            resp = self.cur.fetchone()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return resp
        


    def insert_new_user(self, name, password, email):
        if not isinstance(name, str):
            return "name not string"
        if not isinstance(password, str):
            return "password not string"
        if not isinstance(email, str):
            return "email not string"
        if re.search(self.valid_email_regex, email) is None:
            return "email not valid"

        new_user_created = False

        try:
            self.__db_connect__()
            insert = f"""INSERT INTO users(user_name, passw, mail, points) VALUES 
                        ('{name}', crypt('{password}', gen_salt('bf')), '{email}', 0);"""
            self.cur.execute(insert)
            self.conn.commit()
            new_user_created = "User created"
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

        return new_user_created
    
    def get_points(self, name):
        points = -1
        try:
            self.__db_connect__()
            query = f"""SELECT points FROM users WHERE user_name = '{name}';"""
            self.cur.execute(query)
            points = self.cur.fetchone()
            points = points[0]
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return points

    def set_points(self, name, points):
        points = -1
        try:
            self.__db_connect__()
            query = f"""UPDATE users SET points = {points} WHERE user_name = '{name}';"""
            self.cur.execute(query)
            self.conn.commit()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return points

    def login_user(self, name, password):
        valid_user = False
        try:
            self.__db_connect__()
            query = f"""SELECT user_name FROM users WHERE user_name = '{name}' AND passw = crypt('{password}', passw);"""
            self.cur.execute(query)
            resp = self.cur.fetchone()
            if not resp is None:
                valid_user = True
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return valid_user
    
        

        

    



