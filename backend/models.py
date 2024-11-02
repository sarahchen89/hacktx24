from config import db

# Association table for the many-to-many relationship between Users and Receipts
user_receipt_association = db.Table('user_receipt',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('receipt_id', db.Integer, db.ForeignKey('receipt.id'), primary_key=True)
)

# User has many Receipts
# User has many Items
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    receipts = db.relationship('Receipt', secondary=user_receipt_association, back_populates='users')
    items = db.relationship('Item', backref='user', lazy=True, foreign_keys='Item.user_id')

    def to_json(self, include_receipts=True):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            # include_receipts is a flag to prevent infinite recursion
            'receipts': [receipt.to_json(include_users=False) for receipt in self.receipts] if include_receipts else [],
            'items': [item.to_json() for item in self.items]
        }


# Receipt has many Users
# Receipt has many Items
class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('Item', backref='receipt', lazy=True)
    users = db.relationship('User', secondary=user_receipt_association, back_populates='receipts')

    def to_json(self, include_users=True):
        return {
            'id': self.id,
            'items': [item.to_json() for item in self.items],
            # include_users is a flag to prevent infinite recursion
            'users': [user.to_json(include_receipts=False) for user in self.users] if include_users else []
        }

# Item has one Receipt
# Item has zero or one User
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # allow an Item not to be assigned to a User

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'receipt_id': self.receipt_id,
            'user_id': self.user_id
        }