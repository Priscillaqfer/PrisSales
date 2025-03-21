from flask import Flask, render_template, request, redirect, url_for, flash
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
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta_temporal')  # Defina a chave secreta para Flask

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
        telefone = request.form['telefone']
        tipo_telefone = request.form['tipo_telefone']
        nome_rua = request.form['nome_rua']
        numero = request.form['numero']
        cidade = request.form['cidade']
        estado = request.form['estado']
        cep = request.form['cep']
        tipo_endereco = request.form['tipo_endereco']

        try:
            # Inserir os dados na tabela "Clientes"
            response_client = supabase.table('Clientes').insert({
                "cpf_cnpj": cpf_cnpj,
                "nome": nome,
                "email": email
            }).execute()

            if not response_client.data:
                return "Erro ao cadastrar cliente", 400

            # Inserir os dados na tabela "Clientes_Endereco"
            response_endereco = supabase.table('Clientes_Endereco').insert({
                "cpf_cnpj": cpf_cnpj,
                "rua": nome_rua,
                "numero": numero,
                "cidade": cidade,
                "estado": estado,
                "cep": cep,
                "tipo": tipo_endereco
            }).execute()

            if not response_endereco.data:
                return "Erro ao cadastrar endereço", 400

            # Inserir os dados na tabela "Clientes_Telefone"
            response_telefone = supabase.table('Clientes_Telefone').insert({
                "cpf_cnpj": cpf_cnpj,
                "telefone": telefone,
                "tipotelefone": tipo_telefone
            }).execute()

            if not response_telefone.data:
                return "Erro ao cadastrar telefone", 400

            # Se tudo estiver correto, redireciona para a página principal
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('index'))  # Redirecionar para a página principal após o cadastro

        except Exception as e:
            return f"Erro ao cadastrar cliente: {str(e)}", 500

    return render_template('cadastro_cliente.html')

# Rota para buscar CPF e retornar os dados do cliente para alteração

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
             return render_template('alterar_cliente_dados_pessoais.html', cliente=cliente)
         else:
             return "Cliente não encontrado", 404
 
     # Se for GET, exibe o formulário para inserir o CPF
     return render_template('alterar_cliente_buscarcpf.html')
 
 # Rota para alterar os dados pessoais
@app.route('/alterar_cliente_dados_pessoais/<cpf>', methods=['GET', 'POST'])
def alterar_cliente_dados_pessoais(cpf):
     if request.method == 'POST':
         nome = request.form['nome']
         email = request.form['email']
         cpf_cnpj = request.form['cpf_cnpj']  # Este campo será apenas para leitura
 
         try:
             # Atualizar os dados no Supabase
             response = supabase.table('Clientes').update({
                 "nome": nome,
                 "email": email
             }).eq("cpf_cnpj", cpf_cnpj).execute()
 
             if response.data:
                 # Se a atualização for bem-sucedida, redireciona de volta para a tela principal
                 flash('Dados atualizados com sucesso!', 'success')
                 return redirect(url_for('index'))
             else:
                 flash('Erro ao atualizar os dados.', 'error')
                 return redirect(url_for('alterar_cliente_dados_pessoais', cpf=cpf_cnpj))
 
         except Exception as e:
             flash(f'Erro ao atualizar os dados: {str(e)}', 'error')
             return redirect(url_for('alterar_cliente_dados_pessoais', cpf=cpf_cnpj))
 
     # Se for um GET, exibe os dados atuais do cliente
     response = supabase.table('Clientes').select('*').eq('cpf_cnpj', cpf).execute()
 
     if response.data:
         cliente = response.data[0]
         return render_template('alterar_cliente_dados_pessoais.html', cliente=cliente)
     else:
         flash('Cliente não encontrado.', 'error')
         return redirect(url_for('index'))
     
if __name__ == '__main__':
     app.run(debug=True)

     #JJJJ