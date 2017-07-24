#!/usr/bin/env python3
"""
This script tests the CRUD APIs implemented in api.py.
"""

import json
import unittest
from config import configs
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
        self.app = create_app(config=configs['test'])
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

    def test_valid_get_product(self):
        """
        Tests the /v1/product/<product_id> endpoint for a valid GET request.
        """
        # Getting the first product
        res_1 = self.client().get('/v1/product/1')
        self.assertEqual(res_1.status_code, 200)
        product_1 = json.loads(res_1.get_data(as_text=True))
        self.assertEqual(product_1['id'], 1)
        self.assertEqual(product_1['name'], 'Lavender heart')
        self.assertEqual(product_1['price'], '9.25')
        # Getting the second product
        res_2 = self.client().get('/v1/product/2')
        self.assertEqual(res_2.status_code, 200)
        product_2 = json.loads(res_2.get_data(as_text=True))
        self.assertEqual(product_2['id'], 2)
        self.assertEqual(product_2['name'], 'Personalised cufflinks')
        self.assertEqual(product_2['price'], '45.00')
        # Getting the third product
        res_3 = self.client().get('/v1/product/3')
        product_3 = json.loads(res_3.get_data(as_text=True))
        self.assertEqual(product_3['id'], 3)
        self.assertEqual(product_3['name'], 'Kids T-shirt')
        self.assertEqual(product_3['price'], '19.95')

    def test_invalid_get_product(self):
        """
        Tests the /v1/product/<product_id> endpoint for an invalid GET request.
        """
        res = self.client().get('/v1/product/400')
        self.assertEqual(res.status_code, 404)

    def test_valid_insert_product(self):
        """
         Tests the /v1/product endpoint for an valid POST request.
         """
        res_post = self.client().post('/v1/product', data={'name': 'TestName', 'price': '9.93'})
        self.assertEqual(res_post.status_code, 200)
        new_product = json.loads(res_post.get_data(as_text=True))
        res_get = self.client().get('/v1/product/{}'.format(new_product['id']))
        new_product_from_get = json.loads(res_get.get_data(as_text=True))
        self.assertEqual(new_product_from_get['id'], new_product['id'])
        self.assertEqual(new_product_from_get['name'], 'TestName')
        self.assertEqual(new_product_from_get['price'], '9.93')
        self.assertEqual(new_product_from_get['currency_iso'], None)

    def test_valid_update_product(self):
        """
        Tests the /v1/product/<product_id> endpoint for a valid PUT request.
        """
        res_post = self.client().post('/v1/product', data={'name': 'TestName', 'price': '9.93'})
        self.assertEqual(res_post.status_code, 200)
        new_product = json.loads(res_post.get_data(as_text=True))
        # Updates the newly inserted product
        res_put = self.client().put('/v1/product/{}'.format(new_product['id']), data={'name': 'UpdatedTestName'})
        self.assertEqual(res_put.status_code, 200)
        updated_product = json.loads(res_put.get_data(as_text=True))
        self.assertEqual(updated_product['id'], new_product['id'])
        self.assertEqual(updated_product['name'], 'UpdatedTestName')
        self.assertEqual(updated_product['price'], '9.93')
        self.assertEqual(updated_product['currency_iso'], None)

    def test_invalid_update_product(self):
        """
        Tests the /v1/product/<product_id> endpoint for an invalid PUT request.
        """
        res_put = self.client().put('/v1/product/402', data={'name': 'UpdatedTestName'})
        self.assertEqual(res_put.status_code, 404)

    def test_valid_and_invalid_delete_product(self):
        """
        Tests the /v1/product/<product_id> endpoint for both a valid and invalid DELETE request.
        """
        # Tests a valid deletion
        res_del = self.client().delete('/v1/product/3')
        self.assertEqual(res_del.status_code, 200)
        res_get = self.client().get('/v1/product/3')
        self.assertEqual(res_get.status_code, 404)
        # Tests an invalid deletion
        res_del_2 = self.client().delete('/v1/product/3')
        self.assertEqual(res_del_2.status_code, 404)

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
