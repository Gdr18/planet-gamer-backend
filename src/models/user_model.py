from ..database.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    surnames = db.Column(db.String(40))
    phone_number = db.Column(db.String(9))
    addresses = db.relationship('Address', cascade="all, delete", backref='user', lazy=True)
    orders = db.relationship('Order', cascade="all, delete", backref='user', lazy=True)
    
    def __init__(self, email, name, password, admin, surnames="", phone_number=""):
        self.email = email
        self.name = name
        self.password = password
        self.admin = admin
        self.surnames = surnames
        self.phone_number = phone_number