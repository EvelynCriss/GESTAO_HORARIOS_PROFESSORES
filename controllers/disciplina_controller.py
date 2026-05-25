from flask import render_template, request, redirect, url_for, flash
from models.disciplina import Disciplina
from models.curso import Curso


def configura_rotas(app):


    @app.route('/disciplinas')
    def listar_disciplinas():

        disciplinas = Disciplina.get_disciplinas()

        return render_template(
            'disciplinas/home.html',
            disciplinas=disciplinas
        )


    @app.route('/disciplinas/add', methods=['GET', 'POST'])
    def add_disciplina():

        cursos = Curso.get_cursos()

        if request.method == 'POST':

            nome = request.form.get('nome')
            cor = request.form.get('cor')
            curso_id = request.form.get('curso_id')

            if not nome or not cor or not curso_id:

                flash(
                    "Os campos são obrigatórios!",
                    "danger"
                )

                return redirect(
                    url_for('add_disciplina')
                )

            Disciplina.criar_disciplina(
                nome,
                cor,
                curso_id
            )

            flash(
                "Disciplina cadastrada com sucesso!",
                "success"
            )

            return redirect(
                url_for('listar_disciplinas')
            )

        return render_template(
            'disciplinas/add.html',
            cursos=cursos
        )

    @app.route('/disciplinas/edit/<int:id>',
               methods=['GET', 'POST'])

    def edit_disciplina(id):

        disciplina = Disciplina.get_disciplina(id)

        cursos = Curso.get_cursos()

        if request.method == 'POST':

            nome = request.form.get('nome')
            cor = request.form.get('cor')
            curso_id = request.form.get('curso_id')

            Disciplina.atualizar_disciplina(
                id,
                nome,
                cor,
                curso_id
            )

            flash(
                "Disciplina atualizada com sucesso!",
                "success"
            )

            return redirect(
                url_for('listar_disciplinas')
            )

        return render_template(
            'disciplinas/edit.html',
            disciplina=disciplina,
            cursos=cursos
        )


    @app.route('/disciplinas/delete/<int:id>')

    def deletar_disciplina(id):

        Disciplina.deletar_disciplina(id)

        flash(
            "Disciplina deletada com sucesso!",
            "success"
        )

        return redirect(
            url_for('listar_disciplinas')
        )