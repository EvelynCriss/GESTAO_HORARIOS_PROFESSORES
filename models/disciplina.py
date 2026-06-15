import mysql.connector
from config import db_config


class Disciplina:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)

    @staticmethod
    def get_disciplinas():
        conn = Disciplina.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT d.*, 
                   c.nome AS curso_nome, 
                   c.periodo AS curso_periodo
            FROM disciplinas d
            JOIN cursos c ON c.id = d.curso_id
            ORDER BY d.id DESC
        """)

        disciplinas = cursor.fetchall()
        conn.close()
        return disciplinas

    @staticmethod
    def get_disciplina(id):
        conn = Disciplina.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT d.*, 
                   c.nome AS curso_nome, 
                   c.periodo AS curso_periodo
            FROM disciplinas d
            JOIN cursos c ON c.id = d.curso_id
            WHERE d.id = %s
        """, (id,))

        disciplina = cursor.fetchone()
        conn.close()
        return disciplina

    @staticmethod
    def criar_disciplina(nome, cor, curso_id):

        conn = Disciplina.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO disciplinas
            (nome, cor, curso_id)

            VALUES (%s, %s, %s)
        """, (nome, cor, curso_id))

        conn.commit()

        conn.close()

    @staticmethod
    def atualizar_disciplina(id, nome, cor, curso_id):

        conn = Disciplina.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE disciplinas

            SET
                nome=%s,
                cor=%s,
                curso_id=%s

            WHERE id=%s
        """, (nome, cor, curso_id, id))

        conn.commit()

        conn.close()

    @staticmethod
    def deletar_disciplina(id):

        conn = Disciplina.get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM disciplinas
            WHERE id=%s
        """, (id,))

        conn.commit()

        conn.close()
