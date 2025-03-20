from flask import Flask, render_template, request, redirect, url_for, flash
from flask import Flask, render_template, request, redirect, url_for
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Carregar configurações do Supabase
load_dotenv('python.env')

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Criar cliente do Supabase
supabase: Client = create_client(url, key)

# Iniciar Flask
app = Flask(__name__)
app.secret_key = 'SecretKey' 

# Rota principal - Menu de navegação
@app.route('/')
def index():
    return render_template('index.html')

# Rota para cadastrar cliente
@app.route('/cadastro_cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        cpf_cnpj = request.form['cpf_cnpj']
        nome = request.form['nome']
        email = request.form['email']

        # Inserir os dados no Supabase
        try:
            response = supabase.table('Clientes').insert({
                "cpf_cnpj": cpf_cnpj,
                "nome": nome,
                "email": email
            }).execute()

            if response.data:
                return redirect(url_for('index'))
            else:
                return "Erro ao cadastrar cliente", 400
        except Exception as e:
            return f"Erro ao cadastrar: {str(e)}", 500

    return render_template('cadastro_cliente.html')

# Rota para cadastrar produto (apenas exemplo, será semelhante à de clientes)

@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
    if request.method == 'POST':
        # Verifica se os campos existem no formulário
        if 'nome_produto' not in request.form or 'tipo_produto' not in request.form or 'preco' not in request.form:
            return "Campos 'nome_produto', 'tipo_produto' e 'preco' são obrigatórios", 400

        nome_produto = request.form['nome_produto']
        tipo_produto = request.form['tipo_produto']
        preco = request.form['preco']

        # Inserir os dados no Supabase
        try:
            response = supabase.table('Produtos').insert({
                "nome": nome_produto,
                "tipoproduto": tipo_produto,
                "valorproduto": preco
            }).execute()

            if response.data:
                flash('Cadastro realizado com sucesso!', 'success')  # Mensagem de sucesso
                return redirect(url_for('cadastro_produto'))
            else:
                return "Erro ao cadastrar produto", 400
        except Exception as e:
            flash(f'Erro ao cadastrar: {str(e)}', 'error')
            return redirect(url_for('cadastro_produto'))  

    return render_template('cadastro_produto.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/alterar_produto', methods=['GET'])
def alterar_produto():
    return render_template('alterar_produto.html')

# Rota para buscar CPF e retornar os dados do cliente para alteração
@app.route('/alterar_cliente_buscarcpf', methods=['GET', 'POST'])
def alterar_cliente_buscarcpf():
    if request.method == 'POST':
        cpf = request.form['cpf']
        # Consulta o cliente no Supabase onde o campo 'cpf_cnpj' é igual ao CPF informado.
        response = supabase.table("Clientes").select("*").eq("cpf_cnpj", cpf).execute()

        if response.data:
            # Assumindo que o resultado é uma lista de dicionários, pegamos o primeiro registro.
            cliente = response.data[0]
            return render_template('alterar_cliente_dados.html', cliente=cliente)
        else:
            return "Cliente não encontrado", 404

    # Se for GET, exibe o formulário para inserir o CPF
    return render_template('alterar_cliente_buscarcpf.html')


if __name__ == '__main__':
    app.run(debug=True)

#teste#