import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar configurações do Supabase
load_dotenv('python.env')

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

class ServidorCadastro(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/cadastrar":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode("utf-8"))

            cpf_cnpj = data.get("cpf_cnpj")
            nome = data.get("nome")
            email = data.get("email")

            if not cpf_cnpj or not nome or not email:
                self.enviar_resposta(400, {"error": "Todos os campos são obrigatórios"})
                return

            try:
                response = supabase.table("Clientes").insert({
                    "cpf_cnpj": cpf_cnpj,
                    "nome": nome,
                    "email": email,
                }).execute()

                self.enviar_resposta(200, {"success": "Usuário cadastrado com sucesso!"})
            except Exception as e:
                self.enviar_resposta(500, {"error": str(e)})

    def enviar_resposta(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

# Iniciar o servidor local
def iniciar_servidor():
    servidor = HTTPServer(("127.0.0.1", 8000), ServidorCadastro)
    print("Servidor rodando em http://127.0.0.1:8000")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()
