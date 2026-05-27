from flask import render_template, request, redirect, url_for, flash, jsonify
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

            if not Aula.professor_disponivel(professor_id, dia_semana):
                flash('Professor não está disponível nesse dia!', 'danger')
                return redirect(url_for('add_aula'))

            if Aula.professor_tem_conflito(professor_id, dia_semana, curso_id):
                flash('Professor já possui aula neste turno neste dia!', 'danger')
                return redirect(url_for('add_aula'))

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

    @app.route('/aulas/edit/<int:id>', methods=['GET', 'POST'])
    def edit_aula(id):
        aula = Aula.get_aula(id)
        professores = Professor.get_professores()
        cursos = Curso.get_cursos()
        disciplinas = Disciplina.get_disciplinas()

        if request.method == 'POST':
            professor_id = request.form.get('professor_id')
            curso_id = request.form.get('curso_id')
            disciplina_id = request.form.get('disciplina_id')
            dia_semana = request.form.get('dia_semana')

            if not Aula.professor_disponivel(professor_id, dia_semana):
                flash('Professor não está disponível nesse dia!', 'danger')
                return redirect(url_for('edit_aula', id=id))

            if Aula.professor_tem_conflito(professor_id, dia_semana, curso_id, id):
                flash('Professor já possui aula neste turno neste dia!', 'danger')
                return redirect(url_for('edit_aula', id=id))

            if Aula.curso_tem_conflito(curso_id, dia_semana, id):
                flash('Curso já possui aula neste dia!', 'danger')
                return redirect(url_for('edit_aula', id=id))

            Aula.atualizar_aula(id, professor_id, curso_id, disciplina_id, dia_semana)
            flash('Aula atualizada com sucesso!', 'success')
            return redirect(url_for('listar_aulas'))

        return render_template('aulas/edit.html',
                               aula=aula,
                               professores=professores,
                               cursos=cursos,
                               disciplinas=disciplinas)

    @app.route('/aulas/delete/<int:id>')
    def deletar_aula(id):
        Aula.deletar_aula(id)
        flash('Aula removida com sucesso!', 'success')
        return redirect(url_for('listar_aulas'))

    @app.route('/grade_horaria')
    def grade_horaria():
        aulas = Aula.get_aulas()
        professores_db = Professor.get_professores()

        prof_info = {}
        for p in professores_db:
            prof_info[p['nome']] = {
                'id': p['id'],
                'dias_disponiveis': p['dias_disponiveis'] if p['dias_disponiveis'] else ''
            }

        grade = {}
        pesos_dias = {'Segunda': 1, 'Terça': 2, 'Quarta': 3, 'Quinta': 4, 'Sexta': 5}

        for aula in aulas:
            prof_nome = aula['professor_nome']
            if prof_nome not in grade:
                grade[prof_nome] = {
                    'id': aula['professor_id'],
                    'dias_disponiveis': prof_info.get(prof_nome, {}).get('dias_disponiveis', ''),
                    'aulas': []
                }
            grade[prof_nome]['aulas'].append(aula)

        for prof in grade:
            grade[prof]['aulas'].sort(key=lambda x: pesos_dias.get(x['dia_semana'], 99))

        return render_template('aulas/grade.html', grade=grade)

    @app.route('/aulas/api/mover_aula', methods=['POST'])
    def mover_aula():
        data = request.get_json()
        aula_id = data.get('aula_id')
        novo_dia = data.get('novo_dia')

        aula = Aula.get_aula(aula_id)
        if not aula:
            return jsonify({'status': 'error', 'message': 'Aula não encontrada.'})

        prof_id = aula['professor_id']
        curso_id = aula['curso_id']
        disc_id = aula['disciplina_id']

        if not Aula.professor_disponivel(prof_id, novo_dia):
            return jsonify({'status': 'error', 'message': f"O professor {aula['professor_nome']} não está disponível na {novo_dia}."})

        if Aula.professor_tem_conflito(prof_id, novo_dia, aula_id):
            return jsonify({'status': 'error', 'message': f"O professor {aula['professor_nome']} já tem outra aula na {novo_dia}."})

        if Aula.curso_tem_conflito(curso_id, novo_dia, aula_id):
            return jsonify({'status': 'error', 'message': f"O curso {aula['curso_nome']} já possui outra aula na {novo_dia}."})

        Aula.atualizar_aula(aula_id, prof_id, curso_id, disc_id, novo_dia)
        
        return jsonify({'status': 'success'})