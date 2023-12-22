from database.db import db

class Product(db.Model):
    """
    Class representing a product.

    Attributes:
        id (int): The ID of the product.
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
        inventory (int): The inventory of the product.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(1024))
    price = db.Column(db.Float)
    inventory = db.Column(db.Integer)

    def to_dict(self):
        """
        Convert the product object to a dictionary.

        Returns:
            dict: A dictionary representing the product.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'inventory': self.inventory
        }

    def __repr__(self):
        """
        Return a string representation of the product.

        Returns:
            str: A string representation of the product.
        """
        return f'<Product {self.name}>'

