import json
from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from core.models import Product, db

# Adding a simple blueprint, it might be related to a specific view in the real world
api = Blueprint('api', __name__)

INTERNAL_SERVER_ERROR = {'message': 'An internal error occurred.'}


@api.route('/v1/products', methods=['GET'])
def get_products():
    """
    Endpoint to retrieve all the stored products.

    :return: all the products along with their information as a json
    """
    try:
        # Retrieves all the products following the ascending order of the product.id
        all_products = Product.query.order_by(Product.id.asc()).all()
        # Gets a serialized version for the retrieved products
        serialized_products = [p.as_dict() for p in all_products]
        # Returns the result
        return jsonify(serialized_products)
    except (TypeError, ValueError, IntegrityError):
        # Returns the 500 Internal server error if something bad occurred
        # (e.g.: exceptions in JSON serialization)
        return jsonify(INTERNAL_SERVER_ERROR), 500


@api.route('/v1/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """
    Endpoint to retrieve the information related to a specific product.

    :param: the id of the product for which we should return the information
    :return: all the information related to the asked product if the product exists, else 404
    """
    product = Product.query.get_or_404(product_id)
    return jsonify(product.as_dict())
