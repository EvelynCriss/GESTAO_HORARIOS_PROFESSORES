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
            SELECT a.*,
                   p.nome AS professor_nome,
                   c.nome AS curso_nome,
                   d.nome AS disciplina_nome
            FROM aulas a
            JOIN professores p ON p.id = a.professor_id
            JOIN cursos c ON c.id = a.curso_id
            JOIN disciplinas d ON d.id = a.disciplina_id
            ORDER BY a.id DESC
        """)
        aulas = cursor.fetchall()
        conn.close()
        return aulas

    @staticmethod
    def get_aula(id):
        conn = Aula.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*,
                   p.nome AS professor_nome,
                   c.nome AS curso_nome,
                   d.nome AS disciplina_nome
            FROM aulas a
            JOIN professores p ON p.id = a.professor_id
            JOIN cursos c ON c.id = a.curso_id
            JOIN disciplinas d ON d.id = a.disciplina_id
            WHERE a.id = %s
        """, (id,))
        aula = cursor.fetchone()
        conn.close()
        return aula

    @staticmethod
    def get_aulas_por_curso(curso_id):
        conn = Aula.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*,
                   p.nome AS professor_nome,
                   d.nome AS disciplina_nome
            FROM aulas a
            JOIN professores p ON p.id = a.professor_id
            JOIN disciplinas d ON d.id = a.disciplina_id
            WHERE a.curso_id = %s
        """, (curso_id,))
        aulas = cursor.fetchall()
        conn.close()
        return aulas

    # ─── VALIDAÇÕES ─────────────────────────────

    @staticmethod
    def professor_disponivel(professor_id, dia_semana):
        conn = Aula.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id FROM disponibilidades
            WHERE professor_id = %s AND dia_semana = %s
        """, (professor_id, dia_semana))
        result = cursor.fetchone()
        conn.close()
        return result is not None  # True = disponível

    @staticmethod
    def professor_tem_conflito(professor_id, dia_semana, aula_id=None):
        conn = Aula.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id FROM aulas
            WHERE professor_id = %s AND dia_semana = %s
        """
        params = [professor_id, dia_semana]
        if aula_id:  # ignora a própria aula no caso de edição
            query += " AND id != %s"
            params.append(aula_id)
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result is not None  # True = tem conflito

    @staticmethod
    def curso_tem_conflito(curso_id, dia_semana, aula_id=None):
        conn = Aula.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT id FROM aulas
            WHERE curso_id = %s AND dia_semana = %s
        """
        params = [curso_id, dia_semana]
        if aula_id:
            query += " AND id != %s"
            params.append(aula_id)
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result is not None  # True = tem conflito

    # ─── CRUD ────────────────────────────────────

    @staticmethod
    def criar_aula(professor_id, curso_id, disciplina_id, dia_semana):
        conn = Aula.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO aulas (professor_id, curso_id, disciplina_id, dia_semana)
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
            SET professor_id=%s, curso_id=%s, disciplina_id=%s, dia_semana=%s
            WHERE id=%s
        """, (professor_id, curso_id, disciplina_id, dia_semana, id))
        conn.commit()
        conn.close()

    @staticmethod
    def deletar_aula(id):
        conn = Aula.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM aulas WHERE id=%s", (id,))
        conn.commit()
        conn.close()