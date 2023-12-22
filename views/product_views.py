from flask import Blueprint, jsonify, request
from flasgger import Swagger, swag_from
from services.product_service import ProductService
from shared.logging_utils import get_logger

# Get an instance of a logger
logger = get_logger(__name__)

# Initialize Blueprint
product_blueprint = Blueprint('product_blueprint', __name__)

# Initialize Swagger
swagger = Swagger()

"""
Blueprint for managing product-related routes.
"""

@product_blueprint.route('/products', methods=['GET'])
@swag_from({
    'tags': ['Products'],
    'description': 'Retrieve all products.',
    'responses': {
        '200': {
            'description': 'List of products',
            'schema': {
                'type': 'array',
                'items': {'$ref': '#/definitions/Product'}
            }
        }
    }
})
def get_products():
    """
    Retrieve all products.

    Returns
    -------
    list: A list of all products.
    """
    logger.info('retrieving all products')
    return ProductService.get_all_products()

@product_blueprint.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Retrieve a specific product.

    Parameters:
    product_id (int): The ID of the product to retrieve.

    :return: A dictionary representing the retrieved product.
    :rtype: dict
    """
    logger.info('retrieving details for product id=%s', product_id)
    response = ProductService.get_product(product_id)
    return jsonify(response), 200

@product_blueprint.route('/product', methods=['POST'])
def create_product():
    """
    Create a new product.

    :return: A dictionary representing the created product.
    :rtype: dict
    """
    logger.info('creating a new product')
    data = request.get_json()
    product = ProductService.add_product(data)
    return jsonify(product), 201

@product_blueprint.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update a product.

    :param product_id: The ID of the product to update.

    :return: A dictionary representing the updated product.
    :rtype: dict
    """
    data = request.get_json()
    try:
        product = ProductService.update_product(product_id, data)
        logger.info('updating product details for product id=%s', product_id)
        return jsonify(product), 200
    except ValueError as err:
        logger.error('could not update the product with product id %s: %s', product_id, err)
        return jsonify({'error': str(err)}), 404

@product_blueprint.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Delete a product.

    :param product_id: The ID of the product to delete.

    :return: A message confirming the deletion of the product.
    :rtype: dict
    """
    try:
        success = ProductService.delete_product(product_id)
        if success:
            logger.info('product was deleted: product_id=%s', product_id)
            return jsonify({'message': 'Product deleted'}), 200
    except ValueError as err:
        logger.error('product could not be deleted deleted: product_id=%s, error=', err)
        return jsonify({'error': str(err)}), 404
