import os
import psycopg2
import re
import questions

class DataBase:

    DATABASE_URL = None
    conn = None
    cur = None
    valid_email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


    def __init__(self):
        self.DATABASE_URL = os.environ['DATABASE_URL']
        
    def __db_connect__(self):
        if self.DATABASE_URL.find('amazonaws') != -1:
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        else:
            self.conn = psycopg2.connect(self.DATABASE_URL, sslmode='require', database='localdb', user='postgres', host='localhost', password='admin')
        self.cur = self.conn.cursor() 

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

    def get_questions(self):
        questions_list = []
        try:
            self.__db_connect__()
            cursor = self.conn.cursor()
            query1 = """SELECT * FROM questions"""
            self.cur.execute(query1)
            question = self.cur.fetchone()
            while not question is None:
                question_id = question[0]
                query2 = f"""SELECT answer, is_good FROM answers WHERE question_id = {question_id}"""
                cursor.execute(query2)
                answer1 = cursor.fetchone()
                answer2 = cursor.fetchone()
                answer3 = cursor.fetchone()
                answer1 = questions.Answer(answer1[0], answer1[1])
                answer2 = questions.Answer(answer2[0], answer2[1])
                answer3 = questions.Answer(answer3[0], answer3[1])
                questions_list.append(questions.Question(question[1], answer1, answer2, answer3))
                question = self.cur.fetchone()
            cursor.close()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
        return questions_list

    def insert_questions(self, file:str):
        try:
            self.__db_connect__()
            reader = open(file) # text file
            line = reader.readline()
            while line != '':
                query = f"""INSERT INTO questions (question) VALUES ('{line}') RETURNING question_id"""
                self.cur.execute(query)
                print(query)
                question_id = self.cur.fetchone()[0]
                for i in range(3):
                    line = reader.readline()
                    good = 'false'
                    if re.match('^\+', line):
                        line = line[1:]
                        good = 'true'
                    query = f"""INSERT INTO answers (question_id, answer, is_good) VALUES ({question_id}, '{line}', {good})"""
                    self.cur.execute(query)
                    print(query)
                line = reader.readline()
            self.conn.commit()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
            reader.close()

    def delete_all_questions(self):
        try:
            self.__db_connect__()
            query = "DELETE FROM questions WHERE true"
            self.cur.execute(query)
            self.conn.commit()
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()        


        

        

    



