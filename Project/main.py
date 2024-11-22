from flask import Flask, jsonify, request, render_template

app = Flask(__name__, static_url_path='/static/', static_folder='', template_folder='templates')

# Almacenamiento temporal en memoria
users = {}

# Página principal que renderiza el HTML
@app.route("/")
def root():
    return render_template("index.html")

# Endpoint para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([
        {"id": uid, "name": user["name"], "telefono": user["telefono"]}
        for uid, user in users.items()
    ])
                                                            
# Endpoint para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = str(len(users) + 1)  # Generar un ID simple basado en el conteo
    name = data.get("name", "Sin nombre")
    telefono = data.get("telefono", "Sin teléfono")
    
    # Guardar usuario en el diccionario
    users[user_id] = {"name": name, "telefono": telefono}
    return jsonify({"id": user_id, "name": name, "telefono": telefono}), 201

# Endpoint para actualizar un usuario
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if user_id not in users:
        return jsonify({"error": "Usuario no encontrado"}), 404

    users[user_id]["name"] = data.get("name", users[user_id]["name"])
    users[user_id]["telefono"] = data.get("telefono", users[user_id]["telefono"])
    return jsonify(users[user_id]), 200

# Endpoint para borrar un usuario
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"status": "Usuario eliminado", "id": user_id}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
