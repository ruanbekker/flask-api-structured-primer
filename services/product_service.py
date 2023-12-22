from models.product import Product
from database.db import db

class ProductService:
    """
    A class to handle operations related to products.
    """

    @staticmethod
    def add_product(data):
        """
        Add a new product to the database.

        :param data: A dictionary containing product data.

        :return: A dictionary representing the added product.
        """
        product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            inventory=data['inventory']
        )
        db.session.add(product)
        db.session.commit()
        return product.to_dict()

    @staticmethod
    def get_all_products():
        """
        Retrieve all products from the database.

        :return: A list of dictionaries, each representing a product.
        :rtype: list
        """
        return [product.to_dict() for product in Product.query.all()]

    @staticmethod
    def get_product(product_id):
        """
        Retrieve a specific product from the database.

        :param product_id: The ID of the product to retrieve.

        :return: A dictionary representing the product if found, else None.
        :rtype: dict or None
        """
        # product = Product.query.get(product_id) # v1
        # product = db.session.get(Product, product_id) # v2
        product = db.session.get(Product, product_id)
        return product.to_dict() if product else None

    @staticmethod
    def update_product(product_id, data):
        """
        Update a product in the database.

        :param product_id: The ID of the product to update.
        :param data: A dictionary containing the updated product data.

        :return: A dictionary representing the updated product.
        :rtype: dict
        """
        product = db.session.get(Product, product_id)
        if not product:
            raise ValueError("Product not found")

        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.inventory = data.get('inventory', product.inventory)

        db.session.commit()
        return product.to_dict()

    @staticmethod
    def delete_product(product_id):
        """
        Delete a product from the database.

        :param product_id: The ID of the product to delete.

        :return: True if the product is successfully deleted.
        :rtype: bool
        """
        product = db.session.get(Product, product_id)
        if not product:
            raise ValueError("Product not found")

        db.session.delete(product)
        db.session.commit()
        return True
