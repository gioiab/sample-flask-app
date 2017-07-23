import json
import unittest
from core.models import Currency, Product
from main_app import create_app, db


class APITestCase(unittest.TestCase):
    """
    This class collects all the necessary test cases for the api.py module implementing
    the REST APIs to access and modify products.
    """
    def create_test_tables(self):
        """
        Creates the current model on the testing database and inserts some
        well-known sample data.
        """
        # Binds the app to the current context
        with self.app.app_context():
            # Creates the current model on the testing database
            db.create_all()
            # Adds the test entries to the database with a unique bulk operation
            objects = [
                Currency(iso_code='GBP', description='Pound sterling', symbol='£'),
                Product(name='Lavender heart', price=9.25, currency_iso='GBP'),
                Product(name='Personalised cufflinks', price=45., currency_iso='GBP'),
                Product(name='Kids T-shirt', price=19.95, currency_iso='GBP')
            ]
            db.session.bulk_save_objects(objects)
            db.session.commit()

    def setUp(self):
        """
        Sets up the test application, client and database.
        """
        self.app = create_app(object_config='config.TestingConfig')
        self.client = self.app.test_client
        self.create_test_tables()

    def test_valid_get_products(self):
        """
        Tests the /v1/products endpoint.
        """
        res = self.client().get('/v1/products')
        self.assertEqual(res.status_code, 200)
        products = json.loads(res.get_data(as_text=True))
        self.assertEqual(len(products), 3)
        self.assertEqual(products[0]['id'], 1)
        self.assertEqual(products[0]['name'], 'Lavender heart')
        self.assertEqual(products[0]['price'], '9.25')
        self.assertEqual(products[1]['id'], 2)
        self.assertEqual(products[1]['name'], 'Personalised cufflinks')
        self.assertEqual(products[1]['price'], '45.00')
        self.assertEqual(products[2]['id'], 3)
        self.assertEqual(products[2]['name'], 'Kids T-shirt')
        self.assertEqual(products[2]['price'], '19.95')

    def tearDown(self):
        """
        Teardowns all the initialized objects/structures.
        """
        with self.app.app_context():
            # Drops all tables
            db.session.remove()
            db.drop_all()
            db.session.commit()

# Makes the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
