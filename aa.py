import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar as variáveis do arquivo .env
load_dotenv('python.env')

# Obter a URL e a chave do Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Criar o cliente do Supabase
supabase: Client = create_client(url, key)

response = (
    supabase.table("Clientes")
    .select("*")
    .execute()
)

if response.data:
    print("Dados da tabela 'Clientes':")
    for row in response.data:
        print(row)
else:
    print("Nenhum dado encontrado na tabela 'Clientes'.")