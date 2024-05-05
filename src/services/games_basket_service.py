from flask import Blueprint, request

from ..database.db import db
from ..models.basket_model import Basket
from ..models.game_model import Game
from ..routes.game_route import games_schema

games_basket = Blueprint("games_basket", __name__)


@games_basket.route("/games-basket/<basket_user_id>", methods=["GET"])
def select_basket(basket_user_id):
    if request.method == "GET":
        games_and_baskets = (
            db.session.query(Basket, Game)
            .join(Basket)
            .filter_by(basket_user_id=basket_user_id)
            .all()
        )

        games = []

        for basket, game in games_and_baskets:
            game = Game.query.get(game.id)
            game.qty = basket.qty
            games.append(game)

        return games_schema.jsonify(games)
