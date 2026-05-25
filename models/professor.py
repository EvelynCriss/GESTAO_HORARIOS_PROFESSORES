import mysql.connector
from config import db_config


class Professor:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)



    @staticmethod
    def get_professores():

        conn = Professor.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM professores
            ORDER BY id DESC
        """)

        professores = cursor.fetchall()

        conn.close()

        return professores


    @staticmethod
    def get_professor(id):

        conn = Professor.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM professores
            WHERE id = %s
        """, (id,))

        professor = cursor.fetchone()

        conn.close()

        return professor



    @staticmethod
    def criar_professor(nome, email=None):

        conn = Professor.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO professores
            (nome, email)

            VALUES (%s, %s)
        """, (nome, email))

        conn.commit()

        conn.close()



    @staticmethod
    def atualizar_professor(id, nome, email=None):

        conn = Professor.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE professores

            SET
                nome=%s,
                email=%s

            WHERE id=%s
        """, (nome, email, id))

        conn.commit()

        conn.close()




    @staticmethod
    def deletar_professor(id):

        conn = Professor.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM professores
            WHERE id=%s
        """, (id,))

        conn.commit()

        conn.close()