# Testify Backend

A Python Flask-based backend API for generating AI-powered practice tests. Users can input a subject, specify the number of questions, and choose a difficulty level to generate custom practice tests using OpenAI's GPT models.

## Features

- ✨ AI-powered test generation using OpenAI API
- 📝 Customizable question count (1-50)
- 🎯 Three difficulty levels (easy, medium, hard)
- 🔄 Multiple question types (multiple choice, short answer, true/false)
- 💾 In-memory test storage (easily swappable with a database)
- 🔒 Input validation with Pydantic
- 📊 JSON API responses
- 🐛 Comprehensive logging
- 🚀 Production-ready with error handling

## Project Structure

```
testify-backend/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── models/
│   └── schemas.py           # Pydantic models for validation
├── services/
│   ├── ai_service.py        # OpenAI integration
│   └── test_service.py      # Test management logic
├── routes/
│   └── test_routes.py       # API endpoints
├── tests/
│   └── test_schemas.py      # Unit tests
├── Dockerfile               # Docker configuration
└── docker-compose.yml       # Docker Compose setup
```

## Setup Instructions

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/kahonker/testify-backend.git
cd testify-backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
FLASK_ENV=development
DEBUG=True
PORT=5000
```

### 3. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

### API Info
```
GET /api
```

### Generate Practice Test
```
POST /api/tests/generate
Content-Type: application/json

{
  "subject": "Python Programming",
  "num_questions": 10,
  "difficulty": "medium"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Successfully generated 10 questions for Python Programming",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "subject": "Python Programming",
    "difficulty": "medium",
    "num_questions": 10,
    "total_questions": 10,
    "created_at": "2026-05-28T10:30:00Z",
    "questions": [
      {
        "id": 1,
        "question": "What is the output of print(2 ** 3)?",
        "type": "multiple_choice",
        "options": ["6", "8", "9", "12"],
        "correct_answer": "8",
        "explanation": "The ** operator performs exponentiation in Python. 2 ** 3 equals 2 * 2 * 2 = 8."
      }
    ]
  }
}
```

### Get Specific Test
```
GET /api/tests/<test_id>
```

### List All Tests
```
GET /api/tests
```

### Delete Test
```
DELETE /api/tests/<test_id>
```

## Request Parameters

### Generate Test Request

| Parameter | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `subject` | string | Yes | 1-100 characters | Subject matter for the test |
| `num_questions` | integer | Yes | 1-50 | Number of questions to generate |
| `difficulty` | string | Yes | "easy", "medium", "hard" | Difficulty level |

### Difficulty Levels

- **Easy**: Beginner-friendly questions with straightforward answers
- **Medium**: Intermediate questions requiring critical thinking
- **Hard**: Advanced questions requiring deep understanding and analysis

### Question Types

- **Multiple Choice**: Four options with one correct answer
- **Short Answer**: Free-form text response
- **True/False**: Boolean answer

## Response Format

All responses follow a standard format:

```json
{
  "success": boolean,
  "message": string,
  "data": object | null,
  "error": string | null
}
```

## Error Handling

### 400 Bad Request
```json
{
  "success": false,
  "message": "Invalid request parameters",
  "error": "num_questions must be between 1 and 50"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Test with ID xxx not found",
  "error": "Test not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Failed to generate test",
  "error": "API key is invalid"
}
```

## Docker Deployment

### Build and Run with Docker Compose

```bash
docker-compose up -d
```

The API will be available at `http://localhost:5000`

### Build Docker Image

```bash
docker build -t testify-backend .
```

### Run Docker Container

```bash
docker run -p 5000:5000 -e OPENAI_API_KEY=your-key testify-backend
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
The project follows PEP 8 style guidelines.

## Future Improvements

- [ ] Add database integration (PostgreSQL/MongoDB)
- [ ] Implement user authentication
- [ ] Add test scoring and grading
- [ ] Support for multiple AI providers (Claude, Gemini)
- [ ] Image/diagram support in questions
- [ ] Export tests to PDF/Word
- [ ] Real-time test progress tracking
- [ ] Analytics dashboard

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Enable CORS
- **python-dotenv**: Environment variable management
- **openai**: OpenAI API client
- **pydantic**: Data validation
- **gunicorn**: Production server
- **pytest**: Testing framework

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please create an issue on the GitHub repository.
