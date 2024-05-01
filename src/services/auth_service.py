from flask import Blueprint, request, session

from ..database.db import db, bcrypt, admin_list
from ..models.user_model import User
from ..routes.user_route import user_schema

auth = Blueprint('auth', __name__)

@auth.route('/auth', methods=["GET", "POST", "DELETE"])
def login():
    if request.method == "POST": 
        email = request.json['email']
        password = request.json['password']
        name = request.json['name']    

        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            if bcrypt.check_password_hash(user_exists.password, password) == False:
                return {"error": "Contraseña equivocada"}, 401
            else:
                session['email'] = email
                return user_schema.jsonify(user_exists)
        elif user_exists == None and name != "":
            if admin_list.count(email):
                admin = True
            else:
                admin = False

            password = bcrypt.generate_password_hash(password).decode('utf-8')
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