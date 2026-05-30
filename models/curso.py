import mysql.connector
from config import db_config


class Curso:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)

    @staticmethod
    def get_cursos():

        conn = Curso.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM cursos
            ORDER BY id DESC
        """)

        cursos = cursor.fetchall()

        conn.close()

        return cursos

    @staticmethod
    def get_curso(id):

        conn = Curso.get_connection()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM cursos
            WHERE id = %s
        """, (id,))

        curso = cursor.fetchone()

        conn.close()

        return curso

    @staticmethod
    def criar_curso(nome, periodo, campus):

        conn = Curso.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cursos
            (nome, periodo, campus)

            VALUES (%s, %s, %s)
        """, (nome, periodo, campus))

        conn.commit()

        conn.close()

    @staticmethod
    def atualizar_curso(id, nome, periodo, campus):

        conn = Curso.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE cursos

            SET
                nome=%s,
                periodo=%s,
                campus=%s

            WHERE id=%s
        """, (nome, periodo, campus, id))

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
