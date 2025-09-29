from flask import Flask, request, jsonify

usuario = []
usuario_id = 1

app = Flask(__name__)

@app.route("/users", methods=["POST"])
def save_tarefa():
    global usuario_id
    data = request.get_json()
    new_user = {
        "id": usuario_id,
        "nome": data.get("nome"),
        "cpf": data.get("cpf"),
        "cadastro": False
    }
    usuario.append(new_user)
    usuario += 1
    return jsonify({"message":"Usuario Criado com sucesso!","user":new_user}),201

app.run()