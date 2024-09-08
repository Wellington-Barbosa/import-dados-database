from flask import Flask, render_template, request, redirect, url_for, flash, session
import oracledb
import hashlib

# Habilita o modo thick, necessário para suportar versões antigas do Oracle Database
oracledb.init_oracle_client(lib_dir=r"C:\instantclient_23_4")  # Altere para o caminho correto do Instant Client

# Função para inicializar as rotas no app
def init_routes(app):
    # Página principal (login)
    @app.route('/')
    def index():
        return render_template('index.html')

    # Conectar ao banco de dados Oracle
    def db_connection():
        connection = oracledb.connect(
            user="tasy",
            password="aloisk",
            dsn="172.25.1.4:1521/DBTASY"
        )
        return connection

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            fullname = request.form['fullname']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']  # 'A' para Administrador, 'C' para Convencional

            # Criptografar a senha
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Conectar ao banco e inserir os dados
            conn = db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO TASY.SIS_UNIMED_WB (NR_SEQUENCIA, DT_ATUALIZACAO, NN_USUARIO, DS_USUARIO, DS_SENHA, DS_EMAIL, IE_PERMISSAO)
                VALUES (SEQ_SIS_UNIMED_WB.NEXTVAL, SYSDATE, :username, :fullname, :password, :email, :role)
            """, [username, fullname, hashed_password, email, role])

            conn.commit()
            cursor.close()
            conn.close()

            return redirect('/success')
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Criptografar a senha para comparar com a armazenada no banco
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Conectar ao banco e verificar se o usuário existe
            conn = db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DS_SENHA, IE_PERMISSAO FROM SIS_UNIMED_WB WHERE NN_USUARIO = :username", [username])
            result = cursor.fetchone()

            if result and result[0] == hashed_password:
                # Verificar o tipo de usuário (Administrador ou Convencional)
                user_permission = result[1]
                flash('Login efetuado com sucesso!', 'success')

                # Armazenar informações na sessão
                session['username'] = username
                session['user_permission'] = user_permission

                # Redirecionar para a página de dashboard
                return redirect(url_for('dashboard'))
            else:
                flash('Usuário ou senha inválidos', 'danger')

        return render_template('index.html')

    @app.route('/dashboard')
    def dashboard():
        # Verificação de login e permissões
        if 'username' in session:
            username = session['username']
            user_permission = session.get('user_permission', 'C')  # Padrão para usuário convencional
            return render_template('dashboard.html', username=username, user_permission=user_permission)
        else:
            return redirect(url_for('login'))

    @app.route('/logout', methods=['POST'])
    def logout():
        session.clear()  # Limpar sessão do usuário
        flash('Logout realizado com sucesso!', 'success')
        return redirect(url_for('login'))
