from flask import Blueprint, request, jsonify

from ..database.db import ma, db
from ..models.basket_model import Basket
from ..models.game_model import Game
from .game_route import games_schema

basket = Blueprint("basket", __name__)


class BasketSchema(ma.Schema):
    class Meta:
        fields = ("id", "qty", "basket_game_id", "basket_user_id")


basket_schema = BasketSchema()
baskets_schema = BasketSchema(many=True)


@basket.route("/baskets", methods=["POST", "GET"])
def select_baskets():
    if request.method == "GET":
        if request.method == "GET":
            all_baskets = Basket.query.all()
            result = baskets_schema.dump(all_baskets)
            return jsonify(result)

    if request.method == "POST":
        for basket in request.json:
            qty = basket["qty"]
            basket_game_id = basket["basket_game_id"]
            basket_user_id = basket["basket_user_id"]

            new_basket = Basket(qty, basket_game_id, basket_user_id)

            db.session.add(new_basket)
            db.session.commit()
        baskets = Basket.query.filter_by(basket_user_id=basket_user_id).all()
        result = baskets_schema.dump(baskets)

        return jsonify(result)


@basket.route("/baskets/<basket_user_id>", methods=["GET", "DELETE"])
def select_basket(basket_user_id):
    if request.method == "GET":
        all_items = (
            db.session.query(Basket, Game)
            .join(Basket)
            .filter_by(basket_user_id=basket_user_id)
            .all()
        )

        games = []

        for basket, game in all_items:
            game = Game.query.get(game.id)
            game.qty = basket.qty
            games.append(game)
      
        return games_schema.jsonify(games)

    if request.method == "DELETE":
        db.session.query(Basket).filter(
            Basket.basket_user_id == basket_user_id
        ).delete()
        db.session.commit()
        return f"The basket items were successfully deleted"


@basket.route(
    "/basket/<int:basket_game_id>/<int:basket_user_id>",
    methods=["POST", "PUT", "DELETE"],
)
def select_item_basket(basket_game_id, basket_user_id):
    if request.method == "POST":
        qty = request.json["qty"]

        new_basket = Basket(qty, basket_game_id, basket_user_id)

        db.session.add(new_basket)
        db.session.commit()

        basket = Basket.query.get(new_basket.id)

        return basket_schema.jsonify(basket)

    if request.method == "PUT":
        basket = (
            db.session.query(Basket)
            .filter(
                Basket.basket_user_id == basket_user_id,
                Basket.basket_game_id == basket_game_id,
            )
            .first()
        )
        qty = request.json["qty"]
        print(basket)

        basket.qty = qty
        basket.basket_user_id = basket_user_id
        basket.basket_game_id = basket_game_id

        db.session.commit()
        return basket_schema.jsonify(basket)

    if request.method == "DELETE":
        db.session.query(Basket).filter(
            Basket.basket_user_id == basket_user_id,
            Basket.basket_game_id == basket_game_id,
        ).delete()
        db.session.commit()

        return f"The basket item was successfully deleted"
