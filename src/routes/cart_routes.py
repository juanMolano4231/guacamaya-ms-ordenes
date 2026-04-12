from flask import Blueprint
from src.controllers.cart_controller import *
from src.middleware.auth import authenticate
from src.middleware.authorize import authorize

cart_routes = Blueprint("cart_routes", __name__)

cart_routes.route("/cart", methods=["GET"])(authenticate(get_cart))
cart_routes.route("/cart/items", methods=["POST"])(authenticate(add_item_controller))
cart_routes.route("/cart/items/<int:item_id>", methods=["PUT"])(authenticate(update_item_controller))
cart_routes.route("/cart/items/<int:item_id>", methods=["DELETE"])(authenticate(delete_item_controller))
cart_routes.route("/cart/total", methods=["GET"])(authenticate(get_total_controller))

cart_routes.route("/admin/carts", methods=["GET"])(
    authenticate(authorize(["ADMIN"])(get_all_carts_controller))
)
cart_routes.route("/cart", methods=["DELETE"])(
    authenticate(delete_cart_controller)
)
cart_routes.route("/admin/carts/<int:cart_id>", methods=["DELETE"])(
    authenticate(authorize(["ADMIN"])(admin_delete_cart_controller))
)