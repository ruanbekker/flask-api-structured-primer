"""
Healthprobe views.

These endpoints are typically used by the Kubernetes liveness and readiness
probes to determine the operational state of the application and manage its
lifecycle in a containerized setup.

Routes:
- '/health': Endpoint to check the health of the application.
- '/ready': Endpoint to check if the application is ready to serve traffic.
"""

from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database.db import db

healthprobe_blueprint = Blueprint('healthprobe', __name__)

@healthprobe_blueprint.route('/health')
def health_check():
    """
    Health check endpoint for the application.

    Used by Kubernetes for liveness and startup probes. Returns a simple response
    to indicate the application is operational.
    """
    return jsonify({"status": "healthy"}), 200

@healthprobe_blueprint.route('/ready')
def readiness_check():
    """
    Readiness check endpoint for the application.

    Used by Kubernetes for readiness probes. Checks additional factors like
    database connectivity to determine if the application is ready to serve traffic.
    """
    try:
        # Using the text function to safely execute a raw SQL query
        db.session.execute(text('SELECT 1'))
        return jsonify({"status": "ready"}), 200
    except SQLAlchemyError as error:
        # Log the exception details for debugging purposes
        return jsonify({"status": "not ready", "reason": str(error)}), 500
