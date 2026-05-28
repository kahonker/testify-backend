import uuid
from datetime import datetime
from services.ai_service import ai_service
from models.schemas import PracticeTest, TestGenerationRequest, DifficultyLevel
import logging

logger = logging.getLogger(__name__)

class TestService:
    """Service for managing practice tests"""
    
    def __init__(self):
        # In-memory storage (replace with database in production)
        self.tests_db = {}
    
    def generate_practice_test(self, request: TestGenerationRequest) -> PracticeTest:
        """
        Generate a new practice test based on user input
        
        Args:
            request: TestGenerationRequest with subject, num_questions, and difficulty
        
        Returns:
            PracticeTest object
        """
        try:
            logger.info(f"Generating test for subject: {request.subject}, "
                       f"questions: {request.num_questions}, "
                       f"difficulty: {request.difficulty}")
            
            # Call AI service to generate questions
            questions = ai_service.generate_test(
                subject=request.subject,
                num_questions=request.num_questions,
                difficulty=request.difficulty
            )
            
            # Create practice test object
            test_id = str(uuid.uuid4())
            practice_test = PracticeTest(
                id=test_id,
                subject=request.subject,
                difficulty=request.difficulty,
                num_questions=request.num_questions,
                questions=questions,
                created_at=datetime.utcnow().isoformat() + "Z",
                total_questions=len(questions)
            )
            
            # Store in database
            self.tests_db[test_id] = practice_test
            
            logger.info(f"Successfully generated test {test_id}")
            return practice_test
            
        except Exception as e:
            logger.error(f"Error generating practice test: {str(e)}")
            raise
    
    def get_test(self, test_id: str) -> PracticeTest:
        """Retrieve a practice test by ID"""
        if test_id not in self.tests_db:
            raise ValueError(f"Test with ID {test_id} not found")
        return self.tests_db[test_id]
    
    def list_tests(self) -> list:
        """List all generated tests"""
        return list(self.tests_db.values())
    
    def delete_test(self, test_id: str) -> bool:
        """Delete a practice test by ID"""
        if test_id in self.tests_db:
            del self.tests_db[test_id]
            logger.info(f"Test {test_id} deleted")
            return True
        raise ValueError(f"Test with ID {test_id} not found")

# Singleton instance
test_service = TestService()