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
            SELECT p.*,
                GROUP_CONCAT(d.dia_semana ORDER BY d.dia_semana SEPARATOR ', ') AS dias_disponiveis
            FROM professores p
            LEFT JOIN disponibilidades d ON d.professor_id = p.id
            GROUP BY p.id
            ORDER BY p.id DESC
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
    def criar_professor(nome, email=None, telefone=None):
        conn = Professor.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO professores (nome, email, telefone)
            VALUES (%s, %s, %s)
        """, (nome, email, telefone))
        conn.commit()
        professor_id = cursor.lastrowid
        conn.close()
        return professor_id

    @staticmethod
    def atualizar_professor(id, nome, email=None, telefone=None):
        conn = Professor.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE professores
            SET nome=%s, email=%s, telefone=%s
            WHERE id=%s
        """, (nome, email, telefone, id))
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