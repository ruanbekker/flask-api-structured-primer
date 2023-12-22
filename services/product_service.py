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

        Parameters:
        data (dict): A dictionary containing product data.

        Returns:
        dict: A dictionary representing the added product.
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

        Returns:
        list: A list of dictionaries, each representing a product.
        """
        return [product.to_dict() for product in Product.query.all()]

    @staticmethod
    def get_product(product_id):
        """
        Retrieve a specific product from the database.

        Parameters:
        product_id (int): The ID of the product to retrieve.

        Returns:
        dict or None: A dictionary representing the product if found, else None.
        """
        # product = Product.query.get(product_id) # v1
        # product = db.session.get(Product, product_id) # v2
        product = db.session.get(Product, product_id)
        return product.to_dict() if product else None

    @staticmethod
    def update_product(product_id, data):
        """
        Update a product in the database.

        Parameters:
        product_id (int): The ID of the product to update.
        data (dict): A dictionary containing the updated product data.

        Returns:
        dict: A dictionary representing the updated product.
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

        Parameters:
        product_id (int): The ID of the product to delete.

        Returns:
        bool: True if the product is successfully deleted.
        """
        product = db.session.get(Product, product_id)
        if not product:
            raise ValueError("Product not found")

        db.session.delete(product)
        db.session.commit()
        return True
