import mysql.connector
from config import db_config


class Disponibilidade:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)



    @staticmethod
    def get_disponibilidade():

        conn = Disponibilidade.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM disponibilidade
            ORDER BY id DESC
        """)

        disponibilidade = cursor.fetchall()

        conn.close()

        return disponibilidade


    @staticmethod
    def get_disponibilidade(id):

        conn = Disponibilidade.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM disponibilidade
            WHERE id = %s
        """, (id,))

        disponibilidade = cursor.fetchone()

        conn.close()

        return disponibilidade



    @staticmethod
    def criar_disponibilidade(professor_id, dia_semana):

        conn = Disponibilidade.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO disponibilidade
            (professor_id, dia_semana)

            VALUES (%s, %s)
        """, (professor_id, dia_semana))

        conn.commit()

        conn.close()



    @staticmethod
    def atualizar_disponibilidade(id, professor_id, dia_semana):

        conn = Disponibilidade.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE disponibilidade

            SET
                professor_id=%s,
                dia_semana=%s

            WHERE id=%s
        """, (professor_id, dia_semana, id))

        conn.commit()

        conn.close()




    @staticmethod
    def deletar_curso(id):

        conn = Curso.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM cursos
            WHERE id=%s
        """, (id,))

        conn.commit()

        conn.close()