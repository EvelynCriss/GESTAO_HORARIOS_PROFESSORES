from flask import render_template, redirect, url_for, session
import mysql.connector
from config import db_config


def configura_rotas(app):

    @app.route('/dashboard')
    def dashboard():

        # Verifica login
        if 'loggedin' not in session:
            return redirect(url_for('login'))

        # Conexão banco
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # =========================
        # TOTAL PROFESSORES
        # =========================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM professores
        """)

        total_professores = cursor.fetchone()['total']

        # =========================
        # TOTAL CURSOS
        # =========================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM cursos
        """)

        total_cursos = cursor.fetchone()['total']

        # =========================
        # TOTAL DISCIPLINAS
        # =========================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM disciplinas
        """)

        total_disciplinas = cursor.fetchone()['total']

        # =========================
        # TOTAL AULAS
        # =========================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM aulas
        """)

        total_aulas = cursor.fetchone()['total']

        conn.close()

        # =========================
        # DADOS DASHBOARD
        # =========================

        stats = {

            'total_professores': total_professores,

            'total_cursos': total_cursos,

            'total_disciplinas': total_disciplinas,

            'total_aulas': total_aulas
        }

        return render_template(
            'dashboard.html',
            stats=stats
        )