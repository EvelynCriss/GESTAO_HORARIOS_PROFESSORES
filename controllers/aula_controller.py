from flask import render_template, request, redirect, url_for, flash
from models.aula import Aula
from models.professor import Professor
from models.curso import Curso
from models.disciplina import Disciplina


def configura_rotas(app):

    @app.route('/aulas')

    def listar_aulas():

        aulas = Aula.get_aulas()

        return render_template(
            'aulas/home.html',
            aulas=aulas
        )
    

    @app.route(
        '/aulas/add',
        methods=['GET', 'POST']
    )

    def add_aula():

        professores = Professor.get_professores()

        cursos = Curso.get_cursos()

        disciplinas = Disciplina.get_disciplinas()

        if request.method == 'POST':

            professor_id = request.form.get(
                'professor_id'
            )

            curso_id = request.form.get(
                'curso_id'
            )

            disciplina_id = request.form.get(
                'disciplina_id'
            )

            dia_semana = request.form.get(
                'dia_semana'
            )

            # CONFLITO PROFESSOR

            conflito_professor = Aula.verificar_conflito_professor(
                professor_id,
                dia_semana
            )

            if conflito_professor:

                flash(
                    'Professor já possui aula neste dia!',
                    'danger'
                )

                return redirect(
                    url_for('add_aula')
                )


            # CONFLITO CURSO

            conflito_curso = Aula.verificar_conflito_curso(
                curso_id,
                dia_semana
            )

            if conflito_curso:

                flash(
                    'Curso já possui aula neste dia!',
                    'danger'
                )

                return redirect(
                    url_for('add_aula')
                )


            # CADASTRAR

            Aula.criar_aula(
                professor_id,
                curso_id,
                disciplina_id,
                dia_semana
            )

            flash(
                'Aula cadastrada com sucesso!',
                'success'
            )

            return redirect(
                url_for('listar_aulas')
            )

        return render_template(
            'aulas/add.html',
            professores=professores,
            cursos=cursos,
            disciplinas=disciplinas
        )


    @app.route('/aulas/delete/<int:id>')

    def deletar_aula(id):

        Aula.deletar_aula(id)

        flash(
            'Aula removida com sucesso!',
            'success'
        )

        return redirect(
            url_for('listar_aulas')
        )