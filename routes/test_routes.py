from flask import Blueprint, request, jsonify
from models.schemas import TestGenerationRequest, TestResponse, HealthCheckResponse
from services.test_service import test_service
import logging

logger = logging.getLogger(__name__)

test_bp = Blueprint('tests', __name__, url_prefix='/api/tests')

@test_bp.route('/generate', methods=['POST'])
def generate_test():
    """
    Generate a new practice test
    
    Request body:
    {
        "subject": "Python Programming",
        "num_questions": 10,
        "difficulty": "medium"
    }
    """
    try:
        # Parse and validate request
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is required",
                "error": "Empty request body"
            }), 400
        
        request_obj = TestGenerationRequest(**data)
        
        # Generate test using service
        practice_test = test_service.generate_practice_test(request_obj)
        
        response = TestResponse(
            success=True,
            message=f"Successfully generated {request_obj.num_questions} questions for {request_obj.subject}",
            data=practice_test
        )
        
        return jsonify(response.dict()), 201
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Invalid request parameters",
            "error": str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error generating test: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to generate test",
            "error": str(e)
        }), 500

@test_bp.route('/<test_id>', methods=['GET'])
def get_test(test_id):
    """Retrieve a specific practice test by ID"""
    try:
        practice_test = test_service.get_test(test_id)
        response = TestResponse(
            success=True,
            message="Test retrieved successfully",
            data=practice_test
        )
        return jsonify(response.dict()), 200
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "error": "Test not found"
        }), 404
    except Exception as e:
        logger.error(f"Error retrieving test: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve test",
            "error": str(e)
        }), 500

@test_bp.route('/', methods=['GET'])
def list_tests():
    """List all generated tests"""
    try:
        tests = test_service.list_tests()
        return jsonify({
            "success": True,
            "message": f"Retrieved {len(tests)} tests",
            "data": [t.dict() for t in tests]
        }), 200
    except Exception as e:
        logger.error(f"Error listing tests: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve tests",
            "error": str(e)
        }), 500

@test_bp.route('/<test_id>', methods=['DELETE'])
def delete_test(test_id):
    """Delete a practice test by ID"""
    try:
        test_service.delete_test(test_id)
        return jsonify({
            "success": True,
            "message": f"Test {test_id} deleted successfully"
        }), 200
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "error": "Test not found"
        }), 404
    except Exception as e:
        logger.error(f"Error deleting test: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to delete test",
            "error": str(e)
        }), 500

@test_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    response = HealthCheckResponse(
        status="healthy",
        environment="development"
    )
    return jsonify(response.dict()), 200