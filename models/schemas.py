from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"
    TRUE_FALSE = "true_false"

class Question(BaseModel):
    id: int
    question: str
    type: QuestionType
    options: Optional[List[str]] = None  # For multiple choice
    correct_answer: str
    explanation: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "question": "What is the capital of France?",
                "type": "multiple_choice",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "correct_answer": "Paris",
                "explanation": "Paris is the capital city of France."
            }
        }

class PracticeTest(BaseModel):
    id: str
    subject: str
    difficulty: DifficultyLevel
    num_questions: int
    questions: List[Question]
    created_at: str
    total_questions: int

    class Config:
        schema_extra = {
            "example": {
                "id": "test_123",
                "subject": "Biology",
                "difficulty": "medium",
                "num_questions": 5,
                "questions": [],
                "created_at": "2026-05-28T10:30:00Z",
                "total_questions": 5
            }
        }

class TestGenerationRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100)
    num_questions: int = Field(..., ge=1, le=50)
    difficulty: DifficultyLevel

    @validator('num_questions')
    def validate_num_questions(cls, v):
        if v < 1 or v > 50:
            raise ValueError('Number of questions must be between 1 and 50')
        return v

    class Config:
        schema_extra = {
            "example": {
                "subject": "Python Programming",
                "num_questions": 10,
                "difficulty": "medium"
            }
        }

class TestResponse(BaseModel):
    success: bool
    message: str
    data: Optional[PracticeTest] = None
    error: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str
    environment: str
    version: str = "1.0.0"