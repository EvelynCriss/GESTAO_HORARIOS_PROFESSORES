from flask import render_template, request, redirect, url_for, flash
import mysql.connector
from models.curso import Curso


def configura_rotas(app):

    @app.route('/cursos')
    def listar_cursos():

        cursos = Curso.get_cursos()

        return render_template(
            'cursos/home.html',
            cursos=cursos
        )

    @app.route('/cursos/add', methods=['GET', 'POST'])
    def add_curso():

        if request.method == 'POST':

            nome = request.form.get('nome')
            periodo = request.form.get('periodo')
            campus = request.form.get('campus')

            if not nome or not periodo or not campus:

                flash(
                    "Os campos são obrigatórios!",
                    "danger"
                )

                return redirect(
                    url_for('add_curso')
                )

            Curso.criar_curso(
                nome,
                periodo,
                campus
            )

            flash(
                "Curso cadastrado com sucesso!",
                "success"
            )

            return redirect(
                url_for('listar_cursos')
            )

        return render_template(
            'cursos/add.html'
        )

    @app.route('/cursos/edit/<int:id>',
               methods=['GET', 'POST'])
    def edit_curso(id):

        curso = Curso.get_curso(id)

        if request.method == 'POST':

            nome = request.form.get('nome')
            periodo = request.form.get('periodo')
            campus = request.form.get('campus')

            Curso.atualizar_curso(
                id,
                nome,
                periodo,
                campus
            )

            flash(
                "Curso atualizado com sucesso!",
                "success"
            )

            return redirect(
                url_for('listar_cursos')
            )

        return render_template(
            'cursos/edit.html',
            curso=curso
        )

    @app.route('/cursos/delete/<int:id>')
    def deletar_curso(id):
        try:
            Curso.deletar_curso(id)
            flash("Curso deletado com sucesso!", "success")
        except mysql.connector.Error as err:
            if err.errno == 1451:
                flash("Ação bloqueada: Este curso possui Disciplinas ou Aulas vinculadas a ele. Você precisa deletar as disciplinas e as aulas deste curso primeiro.", "warning")
            else:
                flash(f"Erro no banco de dados: {err}", "danger")

        return redirect(url_for('listar_cursos'))
