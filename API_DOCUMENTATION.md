# Testify API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, the API does not require authentication. Authentication will be added in future versions.

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running

**Response:**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

**Status Code:** 200 OK

---

### 2. API Information

**Endpoint:** `GET /api`

**Description:** Get information about available endpoints

**Response:**
```json
{
  "name": "Testify API",
  "version": "1.0.0",
  "description": "Generate AI-powered practice tests",
  "endpoints": {
    "generate_test": "POST /api/tests/generate",
    "get_test": "GET /api/tests/<test_id>",
    "list_tests": "GET /api/tests",
    "delete_test": "DELETE /api/tests/<test_id>"
  }
}
```

**Status Code:** 200 OK

---

### 3. Generate Practice Test

**Endpoint:** `POST /api/tests/generate`

**Description:** Generate a new practice test based on subject, number of questions, and difficulty

**Request Body:**
```json
{
  "subject": "string (required, 1-100 characters)",
  "num_questions": "integer (required, 1-50)",
  "difficulty": "string (required: 'easy', 'medium', or 'hard')"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:5000/api/tests/generate \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Python Programming",
    "num_questions": 5,
    "difficulty": "medium"
  }'
```

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "Successfully generated 5 questions for Python Programming",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "subject": "Python Programming",
    "difficulty": "medium",
    "num_questions": 5,
    "total_questions": 5,
    "created_at": "2026-05-28T10:30:00Z",
    "questions": [
      {
        "id": 1,
        "question": "What is the output of print(len('Python'))?",
        "type": "multiple_choice",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "6",
        "explanation": "The string 'Python' has 6 characters: P, y, t, h, o, n."
      },
      {
        "id": 2,
        "question": "Which of these is a mutable data type in Python?",
        "type": "multiple_choice",
        "options": ["tuple", "string", "list", "frozenset"],
        "correct_answer": "list",
        "explanation": "Lists are mutable and can be modified after creation. Tuples, strings, and frozensets are immutable."
      }
    ]
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "success": false,
  "message": "Invalid request parameters",
  "error": "num_questions must be between 1 and 50"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "success": false,
  "message": "Failed to generate test",
  "error": "API key is invalid or request failed"
}
```

---

### 4. Get Specific Test

**Endpoint:** `GET /api/tests/<test_id>`

**Description:** Retrieve a previously generated test by its ID

**Path Parameters:**
- `test_id` (string, required): The unique identifier of the test

**Example Request:**
```bash
curl http://localhost:5000/api/tests/550e8400-e29b-41d4-a716-446655440000
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Test retrieved successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "subject": "Python Programming",
    "difficulty": "medium",
    "num_questions": 5,
    "total_questions": 5,
    "created_at": "2026-05-28T10:30:00Z",
    "questions": [...]
  }
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "message": "Test with ID xxx not found",
  "error": "Test not found"
}
```

---

### 5. List All Tests

**Endpoint:** `GET /api/tests`

**Description:** Retrieve all generated tests

**Query Parameters:**
None

**Example Request:**
```bash
curl http://localhost:5000/api/tests
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Retrieved 2 tests",
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "subject": "Python Programming",
      "difficulty": "medium",
      "num_questions": 5,
      "total_questions": 5,
      "created_at": "2026-05-28T10:30:00Z",
      "questions": [...]
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "subject": "Biology",
      "difficulty": "easy",
      "num_questions": 3,
      "total_questions": 3,
      "created_at": "2026-05-28T10:35:00Z",
      "questions": [...]
    }
  ]
}
```

---

### 6. Delete Test

**Endpoint:** `DELETE /api/tests/<test_id>`

**Description:** Delete a previously generated test

**Path Parameters:**
- `test_id` (string, required): The unique identifier of the test to delete

**Example Request:**
```bash
curl -X DELETE http://localhost:5000/api/tests/550e8400-e29b-41d4-a716-446655440000
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Test 550e8400-e29b-41d4-a716-446655440000 deleted successfully"
}
```

**Error Response (404 Not Found):**
```json
{
  "success": false,
  "message": "Test with ID xxx not found",
  "error": "Test not found"
}
```

---

## Data Models

### Question Object
```json
{
  "id": 1,
  "question": "Question text here?",
  "type": "multiple_choice|short_answer|true_false",
  "options": ["option1", "option2", "option3", "option4"],
  "correct_answer": "The correct answer",
  "explanation": "Explanation of why this is correct"
}
```

### Practice Test Object
```json
{
  "id": "UUID",
  "subject": "Subject name",
  "difficulty": "easy|medium|hard",
  "num_questions": 10,
  "total_questions": 10,
  "created_at": "ISO 8601 timestamp",
  "questions": [/* array of Question objects */]
}
```

---

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## Rate Limiting

Currently, there is no rate limiting. Rate limiting will be implemented in future versions.

---

## CORS

The API supports Cross-Origin Resource Sharing (CORS). You can make requests from any origin.

---

## Examples

### Python Example
```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Generate a new test
response = requests.post(
    f"{BASE_URL}/api/tests/generate",
    json={
        "subject": "World History",
        "num_questions": 10,
        "difficulty": "hard"
    }
)

test_data = response.json()
print(json.dumps(test_data, indent=2))

# Get the test ID
test_id = test_data['data']['id']

# Retrieve the test
response = requests.get(f"{BASE_URL}/api/tests/{test_id}")
print(json.dumps(response.json(), indent=2))

# List all tests
response = requests.get(f"{BASE_URL}/api/tests")
print(json.dumps(response.json(), indent=2))

# Delete the test
response = requests.delete(f"{BASE_URL}/api/tests/{test_id}")
print(json.dumps(response.json(), indent=2))
```

### JavaScript Example
```javascript
const BASE_URL = "http://localhost:5000";

async function generateTest() {
  const response = await fetch(`${BASE_URL}/api/tests/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      subject: "Chemistry",
      num_questions: 8,
      difficulty: "medium"
    })
  });

  const data = await response.json();
  console.log(data);
  return data;
}

async function getTest(testId) {
  const response = await fetch(`${BASE_URL}/api/tests/${testId}`);
  const data = await response.json();
  console.log(data);
  return data;
}

async function listTests() {
  const response = await fetch(`${BASE_URL}/api/tests`);
  const data = await response.json();
  console.log(data);
  return data;
}

async function deleteTest(testId) {
  const response = await fetch(`${BASE_URL}/api/tests/${testId}`, {
    method: "DELETE"
  });
  const data = await response.json();
  console.log(data);
  return data;
}

// Usage
generateTest().then(test => {
  if (test.success) {
    getTest(test.data.id);
  }
});
```

### cURL Examples
```bash
# Generate a test
curl -X POST http://localhost:5000/api/tests/generate \
  -H "Content-Type: application/json" \
  -d '{"subject":"Mathematics","num_questions":10,"difficulty":"medium"}'

# Get all tests
curl http://localhost:5000/api/tests

# Get a specific test
curl http://localhost:5000/api/tests/550e8400-e29b-41d4-a716-446655440000

# Delete a test
curl -X DELETE http://localhost:5000/api/tests/550e8400-e29b-41d4-a716-446655440000
```

---

## Versioning

The API uses semantic versioning. The current version is 1.0.0. Breaking changes will be indicated by a new major version number.

---

## Support

For questions or issues, please contact support or create an issue on GitHub.
