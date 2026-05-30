import mysql.connector
from config import db_config


class Disponibilidade:

    @staticmethod
    def get_connection():
        return mysql.connector.connect(**db_config)

    @staticmethod
    def get_dias_por_professor(professor_id):
        conn = Disponibilidade.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT dia_semana FROM disponibilidades
            WHERE professor_id = %s
        """, (professor_id,))
        dias = [row['dia_semana'] for row in cursor.fetchall()]
        conn.close()
        return dias

    @staticmethod
    def criar_disponibilidade(professor_id, dia_semana):
        conn = Disponibilidade.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO disponibilidades (professor_id, dia_semana)
            VALUES (%s, %s)
        """, (professor_id, dia_semana))
        conn.commit()
        conn.close()

    @staticmethod
    def deletar_por_professor(professor_id):
        conn = Disponibilidade.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM disponibilidades
            WHERE professor_id = %s
        """, (professor_id,))
        conn.commit()
        conn.close()
