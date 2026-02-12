# Task Management API - FastAPI

A simple, fully-functional task management system built with FastAPI, featuring in-memory storage, comprehensive validation, and interactive Swagger UI documentation.

## Features

- **Create Tasks** - Auto-generated task IDs with timestamps
- **Read Tasks** - Fetch by ID or list all with optional status filtering
- **Update Tasks** - Partial or full updates with automatic timestamp tracking
- **Delete Tasks** - Remove tasks from the system
- **Task Status Management** - Four status types: pending, in_progress, completed, failed
- **Statistics** - Get task summary by status
- **Comprehensive Validation** - Pydantic models with field constraints
- **Error Handling** - Proper HTTP status codes and meaningful error messages
- **Interactive API Docs** - Swagger UI at `/docs` and ReDoc at `/redoc`
- **In-Memory Storage** - Fast and simple data persistence (resets on restart)

## Project Structure

```
Task2/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation & Setup

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Install Dependencies

```bash
cd Task2
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python app.py
```

The API will start running at: **http://localhost:8000**

## API Endpoints

### Health Check

**GET** `/`
- Status: 200 OK
- Response: `{"message": "Task Management API is running"}`

---

### Task Operations

#### 1. Create a New Task

**POST** `/tasks`

**Request Body:**
```json
{
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API"
}
```

**Response (201 Created):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API",
  "status": "pending",
  "created_at": "2025-02-09T10:30:45.123456",
  "updated_at": "2025-02-09T10:30:45.123456"
}
```

**Status Code:** 201 Created

---

#### 2. Get Task by ID

**GET** `/tasks/{task_id}`

**Example Request:**
```
GET /tasks/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response (200 OK):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API",
  "status": "pending",
  "created_at": "2025-02-09T10:30:45.123456",
  "updated_at": "2025-02-09T10:30:45.123456"
}
```

**Status Code:** 200 OK (or 404 Not Found if task doesn't exist)

---

#### 3. List All Tasks (with Optional Filter)

**GET** `/tasks`

**Query Parameters:**
- `status` (optional): Filter by status - `pending`, `in_progress`, `completed`, or `failed`

**Examples:**
```
GET /tasks                           # Get all tasks
GET /tasks?status=pending           # Get only pending tasks
GET /tasks?status=completed         # Get only completed tasks
```

**Response (200 OK):**
```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Implement user authentication",
    "description": "Add JWT-based authentication to the API",
    "status": "pending",
    "created_at": "2025-02-09T10:30:45.123456",
    "updated_at": "2025-02-09T10:30:45.123456"
  },
  {
    "id": "b2c3d4e5-f6f7-8901-bcde-f12345678901",
    "title": "Fix database connection",
    "description": "Resolve timeout issues with database",
    "status": "in_progress",
    "created_at": "2025-02-09T10:25:30.654321",
    "updated_at": "2025-02-09T10:28:15.654321"
  }
]
```

**Status Code:** 200 OK

---

#### 4. Update a Task

**PATCH** `/tasks/{task_id}`

**Request Body (all fields optional):**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "status": "in_progress"
}
```

**Response (200 OK):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Updated task title",
  "description": "Updated description",
  "status": "in_progress",
  "created_at": "2025-02-09T10:30:45.123456",
  "updated_at": "2025-02-09T10:35:20.123456"
}
```

