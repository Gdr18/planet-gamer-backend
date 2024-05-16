from flask import request, Blueprint

from ..database.db import ma, db
from ..models.user_model import User
from ..models.order_model import Order


class OrderSchema(ma.Schema):
    class Meta:
        fields = ("id", "total", "qty", "order_user_id", "date", "order_address_id")


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

order = Blueprint("order", __name__)


@order.route("/orders", methods=["GET"])
def select_orders():
    all_orders = Order.query.all()
    return orders_schema.jsonify(all_orders)


@order.route("/orders/<order_user_id>", methods=["GET"])
def get_orders(order_user_id):
    user = User.query.get(order_user_id)
    if user is not None:
        orders = user.orders
        for order in orders:
            order.date = order.date.strftime("%d-%m-%Y, %H:%M:%S")
        return orders_schema.jsonify(orders)
    else:
        return "User not found"


@order.route("/order", methods=["POST"])
def post_order():
    total = request.json["total"]
    qty = request.json["qty"]
    order_user_id = request.json["order_user_id"]

    new_order = Order(total, qty, order_user_id)

    db.session.add(new_order)
    db.session.commit()

    order = Order.query.get(new_order.id)
    return order_schema.jsonify(order)


@order.route("/order/<id>", methods=["GET", "PUT", "DELETE"])
def select_order(id):
    if request.method == "GET":
        order = Order.query.get(id)
        return order_schema.jsonify(order)

    if request.method == "PUT":
        order = Order.query.get(id)
        total = request.json["total"]
        qty = request.json["qty"]

        order.total = total
        order.qty = qty

        db.session.commit()
        return order_schema.jsonify(order)

    if request.method == "DELETE":
        order = Order.query.get(id)

        db.session.delete(order)
        db.session.commit()

        return f"The order {id} was successfully deleted"
