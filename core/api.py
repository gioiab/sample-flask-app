from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from core.models import Product, db

# Adding a simple blueprint, it might be related to a specific view in the real world
api = Blueprint('api', __name__)

INTERNAL_SERVER_ERROR_MESSAGE = {'message': 'An internal error occurred.'}
BAD_REQUEST_MESSAGE = {'message': 'Bad request.'}
OK_MESSAGE = {'message': 'Operation successful.'}


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
        return jsonify(INTERNAL_SERVER_ERROR_MESSAGE), 500


@api.route('/v1/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def get_product_by_id(product_id):
    """
    Endpoint devoted to:
    - retrieve the information related to a specific product
    - update an existing product
    - delete an existing product

    :param: the id of the product for which we should return the information
    :return: all the information related to the asked/new product if the product exists for GET and PUT,
    just a success message for DELETE - if the product doesn't exist returns 404
    """
    # Gets the product with the given ID or returns 404 if not found
    product = Product.query.get_or_404(product_id)
    if request.method == 'GET':
        return jsonify(product.as_dict())
    elif request.method == 'PUT':
        name = request.form.get('name')
        price = request.form.get('price')
        # If neither the name nor the price are provided we return 400 Bad Request
        if not name and not price:
            return jsonify(BAD_REQUEST_MESSAGE), 400
        else:  # either name or price is present in the request
            try:
                if name:
                    product.name = name
                if price:
                    product.price = price
                db.session.commit()
                return jsonify(product.as_dict()), 200
            except IntegrityError:
                return jsonify(BAD_REQUEST_MESSAGE), 400
    else: # request.method == 'DELETE'
        db.session.delete(product)
        db.session.commit()
        return jsonify(OK_MESSAGE), 200


@api.route('/v1/product', methods=['POST'])
def insert_new_product():
    """
    Endpoint to insert a new product in the database.

    :return: 200 if the request was successful, 400 or 404 in case it was not
    """
    name = request.form.get('name')
    price = request.form.get('price')
    # If either the name or the price isn't provided, return 400 Bad request (we need both!)
    if not name or not price:
        return jsonify(BAD_REQUEST_MESSAGE), 400
    else:
        try:
            new_product = Product(name=name, price=price)
            db.session.add(new_product)
            db.session.commit()
            return jsonify(new_product.as_dict()), 200
        except IntegrityError:
            return jsonify(BAD_REQUEST_MESSAGE), 400
