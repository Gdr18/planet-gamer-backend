from flask import Blueprint, request, jsonify

from ..database.db import ma, db, admin_list, bcrypt
from ..models.user_model import User

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'admin', 'surnames', 'phone_number')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user = Blueprint('user', __name__)

@user.route('/user', methods=["POST"])
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

    password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = User(email, name, password, admin, surnames, phone_number)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.id)

    return user_schema.jsonify(user)

@user.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@user.route("/user/<id>", methods=["GET", "DELETE", "PUT"])
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
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        user.surnames = surnames
        user.phone_number = phone_number
        user.admin = admin

        db.session.commit()   
        return user_schema.jsonify(user)
