from ..database.db import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Numeric(precision=10, scale=2, asdecimal=False), unique=False, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(40), nullable=False)
    order_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, total, qty, order_user_id, date):
        self.total = total
        self.qty = qty
        self.order_user_id = order_user_id
        self.date = date