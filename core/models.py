from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.types as types

# Connects SQLAlchemy
db = SQLAlchemy()


# Python3 classes doesn't need to ineherit from object
class DictReprMixin:
    """
    Mixin providing a common serialization method to all the objects.
    """

    def as_dict(self):
        """
        Builds a dictionary for the model. This makes the model json-izable without problems.

        :return: a serialized dictionary
        """
        # Makes a dict from just the columns of the model (so bypassing meta-information from SQLAlchemy)
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Currency(DictReprMixin, db.Model):
    """
    Data model for the currency table. Check https://en.wikipedia.org/wiki/Currency
    for all the available currencies.
    """

    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True)
    iso_code = db.Column(db.String(3), unique=True, nullable=False)
    description = db.Column(db.String(100))
    symbol = db.Column(db.String(3))

    def __init__(self, iso_code, description=None, symbol=None):
        self.iso_code = iso_code
        self.description = description
        self.symbol = symbol


class StringableFloat(types.TypeDecorator):
    """
    Since the price should be provided as a string and should be inserted as a string,
    this class actually converts the price to float on his way in and converts it
    to string on it's way out.
    Note: an alternative solution would have defined the price column directly as a
    string. In this solution has been defined as a float since future features may
    require aggregate operations on prices, and it won't be possible with prices as
    strings.
    """

    impl = types.Float

    def process_bind_param(self, value, dialect):
        return float(value)

    def process_result_value(self, value, dialect):
        return '{0:.2f}'.format(value)

    def copy(self, **kw):
        return StringableFloat(self.impl.asdecimal)


class Product(DictReprMixin, db.Model):
    """
    Data model for the products table.
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    # Defining the max length of the string is optional with postgres but in this case
    # we still want to provide a reasonable value for the max length in order not to waste resources
    # TODO: adjust the max length parameter for the product name according to the specs in the real world
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(StringableFloat, nullable=False)
    # The currency has been temporarily defined nullable because the POST/PUT requests don't take
    # into account the currency.
    # TODO: make it nullable when proper tests will be available
    currency_iso = db.Column(db.String(3), db.ForeignKey('currencies.iso_code'), nullable=True)

    def __init__(self, name, price, currency_iso=None):
        self.name = name
        self.price = price
        self.currency_iso = currency_iso
