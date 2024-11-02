from flask import request, jsonify
from config import app, db
from models import User
from gpt import chat

# U S E R S
####################################################################################################
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.to_json(), users))

    return jsonify({"users": json_users})

@app.route('/api/create_user', methods=['POST'])
def create_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')

    if not first_name or not last_name or not email:
        return jsonify({"error": "Missing data"}), 400
    
    new_user = User(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/update_user/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    user.first_name = data.get('firstName', user.first_name)
    user.last_name = data.get('lastName', user.last_name)
    user.email = data.get('email', user.email)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({"message": "User updated successfully"}), 201

@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200
####################################################################################################

# R E C E I P T S
####################################################################################################
####################################################################################################

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)