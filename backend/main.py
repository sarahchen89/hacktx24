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
@app.route('/api/<string:username>/get_uploaded_receipts', methods=['GET'])
def get_uploaded_receipts(username):
    # Verify user exists
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve receipts uploaded by the user
    uploaded_receipts = Receipt.query.filter_by(uploader_username=username).all()
    json_receipts = [receipt.to_json() for receipt in uploaded_receipts]
    return jsonify({"uploaded_receipts": json_receipts})

@app.route('/api/<string:username>/get_assigned_receipts', methods=['GET'])
def get_assigned_receipts(username):
    # Verify user exists
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Find receipts where this user is associated with any item
    assigned_receipts = Receipt.query.join(Item).filter(Item.username == username).all()
    json_receipts = [receipt.to_json() for receipt in assigned_receipts]
    return jsonify({"assigned_receipts": json_receipts})

@app.route('/api/<string:username>/add_receipt', methods=['POST'])
def add_receipt(username):
    # Verify the uploader exists
    uploader = User.query.get(username)
    if not uploader:
        return jsonify({"error": "Uploader not found"}), 404

    # Retrieve and save the receipt file
    receipt = request.files.get('receipt')
    if not receipt:
        return jsonify({"error": "No receipt uploaded"}), 400

    file_path = f"./uploads/{receipt.filename}"
    try:
        receipt.save(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to save receipt file: {str(e)}"}), 500

    # Parse the receipt for items and prices
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

@app.route('/api/<string:username>/<int:receipt_id>/get_items', methods=['GET'])
def get_items(username, receipt_id):
    # Verify if user exists
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if the user is the uploader or has items in the receipt
    receipt = Receipt.query.get(receipt_id)
    if not receipt:
        return jsonify({"error": "Receipt not found"}), 404

    if receipt.uploader_username != username:
        # Check if they have items in this receipt
        user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
        if not user_item_in_receipt:
            return jsonify({"error": "User does not have access to this receipt"}), 403

    # Return all items in the receipt
    items = receipt.items
    json_items = [item.to_json() for item in items]
    return jsonify({"items": json_items})

@app.route('/api/<string:username>/<int:receipt_id>/get_users', methods=['GET'])
def get_users_in_receipt(username, receipt_id):
    # Verify if user exists
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if the user has access to the receipt by being the uploader or having items in the receipt
    receipt = Receipt.query.get(receipt_id)
    if not receipt:
        return jsonify({"error": "Receipt not found"}), 404

    if receipt.uploader_username != username:
        # Check if they have items in this receipt
        user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
        if not user_item_in_receipt:
            return jsonify({"error": "User does not have access to this receipt"}), 403

    # Get unique usernames associated with items in the receipt
    users = {item.username for item in receipt.items if item.username}
    json_users = [User.query.get(u).to_json() for u in users if u]
    return jsonify({"users": json_users})

@app.route('/api/<string:username>/<int:receipt_id>/<int:item_id>/status/<string:pay>', methods=['PATCH'])
def paid_item(username, receipt_id, item_id, pay):
    # Verify if user exists
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if user has access to the receipt
    user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
    if not user_item_in_receipt:
        return jsonify({"error": "User does not have access to this receipt"}), 403

    # Verify the item exists and belongs to the receipt
    item = Item.query.get(item_id)
    if not item or item.receipt_id != receipt_id:
        return jsonify({"error": "Item not found for this receipt"}), 404

    # Update item payment status
    item.paid = pay.lower() == 'paid'

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": f"Item marked as {'paid' if item.paid else 'unpaid'} successfully"}), 200

@app.route('/api/<string:username>/<int:receipt_id>/<int:item_id>/payee/<string:username2>', methods=['PATCH'])
def assign_item(username, receipt_id, item_id, username2):
    # Verify if user exists
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if user has access to the receipt
    user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
    if not user_item_in_receipt:
        return jsonify({"error": "User does not have access to this receipt"}), 403

    # Verify the item exists and belongs to the receipt
    item = Item.query.get(item_id)
    if not item or item.receipt_id != receipt_id:
        return jsonify({"error": "Item not found for this receipt"}), 404

    # Verify the payee exists
    payee = User.query.get(username2)
    if not payee:
        return jsonify({"error": "Payee not found"}), 404

    # Update the item's assigned user
    item.username = username2

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Item transferred successfully"}), 200

@app.route('/api/<string:username>/<int:receipt_id>/<int:item_id>/decipher', methods=['GET'])
def decipher_item(username, receipt_id, item_id):
    # Verify if user exists
    user = User.query.get(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if user has access to the receipt
    user_item_in_receipt = Item.query.filter_by(receipt_id=receipt_id, username=username).first()
    if not user_item_in_receipt:
        return jsonify({"error": "User does not have access to this receipt"}), 403

    # Verify the item exists and belongs to the receipt
    item = Item.query.get(item_id)
    if not item or item.receipt_id != receipt_id:
        return jsonify({"error": "Item not found for this receipt"}), 404

    return jsonify({"message": chat(item.name)})
####################################################################################################

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)