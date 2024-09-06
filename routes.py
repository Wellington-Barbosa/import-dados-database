from flask import render_template, request, redirect, flash, url_for
import os


# Função para inicializar as rotas no app
def init_routes(app):
    # Página principal (login)
    @app.route('/')
    def index():
        return render_template('index.html')

    # Função para tratar o login
    @app.route('/login', methods=['POST'])
    def login():
        username = request.form.get('username')
        password = request.form.get('password')

        # Validação simples de login (substitua por algo mais robusto depois)
        if username == "admin" and password == "admin":
            return redirect(url_for('upload_file'))  # Redireciona para a página de upload
        else:
            flash('Credenciais inválidas, tente novamente.')
            return redirect('/')

    # Página de upload
    @app.route('/upload')
    def upload_file():
        return render_template('upload.html')

    # Função para tratar o upload do arquivo
    @app.route('/upload', methods=['POST'])
    def upload():
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado.')
            return redirect('/upload')

        file = request.files['file']

        if file.filename == '':
            flash('Nenhum arquivo selecionado.')
            return redirect('/upload')

        # Salva o arquivo temporariamente
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Validação do arquivo
        # ...

        flash('Validação concluída com sucesso!')
        return redirect('/upload')
