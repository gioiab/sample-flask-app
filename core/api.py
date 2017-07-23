import json
from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError
from core.models import Product, db

# Adding a simple blueprint, it might be related to a specific view in the real world
api = Blueprint('api', __name__)

INTERNAL_SERVER_ERROR = {'message': 'An internal error occurred.'}


@api.route('/v1/products')
def get_products():
    """
    Endpoint to retrieve all the stored products.
    """
    try:
        # Retrieves all the products following the ascending order of the product.id
        all_products = Product.query.order_by(Product.id.asc()).all()
        # Gets a serialized version for the retrieved products
        serialized_products = [p.as_dict() for p in all_products]
        # Returns the result
        return jsonify(serialized_products)
    except (TypeError, IntegrityError):
        # Returns the 500 Internal server error if something bad occurred
        return jsonify(INTERNAL_SERVER_ERROR), 500

