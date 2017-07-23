from flask_sqlalchemy import SQLAlchemy

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
        # Makes a dict from just the columns of the model (so bypassing meta-information from
        # SQLAlchemy)
        dict_from_columns = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # Since the price should be provided as a string this methods does the conversion
        # Note: an alternative solution would have defined the price column directly as a
        # string. In this solution has been defined as a float since future features may
        # require aggregate operations on prices, and it won't be possible with prices as
        # strings.
        if isinstance(self, Product):
            dict_from_columns['price'] = '{0:.2f}'.format(dict_from_columns['price'])
        return dict_from_columns


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


class Product(DictReprMixin, db.Model):
    """
    Data model for the products table.
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    # Defining the max length of the string is optional with postgres
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency_iso = db.Column(db.String(3), db.ForeignKey('currencies.iso_code'), nullable=False)

    def __init__(self, name, price, currency_iso):
        self.name = name
        self.price = price
        self.currency_iso = currency_iso
