from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

# Aquí se pueden añadir los usuarios admin.
admin_list = ["gador@gmail.com"]
