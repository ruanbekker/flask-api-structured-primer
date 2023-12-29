import os
import unittest
from app import create_app
from database.db import db
from config import TestConfig
from models.product import Product
from services.product_service import ProductService

class AppConfigTestCase(unittest.TestCase):
    """
    Test case for the application's configuration and initialization process.

    This test case ensures that the Flask application correctly loads the appropriate
    configuration settings based on the `FLASK_ENV` environment variable. It tests
    for different environments including development, production, and the default
    configuration.
    """

    def setUp(self):
        """
        Set up method for the test case.

        This method can be used to set up any pre-requisites or common setup
        tasks that are necessary before each test is executed. Currently, this
        method does not perform any setup but can be modified as needed.
        """
        self.app = create_app(TestConfig)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
        Tear down method for the test case.

        This method is executed after each test method to clean up or reset
        any changes made during the test. It can be used to reset environment
        variables or other cleanup tasks.
        """
        self.app_context.pop()

    def test_development_config(self):
        """
        Test to ensure that the application loads the development configuration.

        This test sets the `FLASK_ENV` environment variable to 'development' and
        then initializes the application. It asserts that the application's configuration
        is correctly set for the development environment.
        """
        os.environ['FLASK_ENV'] = 'development'
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app = create_app()
        self.assertEqual(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)

    def test_production_config(self):
        """
        Test to ensure that the application loads the production configuration.

        This test sets the `FLASK_ENV` environment variable to 'production' and
        then initializes the application. It asserts that the application's configuration
        is correctly set for the production environment.
        """
        os.environ['FLASK_ENV'] = 'production'
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app = create_app()
        self.assertEqual(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)

    def test_default_config(self):
        """
        Test to ensure that the application loads the default configuration.

        This test ensures that when the `FLASK_ENV` environment variable is not set
        (or set to an empty string), the application initializes with the default
        configuration. It asserts that the application's configuration matches the expected
        default settings.
        """
        os.environ['FLASK_ENV'] = ''
        os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
        app = create_app()
        self.assertEqual(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)

class ProductModelTestCase(unittest.TestCase):
    """
    Test cases for the Product model.

    Testing Product Model Behavior, tests to ensure that
    it is storing and returning data correctly
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_product_model(self):
        """
        Test the behavior of the Product model.
        """
        product = Product(
            name='Test Product',
            description='A test product',
            price=20.0,
            inventory=50
        )
        db.session.add(product)
        db.session.commit()

        retrieved = Product.query.filter_by(name='Test Product').first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.description, 'A test product')
        self.assertEqual(retrieved.price, 20.0)
        self.assertEqual(retrieved.inventory, 50)

class ProductServiceTestCase(unittest.TestCase):
    """
    Test cases for the ProductService class.

    Testing API Endpoints
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_product_creation(self):
        """
        Test the creation of a product via the API.
        """
        response = self.client.post('/api/product', json={
            'name': 'Test Product',
            'description': 'This is a test product',
            'price': 10.99,
            'inventory': 100
        })
        self.assertEqual(response.status_code, 201)
        product = Product.query.first()
        self.assertIsNotNone(product)
        self.assertEqual(product.name, 'Test Product')

    def test_product_retrieval(self):
        """
        Test the retrieval of a product via the API.
        """
        # Create a product first
        product = Product(name='Test Product', description='Sample', price=10.99, inventory=100)
        db.session.add(product)
        db.session.commit()

        # Now make a GET request to retrieve the product
        response = self.client.get(f'/api/product/{product.id}')
        self.assertEqual(response.status_code, 200)

        # Now we can assume that data should be a dictionary
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data['name'], 'Test Product')

    def test_update_product(self):
        """
        Test the updating of a product via the API.
        """
        # Create a product, then update it
        self.test_product_creation()
        response = self.client.put('/api/product/1', json={
            'name': 'Updated Name',
            'description': 'Updated description',
            'price': 15.99,
            'inventory': 150
        })
        self.assertEqual(response.status_code, 200)
        updated_product = db.session.get(Product, 1)
        self.assertEqual(updated_product.name, 'Updated Name')

    def test_delete_product(self):
        """
        Test the deletion of a product via the API.
        """
        # Create a product, then delete it
        self.test_product_creation()
        response = self.client.delete('/api/product/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Product, 1))

class ProductServiceLayerTestCase(unittest.TestCase):
    """
    Test cases for the ProductService class methods.

    Service Layer Logic Tests:
        ProductService class methods should be tested to ensure they
        handle logic correctly.
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_product_service(self):
        """
        Test the 'add_product' method of the ProductService class.
        """
        product_data = {
            'name': 'Service Test Product',
            'description': 'This is a test product added by the service',
            'price': 10.99,
            'inventory': 100
        }
        new_product = ProductService.add_product(product_data)
        # Since the add_product method returns a dictionary, we should assert like this:
        self.assertEqual(new_product['name'], 'Service Test Product')
        self.assertEqual(new_product['description'], 'This is a test product added by the service')
        self.assertEqual(new_product['price'], 10.99)
        self.assertEqual(new_product['inventory'], 100)

        # Further, we can check if the product was indeed added to the database.
        added_product = Product.query.filter_by(name='Service Test Product').first()
        self.assertIsNotNone(added_product)


if __name__ == '__main__':
    unittest.main()
