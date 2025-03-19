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
        nome_produto = request.form['nome_produto']
        preco = request.form['preco']
        
        # Inserir os dados no Supabase
        try:
            response = supabase.table('Produtos').insert({
                "nome_produto": nome_produto,
                "preco": preco
            }).execute()

            if response.data:
                return redirect(url_for('index'))
            else:
                return "Erro ao cadastrar produto", 400
        except Exception as e:
            return f"Erro ao cadastrar: {str(e)}", 500

    return render_template('cadastro_produto.html')

if __name__ == '__main__':
    app.run(debug=True)