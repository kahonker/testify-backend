import openai
import json
import logging
from config import Config
from models.schemas import Question, QuestionType, DifficultyLevel
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.AI_MODEL
        self.temperature = Config.AI_TEMPERATURE
        self.max_tokens = Config.AI_MAX_TOKENS
    
    def generate_test(self, subject: str, num_questions: int, difficulty: DifficultyLevel) -> List[Question]:
        """
        Generate practice test questions using OpenAI API
        
        Args:
            subject: The subject of the test
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
        
        Returns:
            List of Question objects
        """
        try:
            prompt = self._build_prompt(subject, num_questions, difficulty)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational content creator specializing in generating comprehensive practice tests. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract and parse the response
            content = response['choices'][0]['message']['content']
            logger.info(f"AI Response received for subject: {subject}")
            
            questions = self._parse_ai_response(content)
            return questions
            
        except openai.error.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate test: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {str(e)}")
            raise Exception("Failed to parse AI response as valid JSON")
        except Exception as e:
            logger.error(f"Unexpected error in generate_test: {str(e)}")
            raise
    
    def _build_prompt(self, subject: str, num_questions: int, difficulty: DifficultyLevel) -> str:
        """Build the prompt for the AI to generate questions"""
        
        difficulty_descriptions = {
            DifficultyLevel.EASY: "beginner-friendly with straightforward answers",
            DifficultyLevel.MEDIUM: "intermediate level requiring some critical thinking",
            DifficultyLevel.HARD: "advanced level requiring deep understanding and analysis"
        }
        
        prompt = f"""Generate exactly {num_questions} practice test questions about \"{subject}\".

Difficulty level: {difficulty_descriptions[difficulty]}

Return the response as a valid JSON array with the following structure:
{{
  \"questions\": [
    {{
      \"id\": 1,
      \"question\": \"Question text here?\",
      \"type\": \"multiple_choice|short_answer|true_false\",
      \"options\": [\"option1\", \"option2\", \"option3\", \"option4\"],
      \"correct_answer\": \"The correct answer\",
      \"explanation\": \"Explanation of why this is correct\"
    }}
  ]
}}

Requirements:
- Generate exactly {num_questions} questions
- Mix question types: primarily multiple choice, some short answer or true/false
- Ensure questions are {difficulty.value} difficulty
- Make explanations clear and educational
- For multiple choice, provide 4 options
- Ensure the JSON is valid and parseable
- Do NOT include any text outside the JSON object"""

        return prompt
    
    def _parse_ai_response(self, content: str) -> List[Question]:
        """Parse the AI response and create Question objects"""
        try:
            # Try to extract JSON from the response
            data = json.loads(content)
            
            if 'questions' not in data:
                raise ValueError("Response missing 'questions' field")
            
            questions = []
            for idx, q_data in enumerate(data['questions'], 1):
                try:
                    # Validate question type
                    q_type = QuestionType(q_data.get('type', 'multiple_choice'))
                    
                    question = Question(
                        id=q_data.get('id', idx),
                        question=q_data.get('question', ''),
                        type=q_type,
                        options=q_data.get('options'),
                        correct_answer=q_data.get('correct_answer', ''),
                        explanation=q_data.get('explanation', '')
                    )
                    questions.append(question)
                except Exception as e:
                    logger.warning(f"Failed to parse question {idx}: {str(e)}")
                    continue
            
            if not questions:
                raise ValueError("No valid questions were parsed from the response")
            
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise ValueError(f"Invalid JSON in AI response: {str(e)}")

# Singleton instance
ai_service = AIService()