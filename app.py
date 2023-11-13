from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://unshljxralxgnh:abe397475060bc7a68310980bd6b34d1d79f43e2ddc6750b79043d713cb36441@ec2-63-34-69-123.eu-west-1.compute.amazonaws.com:5432/d906uc31ddn6k'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///planet_gamer.db'
app.config['SECRET_KEY'] = 'mis_michis'
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = 10000
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

db = SQLAlchemy(app)
ma = Marshmallow()

CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

def begin():
    with app.app_context():
        db.create_all()
    
app.app_context().push()

admin_list = ["gador@gmail.com"]    #Aquí se pueden añadir los usuarios admin.

#SCHEMAS

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'admin', 'surnames', 'phone_number')

class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id', 'street', 'second_line_street', 'postal_code', 'city', 'address_user_id')

class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'platform', 'platform_url', 'gender', 'pegi', 'release', 'price', 'img', 'qty')

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'total', 'qty', 'order_user_id', 'date', 'order_address_id')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

game_schema = GameSchema()
games_schema = GameSchema(many=True)

#MODELS

#user

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    admin = db.Column(db.Boolean, unique=False, nullable=False)
    surnames = db.Column(db.String(40), unique=False, nullable=True)
    phone_number = db.Column(db.String(9), unique=False, nullable=True)
    addresses = db.relationship('Address', cascade="all, delete", backref='user', lazy=True)
    orders = db.relationship('Order', cascade="all, delete", backref='user', lazy=True)
    
    def __init__(self, email, name, password, admin, surnames="", phone_number=""):
        self.email = email
        self.name = name
        self.password = password
        self.admin = admin
        self.surnames = surnames
        self.phone_number = phone_number

#address

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(80), nullable=False)
    second_line_street = db.Column(db.String(40), nullable=True)
    postal_code = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    address_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __init__(self, street, second_line_street, postal_code, city, address_user_id):
        self.street = street
        self.second_line_street = second_line_street
        self.postal_code = postal_code
        self.city = city
        self.address_user_id = address_user_id

#order

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Numeric(precision=10, scale=2, asdecimal=False), unique=False, nullable=False)
    qty = db.Column(db.Integer, unique=False, nullable=False)
    date = db.Column(db.String(40), nullable=False)
    order_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, total, qty, order_user_id, date):
        self.total = total
        self.qty = qty
        self.order_user_id = order_user_id
        self.date = date

#game

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(1500), unique=True, nullable=False)
    platform = db.Column(db.String(20), unique=False, nullable=False)
    platform_url = db.Column(db.String(20), unique=False, nullable=False)
    gender = db.Column(db.String(10), unique=False, nullable=False)
    pegi = db.Column(db.String(3), unique=False, nullable=False)
    release = db.Column(db.String(4), unique=False, nullable=False)
    price = db.Column(db.Numeric(precision=4, scale=2), unique=False, nullable=False)
    img = db.Column(db.String(150), unique=True, nullable=False)
    qty = db.Column(db.Integer, unique=False, nullable=False)
    
    def __init__(self, title, description, platform, platform_url, gender, pegi, release, price, img, qty=1 ):
        self.title = title
        self.description = description
        self.platform = platform
        self.platform_url = platform_url
        self.gender = gender
        self.pegi = pegi
        self.release = release
        self.price = price
        self.img = img
        self.qty = qty

#ROUTES

#users routes

@app.route('/user', methods=["POST"])
def add_user():
    name = request.json['name']
    password = request.json['password']
    email = request.json['email']
    phone_number = request.json['phone_number']
    surnames = request.json['surnames']

    if admin_list.count(email):
        admin = True
    else:
        admin = False

    password = bcrypt.generate_password_hash(password)
    
    new_user = User(email, name, password, admin, surnames, phone_number)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)

@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route("/user/<id>", methods=["GET", "DELETE", "PUT"])
def select_user(id):
    if request.method == "GET":
        user = User.query.get(id)
        return user_schema.jsonify(user)

    if request.method == "DELETE":
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()

        return f'The user {id} was successfully deleted'

    if request.method == "PUT":
        user = User.query.get(id)
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        surnames = request.json['surnames']
        phone_number = request.json['phone_number']
        admin = request.json['admin']

        user.name = name
        user.email = email

        if password != "" and not bcrypt.check_password_hash(user.password, password):
            user.password = bcrypt.generate_password_hash(password)

        user.surnames = surnames
        user.phone_number = phone_number
        user.admin = admin

        db.session.commit()   
        return user_schema.jsonify(user)
    
#logins routes

@app.route('/login', methods=["GET", "POST", "DELETE"])
def login():
    if request.method == "POST": 
        email = request.json['email']
        password = request.json['password']
        name = request.json['name']    

        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            if not bcrypt.check_password_hash(user_exists.password, password):
                return {"error": "Contraseña equivocada"}, 401
            else:
                session['email'] = email
                return user_schema.jsonify(user_exists)
        elif user_exists == None and name != "":
            if admin_list.count(email):
                admin = True
            else:
                admin = False

            password = bcrypt.generate_password_hash(password)
            new_user = User(email, name, password, admin)

            db.session.add(new_user)
            db.session.commit()

            session['email'] = email

            user = User.query.get(new_user.id)
            return user_schema.jsonify(user)
        else:
            return {"name": name}
    if request.method == "GET":
        sessionEmail = session.get("email", "")
        if sessionEmail == "":
            return {"loggedIn": False}
        else:
            emailSession = session["email"]
            user = User.query.filter_by(email=emailSession).first()
            return {"loggedIn": True, "id": user.id}
    if request.method == "DELETE":
        session.pop("email", None)
        return {"loggedOut": True}
    
