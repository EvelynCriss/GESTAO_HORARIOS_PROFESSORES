import io
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
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

            erro = False

            if not Aula.professor_disponivel(professor_id, dia_semana):
                flash('Professor não está disponível nesse dia!', 'danger')
                erro = True
            elif Aula.professor_tem_conflito(professor_id, dia_semana, disciplina_id):
                flash('Conflito: Professor já possui uma aula de matéria diferente neste dia! Ele só pode assumir esta turma se for uma junção (mesma disciplina).', 'danger')
                erro = True
            elif Aula.curso_tem_conflito(curso_id, dia_semana):
                flash('Curso já possui aula neste dia!', 'danger')
                erro = True
            elif Aula.disciplina_ja_alocada(curso_id, disciplina_id):
                flash(
                    'Esta disciplina já está alocada na grade deste curso noutro dia da semana!', 'danger')
                erro = True

            if erro:
                aula_temp = {
                    'curso_id': int(curso_id) if curso_id else '',
                    'disciplina_id': int(disciplina_id) if disciplina_id else '',
                    'professor_id': int(professor_id) if professor_id else '',
                    'dia_semana': dia_semana
                }
                return render_template('aulas/add.html',
                                       professores=professores,
                                       cursos=cursos,
                                       disciplinas=disciplinas,
                                       aula=aula_temp)

            Aula.criar_aula(professor_id, curso_id, disciplina_id, dia_semana)
            flash('Aula cadastrada com sucesso!', 'success')
            return redirect(url_for('listar_aulas'))

        return render_template('aulas/add.html',
                               professores=professores,
                               cursos=cursos,
                               disciplinas=disciplinas,
                               aula=None)

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

            elif Aula.professor_tem_conflito(professor_id, dia_semana, disciplina_id, id):
                flash(
                    'Conflito: Professor já possui uma aula de matéria diferente neste dia!', 'danger')
                return redirect(url_for('edit_aula', id=id))

            elif Aula.curso_tem_conflito(curso_id, dia_semana, id):
                flash('Curso já possui aula neste dia!', 'danger')
                return redirect(url_for('edit_aula', id=id))

            elif Aula.disciplina_ja_alocada(curso_id, disciplina_id, id):
                flash(
                    'Esta disciplina já está alocada na grade deste curso em outro dia da semana!', 'danger')
                return redirect(url_for('edit_aula', id=id))

            Aula.atualizar_aula(id, professor_id, curso_id,
                                disciplina_id, dia_semana)
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
        cursos_db = Curso.get_cursos()

        prof_info = {p['id']: p['dias_disponiveis']
                     if p['dias_disponiveis'] else '' for p in professores_db}

        grade_professores = {}
        grade_cursos = {}
        pesos_dias = {'Segunda': 1, 'Terça': 2,
                      'Quarta': 3, 'Quinta': 4, 'Sexta': 5}

        for p in professores_db:
            grade_professores[p['nome']] = {
                'id': p['id'],
                'dias_disponiveis': p['dias_disponiveis'] if p['dias_disponiveis'] else '',
                'aulas': []
            }

        for c in cursos_db:
            chave_curso = f"{c['nome']} ({c['periodo']})"
            grade_cursos[chave_curso] = {
                'id': c['id'],
                'aulas': []
            }

        for aula in aulas:
            prof_nome = aula['professor_nome']
            curso_chave = f"{aula['curso_nome']} ({aula['curso_periodo']})"

            if prof_nome in grade_professores:
                grade_professores[prof_nome]['aulas'].append(aula)
            if curso_chave in grade_cursos:
                grade_cursos[curso_chave]['aulas'].append(aula)

        for prof in grade_professores:
            grade_professores[prof]['aulas'].sort(
                key=lambda x: pesos_dias.get(x['dia_semana'], 99))
        for curso in grade_cursos:
            grade_cursos[curso]['aulas'].sort(
                key=lambda x: pesos_dias.get(x['dia_semana'], 99))

        return render_template('aulas/grade.html',
                               grade_professores=grade_professores,
                               grade_cursos=grade_cursos)

    @app.route('/aulas/mover', methods=['POST'])
    def mover_aula():
        dados = request.get_json()
        aula_id = dados.get('aula_id')
        novo_dia = dados.get('novo_dia')

        if not aula_id or str(aula_id).lower() == 'null':
            return jsonify({'status': 'error', 'message': 'Falha na interface: Tente arrastar novamente pela borda da matéria.'})

        aula_atual = Aula.get_aula(aula_id)

        if not aula_atual:
            return jsonify({'status': 'error', 'message': 'Aula não encontrada no banco de dados.'})

        if not Aula.professor_disponivel(aula_atual['professor_id'], novo_dia):
            return jsonify({'status': 'error', 'message': 'Professor indisponível neste dia.'})

        if Aula.professor_tem_conflito(aula_atual['professor_id'], novo_dia, aula_atual['disciplina_id'], aula_id):
            return jsonify({'status': 'error', 'message': 'Conflito: Professor já possui outra matéria neste dia.'})

        if Aula.curso_tem_conflito(aula_atual['curso_id'], novo_dia, aula_id):
            return jsonify({'status': 'error', 'message': 'Conflito: Curso já possui aula neste dia.'})

        Aula.atualizar_dia_aula(aula_id, novo_dia)
        return jsonify({'status': 'success'})

    @app.route('/aulas/exportar_excel')
    def exportar_excel():
        aulas = Aula.get_aulas()
        professores_db = Professor.get_professores()

        wb = openpyxl.Workbook()

        font_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
        font_prof = Font(name="Segoe UI", size=12, bold=True, color="12084f")
        font_header = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
        font_body_bold = Font(name="Segoe UI", size=10,
                              bold=True, color="12084f")
        font_body_sub = Font(name="Segoe UI", size=9,
                             italic=True, color="555555")
        font_unavailable = Font(name="Segoe UI", size=10,
                                italic=True, color="888888")

        fill_title = PatternFill(start_color="12084f",
                                 end_color="12084f", fill_type="solid")
        fill_prof = PatternFill(start_color="EAF5FF",
                                end_color="EAF5FF", fill_type="solid")
        fill_header = PatternFill(
            start_color="282c5a", end_color="282c5a", fill_type="solid")
        fill_time_cell = PatternFill(
            start_color="F5F5F5", end_color="F5F5F5", fill_type="solid")
        fill_unavailable = PatternFill(
            start_color="EAEAEA", end_color="EAEAEA", fill_type="solid")
        fill_class = PatternFill(start_color="E3F2FD",
                                 end_color="E3F2FD", fill_type="solid")

        align_center = Alignment(
            horizontal="center", vertical="center", wrap_text=True)
        align_left = Alignment(horizontal="left", vertical="center")

        thin_border_side = Side(border_style="thin", color="CCCCCC")
        thick_border_bottom = Side(border_style="medium", color="12084f")
        border_cell = Border(left=thin_border_side, right=thin_border_side,
                             top=thin_border_side, bottom=thin_border_side)

        ws = wb.active
        ws.title = "Grade Completa"
        ws.views.sheetView[0].showGridLines = False

        ws.merge_cells("A1:F1")
        title_cell = ws["A1"]
        title_cell.value = "SISTEMA DE GESTÃO - GRADE HORÁRIA COMPLETA"
        title_cell.font = font_title
        title_cell.fill = fill_title
        title_cell.alignment = align_center
        ws.row_dimensions[1].height = 40

        current_row = 3
        dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

        for prof in professores_db:
            aulas_do_prof = [
                a for a in aulas if a['professor_id'] == prof['id']]
            dias_disponiveis = prof['dias_disponiveis'].split(
                ', ') if prof['dias_disponiveis'] else []

            ws.merge_cells(start_row=current_row, start_column=1,
                           end_row=current_row, end_column=6)
            cell_prof = ws.cell(row=current_row, column=1)
            cell_prof.value = f"👨‍🏫 PROFESSOR(A): {prof['nome'].upper()}"
            cell_prof.font = font_prof
            cell_prof.fill = fill_prof
            cell_prof.alignment = align_left

            for col in range(1, 7):
                ws.cell(row=current_row, column=col).border = Border(
                    bottom=thick_border_bottom)

            ws.row_dimensions[current_row].height = 30
            current_row += 1

            headers_grade = ["Turno / Horário", "Segunda-feira",
                             "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira"]
            for col_num, header in enumerate(headers_grade, 1):
                cell = ws.cell(row=current_row, column=col_num)
                cell.value = header
                cell.font = font_header
                cell.fill = fill_header
                cell.alignment = align_center
                cell.border = border_cell

            ws.row_dimensions[current_row].height = 25
            current_row += 1

            max_aulas_num_dia = 1
            for dia in dias_semana:
                qtd_aulas = len(
                    [a for a in aulas_do_prof if a['dia_semana'] == dia])
                if qtd_aulas > max_aulas_num_dia:
                    max_aulas_num_dia = qtd_aulas

            cell_time = ws.cell(row=current_row, column=1)
            cell_time.value = "NOTURNO\n\n19h00 às 22h10"
            cell_time.fill = fill_time_cell
            cell_time.font = Font(name="Segoe UI", size=10,
                                  bold=True, color="12084f")
            cell_time.alignment = align_center
            cell_time.border = border_cell

            ws.row_dimensions[current_row].height = 70 * max_aulas_num_dia

            for col_idx, dia in enumerate(dias_semana, 2):
                cell = ws.cell(row=current_row, column=col_idx)
                cell.border = border_cell
                cell.alignment = align_center

                if dia not in dias_disponiveis:
                    cell.value = "Indisponível\n(Fora da agenda)"
                    cell.fill = fill_unavailable
                    cell.font = font_unavailable
                    continue

                aulas_no_dia = [
                    a for a in aulas_do_prof if a['dia_semana'] == dia]

                if aulas_no_dia:
                    texto_celula = ""
                    for idx, aula_alocada in enumerate(aulas_no_dia):
                        texto_celula += f"{aula_alocada['curso_nome']}\n({aula_alocada['curso_periodo']})\n📚 {aula_alocada['disciplina_nome']}"

                        if idx < len(aulas_no_dia) - 1:
                            texto_celula += "\n\n------\n\n"

                    cell.value = texto_celula
                    cell.fill = fill_class
                    cell.font = font_body_bold
                else:
                    cell.value = "Disponível\n(Sem aula)"
                    cell.font = font_body_sub

            current_row += 3

        ws.column_dimensions["A"].width = 18
        for col_letter in ["B", "C", "D", "E", "F"]:
            ws.column_dimensions[col_letter].width = 25

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="grade_horaria_completa.xlsx"
        )
