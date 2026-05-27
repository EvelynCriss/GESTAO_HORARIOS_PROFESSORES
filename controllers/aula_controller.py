from flask import render_template, request, redirect, url_for, flash
from models.aula import Aula
from models.professor import Professor
from models.curso import Curso
from models.disciplina import Disciplina


def configura_rotas(app):

    @app.route('/aulas')
    def listar_aulas():
        aulas = Aula.get_aulas()
        return render_template('aulas/home.html', aulas=aulas)

    @app.route('/aulas/add', methods=['GET', 'POST'])
    def add_aula():
        professores = Professor.get_professores()
        cursos = Curso.get_cursos()
        disciplinas = Disciplina.get_disciplinas()

        if request.method == 'POST':
            professor_id = request.form.get('professor_id')
            curso_id = request.form.get('curso_id')
            disciplina_id = request.form.get('disciplina_id')
            dia_semana = request.form.get('dia_semana')

            # 1. DISPONIBILIDADE DO PROFESSOR
            if not Aula.professor_disponivel(professor_id, dia_semana):
                flash('Professor não está disponível nesse dia!', 'danger')
                return redirect(url_for('add_aula'))

            # 2. CONFLITO DE PROFESSOR
            if Aula.professor_tem_conflito(professor_id, dia_semana):
                flash('Professor já possui aula neste dia!', 'danger')
                return redirect(url_for('add_aula'))

            # 3. CONFLITO DE CURSO
            if Aula.curso_tem_conflito(curso_id, dia_semana):
                flash('Curso já possui aula neste dia!', 'danger')
                return redirect(url_for('add_aula'))

            Aula.criar_aula(professor_id, curso_id, disciplina_id, dia_semana)
            flash('Aula cadastrada com sucesso!', 'success')
            return redirect(url_for('listar_aulas'))

        return render_template('aulas/add.html',
                               professores=professores,
                               cursos=cursos,
                               disciplinas=disciplinas)

    @app.route('/aulas/delete/<int:id>')
    def deletar_aula(id):
        Aula.deletar_aula(id)
        flash('Aula removida com sucesso!', 'success')
        return redirect(url_for('listar_aulas'))