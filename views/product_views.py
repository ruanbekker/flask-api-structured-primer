from flask import Blueprint, jsonify, request
from services.product_service import ProductService

product_blueprint = Blueprint('product_blueprint', __name__)
"""
Blueprint for managing product-related routes.
"""

@product_blueprint.route('/products', methods=['GET'])
def get_products():
    """
    Retrieve all products.

    Returns:
    list: A list of all products.
    """
    return ProductService.get_all_products()

@product_blueprint.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Retrieve a specific product.

    Parameters:
    product_id (int): The ID of the product to retrieve.

    Returns:
    dict: A dictionary representing the retrieved product.
    """
    response = ProductService.get_product(product_id)
    return jsonify(response), 200

@product_blueprint.route('/product', methods=['POST'])
def create_product():
    """
    Create a new product.

    Returns:
    dict: A dictionary representing the created product.
    """
    data = request.get_json()
    product = ProductService.add_product(data)
    return jsonify(product), 201

@product_blueprint.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update a product.

    Parameters:
    product_id (int): The ID of the product to update.

    Returns:
    dict: A dictionary representing the updated product.
    """
    data = request.get_json()
    try:
        product = ProductService.update_product(product_id, data)
        return jsonify(product), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@product_blueprint.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Delete a product.

    Parameters:
    product_id (int): The ID of the product to delete.

    Returns:
    dict: A message confirming the deletion of the product.
    """
    try:
        success = ProductService.delete_product(product_id)
        if success:
            return jsonify({'message': 'Product deleted'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
