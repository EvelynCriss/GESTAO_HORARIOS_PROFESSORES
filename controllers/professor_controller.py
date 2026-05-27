from flask import render_template, request, redirect, url_for, flash
from models.professor import Professor
from models.disponibilidade import Disponibilidade


def configura_rotas(app):

    @app.route('/professores')
    def listar_professores():
        professores = Professor.get_professores()
        return render_template('professores/home.html', professores=professores)

    @app.route('/professores/add', methods=['GET', 'POST'])
    def add_professor():
        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            dias = request.form.getlist('dias_semana')

            if not nome:
                flash("Nome é obrigatório!", "danger")
                return redirect(url_for('add_professor'))

            professor_id = Professor.criar_professor(nome, email, telefone)

            for dia in dias:
                Disponibilidade.criar_disponibilidade(professor_id, dia)

            flash("Professor cadastrado com sucesso!", "success")
            return redirect(url_for('listar_professores'))

        return render_template('professores/add.html')

    @app.route('/professores/edit/<int:id>', methods=['GET', 'POST'])
    def edit_professor(id):
        professor = Professor.get_professor(id)

        if request.method == 'POST':
            nome = request.form.get('nome')
            email = request.form.get('email')
            telefone = request.form.get('telefone')
            dias = request.form.getlist('dias_semana')

            Professor.atualizar_professor(id, nome, email, telefone)

            Disponibilidade.deletar_por_professor(id)
            for dia in dias:
                Disponibilidade.criar_disponibilidade(id, dia)

            flash("Professor atualizado com sucesso!", "success")
            return redirect(url_for('listar_professores'))

        dias_selecionados = Disponibilidade.get_dias_por_professor(id)
        return render_template('professores/edit.html',
                               professor=professor,
                               dias_selecionados=dias_selecionados)

    @app.route('/professores/delete/<int:id>')
    def deletar_professor(id):
        Disponibilidade.deletar_por_professor(id)  # ← apaga os dias antes
        Professor.deletar_professor(id)
        flash("Professor deletado com sucesso!", "success")
        return redirect(url_for('listar_professores'))