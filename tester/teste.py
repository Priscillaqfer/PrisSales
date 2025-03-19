import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv('python.env')

# Obter a URL e a chave do Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Criar cliente do Supabase
supabase: Client = create_client(url, key)

# Consultar: response = supabase.table("Clientes").select("*").execute()

cpf= "70927982481"


# Inserção de dados na tabela "Clientes"
response = supabase.table("Clientes").select("*").eq("cpf_cnpj", cpf).execute()

# Exibir a resposta
print("Resposta da consulta:", response)

# Verificar se a consulta retornou dados
if response.data:
    print("Dados da tabela 'Clientes':")
    for row in response.data:
        print(row)
else:
    print("Nenhum dado encontrado na tabela 'Clientes'.")