import pytest
from models.schemas import TestGenerationRequest, DifficultyLevel, Question, QuestionType

def test_valid_test_generation_request():
    """Test valid test generation request"""
    request = TestGenerationRequest(
        subject="Python Programming",
        num_questions=10,
        difficulty=DifficultyLevel.MEDIUM
    )
    assert request.subject == "Python Programming"
    assert request.num_questions == 10
    assert request.difficulty == DifficultyLevel.MEDIUM

def test_invalid_num_questions_zero():
    """Test that zero questions are invalid"""
    with pytest.raises(ValueError):
        TestGenerationRequest(
            subject="Python",
            num_questions=0,
            difficulty=DifficultyLevel.EASY
        )

def test_invalid_num_questions_exceeds_max():
    """Test that more than 50 questions are invalid"""
    with pytest.raises(ValueError):
        TestGenerationRequest(
            subject="Python",
            num_questions=51,
            difficulty=DifficultyLevel.EASY
        )

def test_valid_question():
    """Test valid question creation"""
    question = Question(
        id=1,
        question="What is 2+2?",
        type=QuestionType.MULTIPLE_CHOICE,
        options=["3", "4", "5", "6"],
        correct_answer="4",
        explanation="2+2=4"
    )
    assert question.id == 1
    assert question.correct_answer == "4"

def test_difficulty_levels():
    """Test all difficulty levels"""
    assert DifficultyLevel.EASY == "easy"
    assert DifficultyLevel.MEDIUM == "medium"
    assert DifficultyLevel.HARD == "hard"