**Status Code:** 200 OK (or 404 Not Found if task doesn't exist)

---

#### 5. Delete a Task

**DELETE** `/tasks/{task_id}`

**Example Request:**
```
DELETE /tasks/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response:** No Content

**Status Code:** 204 No Content (or 404 Not Found if task doesn't exist)

---

#### 6. Get Task Statistics

**GET** `/tasks/stats/summary`

**Response (200 OK):**
```json
{
  "total_tasks": 5,
  "by_status": {
    "pending": 2,
    "in_progress": 1,
    "completed": 2,
    "failed": 0
  }
}
```

**Status Code:** 200 OK

---

## Task Status Types

| Status | Description |
|--------|-------------|
| `pending` | Task is created but not yet started (default) |
| `in_progress` | Task is currently being worked on |
| `completed` | Task has been successfully completed |
| `failed` | Task failed to complete |

---

## Validation Rules

- **Task Title:**
  - Required field
  - Length: 1-255 characters
  
- **Task Description:**
  - Required field (can be empty string)
  - Length: 0-1000 characters

- **Task Status:**
  - Must be one of: `pending`, `in_progress`, `completed`, `failed`
  - Default: `pending`

- **Task ID:**
  - Auto-generated UUID
  - Read-only (cannot be modified)

---

## Error Handling

The API returns appropriate HTTP status codes and error messages:

### 404 Not Found
```json
{
  "detail": "Task with ID 'invalid-id' not found"
}
```

### 422 Unprocessable Entity (Validation Error)
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

## Interactive API Documentation

Once the server is running, access the interactive API documentation at:

- **Swagger UI:** http://localhost:8000/docs
  - Full interactive API testing interface
  - "Try it out" button to test endpoints
  
- **ReDoc:** http://localhost:8000/redoc
  - Alternative documentation view

---

## Example Usage with cURL

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project report",
    "description": "Write comprehensive project documentation"
  }'
```

### List All Tasks
```bash
curl -X GET "http://localhost:8000/tasks"
```

### List Pending Tasks Only
```bash
curl -X GET "http://localhost:8000/tasks?status=pending"
```

### Update a Task (replace with actual task ID)
```bash
curl -X PATCH "http://localhost:8000/tasks/{task_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress"
  }'
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/tasks/{task_id}"
```

---

## Data Persistence

**Important:** This implementation uses **in-memory storage**, which means:

- All data is stored in a Python dictionary during runtime
- Fast and efficient for development and testing
- Data is lost when the server stops
- Not suitable for production without modifications

To persist data, you could integrate:
- SQLite/PostgreSQL with SQLAlchemy
- MongoDB with PyMongo
- Redis for caching

---

## Code Structure

### Enums
- `TaskStatus`: Defines the four valid task statuses

### Pydantic Models
- `TaskBase`: Base model with title and description
- `TaskCreate`: Model for creating new tasks
- `TaskUpdate`: Model for partial updates (all fields optional)
- `Task`: Complete task model with ID, status, and timestamps

### Endpoints
- 1 health check endpoint
- 6 task management endpoints
- 1 statistics endpoint

### Storage
- `tasks_db`: Dictionary-based in-memory database

---

## API Workflow Example

1. **Create a task:**
   - POST `/tasks` with title and description
   - Receive task with auto-generated ID and `pending` status

2. **Update task status to in progress:**
   - PATCH `/tasks/{id}` with `status: "in_progress"`
   - `updated_at` timestamp automatically updates

3. **Mark task as completed:**
   - PATCH `/tasks/{id}` with `status: "completed"`

4. **Filter completed tasks:**
   - GET `/tasks?status=completed`

5. **Check statistics:**
   - GET `/tasks/stats/summary`

6. **Clean up:**
   - DELETE `/tasks/{id}` when done

---

## Testing the API

### Via Swagger UI (Recommended)

1. Start the server: `python app.py`
2. Open: http://localhost:8000/docs
3. Click on any endpoint
4. Click "Try it out"
5. Fill in parameters/body
6. Click "Execute"
7. View the response

### Via Command Line (cURL)

See the "Example Usage with cURL" section above.

### Python Requests Library

```python
import requests

# Create task
response = requests.post(
    "http://localhost:8000/tasks",
    json={"title": "Test Task", "description": "A test task"}
)
task = response.json()
print(f"Created task: {task['id']}")

# Get task
response = requests.get(f"http://localhost:8000/tasks/{task['id']}")
print(response.json())

# Update task
response = requests.patch(
    f"http://localhost:8000/tasks/{task['id']}",
    json={"status": "in_progress"}
)
print(response.json())

# List all tasks
response = requests.get("http://localhost:8000/tasks")
print(response.json())

# Delete task
requests.delete(f"http://localhost:8000/tasks/{task['id']}")
```

---

## Troubleshooting

### Port 8000 Already in Use

If port 8000 is already in use, modify `app.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to different port
```

### Module Not Found Error

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Invalid Task ID

- Task IDs are UUIDs generated automatically
- Copy the exact ID from the task creation response
- If the ID is incorrect, you'll receive a 404 error

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI 0.104.1 |
| Server | Uvicorn 0.24.0 |
| Validation | Pydantic 2.5.0 |
| Language | Python 3.8+ |

---

## Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- User authentication and authorization
- Task categories and tags
- Due dates and reminders
- Task dependencies
- Bulk operations
- Export/import functionality
- Task history and audit logs

---

## License

This project is provided as-is for educational and demonstration purposes.

---

## Support

For issues or questions, refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

Enjoy your Task Management API! 
