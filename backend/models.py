from config import db

class User(db.Model):
    username = db.Column(db.String(16), unique=True, nullable=False, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    
    # One-to-many relationship with items
    items = db.relationship('Item', backref='user', lazy=True)
    # One-to-many relationship with receipts as uploader
    receipts = db.relationship('Receipt', backref='uploader', lazy=True)

    def to_json(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'items': [item.to_json() for item in self.items]
        }

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign key to link uploader (user who uploaded the receipt)
    uploader_username = db.Column(db.String(16), db.ForeignKey('user.username'), nullable=False)
    
    # One-to-many relationship with items
    items = db.relationship('Item', backref='receipt', lazy=True, cascade="all, delete-orphan")

    def to_json(self):
        return {
            'id': self.id,
            'uploader': self.uploader.to_json() if self.uploader else None,
            'items': [item.to_json() for item in self.items],
            'users': list({item.user.to_json() for item in self.items if item.user})
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)
    username = db.Column(db.String(16), db.ForeignKey('user.username'), nullable=True)  # Allows item without a specific user
    paid = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'receipt_id': self.receipt_id,
            'username': self.username,
            'paid': self.paid
        }
