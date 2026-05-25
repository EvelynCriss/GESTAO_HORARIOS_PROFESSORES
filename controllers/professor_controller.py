from flask import render_template, request, redirect, url_for, flash

from models.professor import Professor


def configura_rotas(app):


    @app.route('/professores')
    def listar_professores():

        professores = Professor.get_professores()

        return render_template(
            'professores/home.html',
            professores=professores
        )


    @app.route('/professores/add', methods=['GET', 'POST'])
    def add_professor():

        if request.method == 'POST':

            nome = request.form.get('nome')
            email = request.form.get('email')

            if not nome:

                flash(
                    "Nome é obrigatório!",
                    "danger"
                )

                return redirect(
                    url_for('add_professor')
                )

            Professor.criar_professor(
                nome,
                email
            )

            flash(
                "Professor cadastrado com sucesso!",
                "success"
            )

            return redirect(
                url_for('listar_professores')
            )

        return render_template(
            'professores/add.html'
        )


    @app.route('/professores/edit/<int:id>',
               methods=['GET', 'POST'])

    def edit_professor(id):

        professor = Professor.get_professor(id)

        if request.method == 'POST':

            nome = request.form.get('nome')
            email = request.form.get('email')

            Professor.atualizar_professor(
                id,
                nome,
                email
            )

            flash(
                "Professor atualizado com sucesso!",
                "success"
            )

            return redirect(
                url_for('listar_professores')
            )

        return render_template(
            'professores/edit.html',
            professor=professor
        )


    @app.route('/professores/delete/<int:id>')

    def deletar_professor(id):

        Professor.deletar_professor(id)

        flash(
            "Professor deletado com sucesso!",
            "success"
        )

        return redirect(
            url_for('listar_professores')
        )