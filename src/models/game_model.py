from ..utils.instantiations import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(1500), unique=True, nullable=False)
    platform = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    pegi = db.Column(db.String(3), nullable=False)
    release = db.Column(db.String(4), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    img = db.Column(db.String(150), unique=True, nullable=False)
    qty = db.Column(db.Integer, default=1, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    details = db.relationship('OrderDetails', backref='game', lazy=True)
    
    def __init__(self, title, description, platform, gender, pegi, release, price, img):
        self.title = title
        self.description = description
        self.platform = platform
        self.gender = gender
        self.pegi = pegi
        self.release = release
        self.price = price
        self.img = img
