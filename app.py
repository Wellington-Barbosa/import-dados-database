import os
from flask import Flask, render_template, request, redirect, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = "Surubaoderato123#"  # Necessário para exibir mensagens de erro e sucesso
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Página principal com o formulário de upload
@app.route('/')
def upload_file():
    return render_template('upload.html')


# Função para tratar o upload do arquivo
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado.')
        return redirect('/')

    file = request.files['file']

    # Verifica se o arquivo tem extensão permitida
    if file.filename == '':
        flash('Nenhum arquivo selecionado.')
        return redirect('/')

    # Salva o arquivo temporariamente
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Validação do arquivo
    try:
        # Aqui você pode escolher se é CSV ou TXT
        df = pd.read_csv(file_path)  # Ou pd.read_table(file_path) para TXT

        # Validação dos campos obrigatórios
        required_columns = ['NM_USUARIO', 'CD_ESTABELECIMENTO', 'CD_BEM', 'DS_BEM',
                            'DT_AQUISICAO', 'NR_SEQ_TIPO', 'NR_SEQ_LOCAL',
                            'IE_TIPO_VALOR', 'TX_DEPREC', 'VL_ORIGINAL', 'CD_MOEDA']
        if not all(col in df.columns for col in required_columns):
            flash('Arquivo inválido: campos obrigatórios faltando.')
            return redirect('/')

        # Sucesso na validação
        flash('Validação concluída com sucesso!')
    except Exception as e:
        flash(f'Erro na validação do arquivo: {str(e)}')
        return redirect('/')

    return redirect('/')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5000)
