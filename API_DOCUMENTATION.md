# Testify API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Currently, the API does not require authentication.

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "environment": "development"
}
```

---

### 2. Generate Practice Test

**Endpoint:** `POST /api/tests/generate`

**Request Body:**
```json
{
  "subject": "Python Programming",
  "num_questions": 10,
  "difficulty": "medium"
}
```

**Success Response (201 Created):**
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
        "question": "What is the output of print(len('Python'))?",
        "type": "multiple_choice",
        "options": ["5", "6", "7", "8"],
        "correct_answer": "6",
        "explanation": "The string 'Python' has 6 characters."
      }
    ]
  }
}
```

---

### 3. Get Specific Test

**Endpoint:** `GET /api/tests/<test_id>`

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Test retrieved successfully",
  "data": { /* PracticeTest object */ }
}
```

---

### 4. List All Tests

**Endpoint:** `GET /api/tests`

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Retrieved 2 tests",
  "data": [ /* Array of PracticeTest objects */ ]
}
```

---

### 5. Delete Test

**Endpoint:** `DELETE /api/tests/<test_id>`

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Test 550e8400-e29b-41d4-a716-446655440000 deleted successfully"
}
```

---

## Example Usage

### cURL
```bash
# Generate a test
curl -X POST http://localhost:5000/api/tests/generate \
  -H "Content-Type: application/json" \
  -d '{"subject":"Biology","num_questions":5,"difficulty":"easy"}'

# List all tests
curl http://localhost:5000/api/tests

# Get a specific test
curl http://localhost:5000/api/tests/550e8400-e29b-41d4-a716-446655440000

# Delete a test
curl -X DELETE http://localhost:5000/api/tests/550e8400-e29b-41d4-a716-446655440000
```

### Python
```python
import requests

BASE_URL = "http://localhost:5000"

# Generate a test
response = requests.post(
    f"{BASE_URL}/api/tests/generate",
    json={
        "subject": "Chemistry",
        "num_questions": 8,
        "difficulty": "medium"
    }
)

test_data = response.json()
print(test_data)
```

### JavaScript
```javascript
const BASE_URL = "http://localhost:5000";

async function generateTest() {
  const response = await fetch(`${BASE_URL}/api/tests/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      subject: "History",
      num_questions: 10,
      difficulty: "hard"
    })
  });
  
  return await response.json();
}
```
