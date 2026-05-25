import mysql.connector
from config import db_config

class Aula:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)



    @staticmethod
    def get_aulas():

        conn = Aula.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM aulas
            ORDER BY id DESC
        """)

        aulas = cursor.fetchall()

        conn.close()

        return aulas


    @staticmethod
    def get_aula(id):

        conn = Aula.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM aulas
            WHERE id = %s
        """, (id,))

        aula = cursor.fetchone()

        conn.close()

        return aula



    @staticmethod
    def criar_aula(professor_id, curso_id, disciplina_id, dia_semana):

        conn = Aula.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO aulas
            (professor_id, curso_id, disciplina_id, dia_semana)

            VALUES (%s, %s, %s, %s)
        """, (professor_id, curso_id, disciplina_id, dia_semana))

        conn.commit()

        conn.close()



    @staticmethod
    def atualizar_aula(id, professor_id, curso_id, disciplina_id, dia_semana):

        conn = Aula.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE aulas

            SET
                professor_id=%s,
                curso_id=%s,
                disciplina_id=%s,
                dia_semana=%s

            WHERE id=%s
        """, (professor_id, curso_id, disciplina_id, dia_semana, id))

        conn.commit()

        conn.close()




    @staticmethod
    def deletar_aula(id):

        conn = Aula.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM aulas
            WHERE id=%s
        """, (id,))

        conn.commit()

        conn.close()