import mysql.connector
from werkzeug.security import generate_password_hash
from config import db_config


class Login:

    @staticmethod
    def conectar():
        return mysql.connector.connect(**db_config)

    @staticmethod
    def get_email(email):
        conn = Login.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    @staticmethod
    def get_id(id_usuario):
        conn = Login.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM login WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario

    @staticmethod
    def criar_login_usuario(nome, email, senha):
        senha_hash = generate_password_hash(senha)

        conn = Login.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO login (nome, email, senha) VALUES (%s, %s, %s)
        """, (nome, email, senha_hash))

        conn.commit()
        conn.close()
