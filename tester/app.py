from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def home():
    return "Bem-vindo à API Flask!"

# Rota para receber dados via GET
@app.route('/api/data', methods=['GET'])
def get_data():
    # Parâmetros da URL (query string)
    name = request.args.get('name', 'Visitante')
    return jsonify({"message": f"Olá, {name}!"})

# Rota para receber dados via POST
@app.route('/api/data', methods=['POST'])
def post_data():
    # Corpo da requisição (JSON)
    data = request.json
    return jsonify({"received_data": data})

if __name__ == '__main__':
    app.run(debug=True)