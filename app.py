from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from routes.test_routes import test_bp
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(test_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Endpoint not found",
            "error": "404 Not Found"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            "success": False,
            "message": "Internal server error",
            "error": "500 Internal Server Error"
        }), 500
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            "status": "healthy",
            "environment": app.config['FLASK_ENV']
        }), 200
    
    # API info
    @app.route('/api', methods=['GET'])
    def api_info():
        return jsonify({
            "name": "Testify API",
            "version": "1.0.0",
            "description": "Generate AI-powered practice tests",
            "endpoints": {
                "generate_test": "POST /api/tests/generate",
                "get_test": "GET /api/tests/<test_id>",
                "list_tests": "GET /api/tests",
                "delete_test": "DELETE /api/tests/<test_id>"
            }
        }), 200
    
    logger.info(f"Flask app created with config: {config_name}")
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )