from flask import Blueprint, jsonify, request
from flasgger import Swagger
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
def get_products():
    """
    Retrieve all products.

    ---
    tags:
      - Products
    description: Retrieve all products.
    responses:
      200:
        description: List of products
        schema:
          type: array
          items:
            $ref: '#/definitions/Product'
    """
    logger.info('retrieving all products')
    return ProductService.get_all_products()

@product_blueprint.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Retrieve a specific product by ID.

    ---
    tags:
      - Products
    description: Fetch the details of a specific product from the database using its ID.
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: The ID of the product to retrieve.
    responses:
      200:
        description: Product successfully retrieved.
        schema:
          $ref: '#/definitions/Product'
      404:
        description: Product not found.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Product not found"
    """
    logger.info('retrieving details for product id=%s', product_id)
    response = ProductService.get_product(product_id)
    return jsonify(response), 200

@product_blueprint.route('/product', methods=['POST'])
def create_product():
    """
    Create a new product.

    ---
    tags:
      - Products
    parameters:
      - in: body
        name: product
        description: Product data
        schema:
          type: object
          required:
            - name
            - price
            - description
            - inventory
          properties:
            name:
              type: string
              example: "Sample Product"
            description:
              type: string
              example: "Sample Product Description"
            price:
              type: number
              example: 12.99
            inventory:
              type: integer
              example: 10
    responses:
      201:
        description: Product created
        schema:
          $ref: '#/definitions/Product'
    """
    logger.info('creating a new product')
    data = request.get_json()
    product = ProductService.add_product(data)
    return jsonify(product), 201

@product_blueprint.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update a specific product by ID.

    ---
    tags:
      - Products
    description: Update the details of an existing product in the database.
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: The ID of the product to update.
      - in: body
        name: body
        required: true
        description: Object containing the updated product details.
        schema:
          $ref: '#/definitions/Product'
    responses:
      200:
        description: Product successfully updated.
        schema:
          $ref: '#/definitions/Product'
      404:
        description: Product not found or error in update.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Product not found or update failed"
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
    Delete a product by ID.

    ---
    tags:
      - Products
    description: Delete a specific product from the database.
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
        description: The ID of the product to delete.
    responses:
      200:
        description: Product successfully deleted.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Product deleted"
      404:
        description: Product not found or error in deletion.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Product not found"
    """
    try:
        success = ProductService.delete_product(product_id)
        if success:
            logger.info('product was deleted: product_id=%s', product_id)
            return jsonify({'message': 'Product deleted'}), 200
    except ValueError as err:
        logger.error('product could not be deleted deleted: product_id=%s, error=', err)
        return jsonify({'error': str(err)}), 404