#addresses routes

@app.route('/address/<address_user_id>', methods=["POST"])
def add_address(address_user_id):
    street = request.json['street']
    second_line_street = request.json['second_line_street']
    postal_code = request.json['postal_code']
    city = request.json['city']
    
    user_address = Address.query.filter_by(address_user_id=address_user_id).first()

    if user_address != None:
        user_address.street = street
        user_address.second_line_street = second_line_street
        user_address.postal_code = postal_code
        user_address.city = city

        db.session.commit()
        return address_schema.jsonify(user_address)
    else:
        new_address = Address(street, second_line_street, postal_code, city, address_user_id)

        db.session.add(new_address)
        db.session.commit()

        address = Address.query.get(new_address.id)

        return address_schema.jsonify(address)

@app.route("/address-user/<address_user_id>", methods=["GET"])
def get_addresses(address_user_id):
    address = Address.query.filter_by(address_user_id=address_user_id).first()
    return address_schema.jsonify(address)

@app.route("/address/<id>", methods=["GET", "DELETE", "PUT"])
def select_address(id):
    if request.method == "GET":
        address = Address.query.get(id)
        return address_schema.jsonify(address)
    
    if request.method == "DELETE":
        address = Address.query.get(id)

        db.session.delete(address)
        db.session.commit()
    
        return f'The address {address.id} was successfully deleted'

    if request.method == "PUT":
        address = Address.query.get(id)
        street = request.json['street']
        second_line_street = request.json['second_line_street']
        postal_code = request.json['postal_code']
        city = request.json['city']

        address.street = street
        address.second_line_street = second_line_street
        address.postal_code = postal_code
        address.city = city

        db.session.commit()   
        return address_schema.jsonify(address)
    
@app.route("/addresses", methods=["GET"])
def get_all_addresses():
    all_addresses = Address.query.all()
    result = addresses_schema.dump(all_addresses)
    return jsonify(result)

#games routes

@app.route("/games", methods=["POST", "GET"])
def select_games():
    if request.method  == "POST":
        for game in request.json:
            title = game['title']
            description = game['description']
            platform = game['platform']
            platform_url = game['platform_url']
            gender = game['gender']
            pegi = game['pegi']
            release = game['release']
            price = game['price']
            img = game['img']
            
            new_game = Game(title, description, platform, platform_url, gender, pegi, release, price, img)

            db.session.add(new_game)
            db.session.commit()

        games = Game.query.all()
        result = games_schema.dump(games)

        return jsonify(result)
        
    if request.method == "GET":
        all_games = Game.query.all()
        result = games_schema.dump(all_games)
        return jsonify(result)
    
@app.route("/game", methods=["POST"])
def post_game():
    title = request.json['title']
    description = request.json['description']
    platform = request.json['platform']
    platform_url = request.json['platform_url']
    gender = request.json['gender']
    pegi = request.json['pegi']
    release = request.json['release']
    price = request.json['price']
    img = request.json['img']
    
    new_game = Game(title, description, platform, platform_url, gender, pegi, release, price, img)

    db.session.add(new_game)
    db.session.commit()

    game = Game.query.get(new_game.id)

    return game_schema.jsonify(game)

    
@app.route("/game/<id>", methods=["GET", "PUT", "DELETE"])
def select_game(id):
    if request.method == "GET":
        game = Game.query.get(id)

        return game_schema.jsonify(game)
    
    if request.method == "PUT":
        game = Game.query.get(id)
        title = request.json['title']
        description = request.json['description']
        gender = request.json['gender']
        platform = request.json['platform']
        platform_url = request.json['platform_url']
        pegi = request.json['pegi']
        release = request.json['release']
        price = request.json['price']
        img = request.json['img']

        game.title = title
        game.description = description
        game.gender = gender
        game.platform = platform
        game.platform_url = platform_url
        game.pegi = pegi
        game.release = release
        game.price = price
        game.img = img

        db.session.commit()
        return game_schema.jsonify(game)
    
    if request.method == "DELETE":
        game = Game.query.get(id)
        db.session.delete(game)
        db.session.commit()

        return f'The game {id} was successfully deleted'
    
#orders routes

@app.route("/orders", methods=["GET"])
def select_orders():
    all_orders = Order.query.all()
    result = orders_schema.dump(all_orders)
    return jsonify(result)

@app.route("/orders/<order_user_id>", methods=["GET"])
def get_orders(order_user_id):
    user = User.query.get(order_user_id)
    if user != None:
        orders = user.orders
        return orders_schema.jsonify(orders)
    # else:
    #     return {"status": "NO_ORDERS"}

@app.route("/order/<order_user_id>", methods=["POST"])
def post_order(order_user_id):
    total = request.json['total']
    qty = request.json['qty']

    data = datetime.now()
    date = data.strftime('%d-%m-%Y, %H:%M:%S')
    
    new_order = Order(total, qty, order_user_id, date)

    db.session.add(new_order)
    db.session.commit()

    order = Order.query.get(new_order.id)
    return order_schema.jsonify(order)

@app.route("/order/<id>", methods=["GET", "PUT", "DELETE"])
def select_order(id):
    if request.method == "GET":
        order = Order.query.get(id)

        return order_schema.jsonify(order)
    
    if request.method == "PUT":
        order = Order.query.get(id)
        total = request.json['total']
        qty = request.json['qty']

        order.total = total
        order.qty = qty

        db.session.commit()
        return order_schema.jsonify(order)
    
    if request.method == "DELETE":
        order = Order.query.get(id)

        db.session.delete(order)
        db.session.commit()

        return f'The order {id} was successfully deleted'

if __name__ == '__main__':
   app.run(debug=True)