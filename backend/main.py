from flask import request, jsonify
from config import app, db
from models import User, Receipt, Item
from gpt import chat
from receipt_scan import parse_receipt

# U S E R S
####################################################################################################
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    json_users = [user.to_json() for user in users]
    return jsonify({"users": json_users})

@app.route('/api/create_user', methods=['POST'])
def create_user():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')

    if not all([first_name, last_name, email, username, password]):
        return jsonify({"error": "Missing data"}), 400

    new_user = User(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/update_user/<string:username>', methods=['PATCH'])
def update_user(username):
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "User updated successfully"}), 200

@app.route('/api/delete_user/<string:username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200
####################################################################################################

# R E C E I P T S
####################################################################################################
@app.route('/api/<string:username>/get_receipts', methods=['GET'])
def get_receipts(username):
    # Retrieve all receipts in which the user has items
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Find receipts where this user is associated with any item
    user_receipts = Receipt.query.join(Item).filter(Item.username == username).all()
    json_receipts = [receipt.to_json() for receipt in user_receipts]
    return jsonify({"receipts": json_receipts})

@app.route('/api/<string:username>/add_receipt', methods=['POST'])
def add_receipt(username):
    # Verify the uploader (user) exists
    uploader = User.query.get(username)
    if not uploader:
        return jsonify({"error": "Uploader not found"}), 404

    # Retrieve and save the receipt file
    receipt = request.files.get('receipt')
    if not receipt:
        return jsonify({"error": "No receipt uploaded"}), 400

    receipt.save(f"uploads/{receipt.filename}")
    data = parse_receipt(receipt.filename)
    if not data:
        return jsonify({"error": "Receipt could not be parsed"}), 400

    items, prices = data
    if len(items) != len(prices):
        return jsonify({"error": "Data mismatch between items and prices"}), 400

    # Create new Receipt with uploader information
    new_receipt = Receipt(uploader_username=username)
    db.session.add(new_receipt)

    # Add items to the new receipt
    for name, price in zip(items, prices):
        item = Item(name=name, price=price, receipt_id=new_receipt.id)
        db.session.add(item)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Receipt and items added successfully", "receipt": new_receipt.to_json()}), 201

@app.route('/api/<string:username>/get_items/<int:receipt_id>', methods=['GET'])
def get_items(username, receipt_id):
    # Check if the user has items in the receipt
    user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
    if not user_item_in_receipt:
        return jsonify({"error": "User does not have access to this receipt"}), 403

    receipt = Receipt.query.get(receipt_id)
    if not receipt:
        return jsonify({"error": "Receipt not found"}), 404

    # Return all items in the receipt
    items = receipt.items
    json_items = [item.to_json() for item in items]
    return jsonify({"items": json_items})

@app.route('/api/<string:username>/<int:receipt_id>/<int:item_id>/status/<string:pay>', methods=['PATCH'])
def paid_item(username, receipt_id, item_id, pay):
    user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
    if not user_item_in_receipt:
        return jsonify({"error": "User does not have access to this receipt"}), 403

    item = Item.query.get(item_id)
    if not item or item.receipt_id != receipt_id:
        return jsonify({"error": "Item not found for this receipt"}), 404

    item.paid = pay.lower() == 'paid'

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": f"Item marked as {'paid' if item.paid else 'unpaid'} successfully"}), 200

@app.route('/api/<string:username>/<int:receipt_id>/<int:item_id>/payee/<string:username2>', methods=['PATCH'])
def assign_item(username, receipt_id, item_id, username2):
    user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
    if not user_item_in_receipt:
        return jsonify({"error": "User does not have access to this receipt"}), 403

    item = Item.query.get(item_id)
    if not item or item.receipt_id != receipt_id:
        return jsonify({"error": "Item not found for this receipt"}), 404

    payee = User.query.get(username2)
    if not payee:
        return jsonify({"error": "Payee not found"}), 404

    item.username = username2

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Item transferred successfully"}), 200

@app.route('/api/<string:username>/<int:receipt_id>/<int:item_id>/decipher', methods=['GET'])
def decipher_item(username, receipt_id, item_id):
    user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
    if not user_item_in_receipt:
        return jsonify({"error": "User does not have access to this receipt"}), 403

    item = Item.query.get(item_id)
    if not item or item.receipt_id != receipt_id:
        return jsonify({"error": "Item not found for this receipt"}), 404

    return jsonify({"message": chat(item.name)})
####################################################################################################

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
