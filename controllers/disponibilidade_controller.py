from flask import render_template, request, redirect, url_for, flash
from models.disponibilidade import Disponibilidade
from models.professor import Professor


def configura_rotas(app):


    @app.route('/disponibilidades')

    def listar_disponibilidades():

        disponibilidades = Disponibilidade.get_disponibilidades()

        return render_template(
            'disponibilidades/home.html',
            disponibilidades=disponibilidades
        )



    @app.route(
        '/disponibilidades/add',
        methods=['GET', 'POST']
    )

    def add_disponibilidade():

        professores = Professor.get_professores()

        if request.method == 'POST':

            professor_id = request.form.get(
                'professor_id'
            )

            dia_semana = request.form.get(
                'dia_semana'
            )

            Disponibilidade.criar_disponibilidade(
                professor_id,
                dia_semana
            )

            flash(
                'Disponibilidade cadastrada!',
                'success'
            )

            return redirect(
                url_for(
                    'listar_disponibilidades'
                )
            )

        return render_template(
            'disponibilidades/add.html',
            professores=professores
        )


    @app.route(
        '/disponibilidades/delete/<int:id>'
    )

    def deletar_disponibilidade(id):

        Disponibilidade.deletar_disponibilidade(id)

        flash(
            'Disponibilidade removida!',
            'success'
        )

        return redirect(
            url_for(
                'listar_disponibilidades'
            )
        )