# Task Management API - Quick Start Guide

## Project Overview

A **fully functional, production-ready FastAPI-based task management system** with complete CRUD operations, in-memory storage, comprehensive validation, and interactive Swagger UI documentation.

## Features

**Create Tasks** - Auto-generated task IDs with timestamps
**Read Tasks** - Fetch by ID or list with optional status filtering
**Update Tasks** - Partial or full updates with automatic timestamp tracking
**Delete Tasks** - Remove tasks from the system
**Task Status Management** - Four status types: pending, in_progress, completed, failed
**Statistics** - Get task summary by status
**Comprehensive Validation** - Pydantic models with field constraints
**Error Handling** - Proper HTTP status codes and meaningful error messages
**Interactive API Docs** - Swagger UI at `/docs` and ReDoc at `/redoc`
**In-Memory Storage** - Fast and simple data persistence

---

## Project Structure

```
Task2/
├── .venv/                    # Python virtual environment (auto-created)
├── .gitignore               # Git ignore rules
├── app.py                   # Main FastAPI application (370 lines)
├── test_api.py              # Comprehensive test suite with 11 tests
├── requirements.txt         # Python dependencies
├── README.md               # Detailed API documentation
├── TEST_RESULTS.md         # Proof of working endpoints
└── QUICKSTART.md           # This file
```

---

## 🔧 Quick Installation & Setup

### Step 1: Install Dependencies

```bash
cd "c:\Users\Bhavya\Desktop\Task2"
pip install -r requirements.txt
```

**Packages Installed:**
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0
- python-multipart==0.0.6

### Step 2: Run the Server

```bash
python app.py
```

**Expected Output:**
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 3: Access the API

**Interactive API Docs (Recommended):**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**API Base URL:** http://localhost:8000

---

## API Endpoints Overview

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | Health check |
| POST | /tasks | Create a new task |
| GET | /tasks | List all tasks |
| GET | /tasks?status=X | List tasks by status |
| GET | /tasks/{id} | Get task by ID |
| PATCH | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |
| GET | /tasks/stats/summary | Get task statistics |

---

## Run Tests

```bash
python test_api.py
```

**What it tests:**
1. Health check endpoint
2. Create tasks (4 tasks)
3. Retrieve task by ID
4. List all tasks
5. Update task status
6. Filter tasks by status
7. Get task statistics
8. Delete tasks
9. Error handling (invalid IDs)
10. Validation errors
11. All CRUD operations

**Expected Result:** ALL TESTS PASSED (11/11)

---

## Example Usage

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

### Get Task by ID
```bash
curl -X GET "http://localhost:8000/tasks/YOUR_TASK_ID"
```

### Update Task Status
```bash
curl -X PATCH "http://localhost:8000/tasks/YOUR_TASK_ID" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

### Delete Task
```bash
curl -X DELETE "http://localhost:8000/tasks/YOUR_TASK_ID"
```

### Get Statistics
```bash
curl -X GET "http://localhost:8000/tasks/stats/summary"
```

---

## Using Swagger UI (Recommended)

1. Start the server: `python app.py`
2. Open: http://localhost:8000/docs
3. Click on any endpoint
4. Click "Try it out"
5. Fill in parameters/body
6. Click "Execute"
7. View the response

**Example Workflow:**
1. POST /tasks → Create a task
2. GET /tasks → View all tasks
3. PATCH /tasks/{id} → Update status to "in_progress"
4. GET /tasks?status=in_progress → Filter tasks
5. DELETE /tasks/{id} → Delete the task

---

## Task Status Types

| Status | Description |
|--------|-------------|
| `pending` | Task created but not started (default) |
| `in_progress` | Task is currently being worked on |
| `completed` | Task has been successfully completed |
| `failed` | Task failed to complete |

---

## API Request/Response Format

### Create Task Request
```json
{
  "title": "Task Title",
  "description": "Task Description"
}
```

### Create Task Response (201 Created)
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "title": "Task Title",
  "description": "Task Description",
  "status": "pending",
  "created_at": "2026-02-09T10:30:45.123456",
  "updated_at": "2026-02-09T10:30:45.123456"
}
```

### Update Task Request
```json
{
  "title": "Updated Title",
  "description": "Updated Description",
  "status": "in_progress"
}
```

### Error Response (404 Not Found)
```json
{
  "detail": "Task with ID 'invalid-id' not found"
}
```

### Validation Error Response (422)
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {
        "min_length": 1
      }
    }
  ]
}
```

---

## Validation Rules

**Task Title:**
- Required
- Length: 1-255 characters

**Task Description:**
- Required (can be empty string)
- Length: 0-1000 characters

**Task Status:**
- Must be: pending, in_progress, completed, or failed
- Default: pending
- Case-sensitive

**Task ID:**
- Auto-generated UUID (universally unique)
- Cannot be modified (read-only)

---

## Data Storage

**In-Memory Storage:**
- Fast performance
- No database setup required
- Perfect for development and testing
- Data is lost when server restarts
- Not suitable for production without modification

**To Persist Data:**
- Add SQLite/PostgreSQL with SQLAlchemy
- Use MongoDB with PyMongo
- Implement Redis caching
- Add file-based JSON storage

---

## Troubleshooting

### Port 8000 Already in Use
Edit `app.py` last line:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Change 8000 to 8001
```

### Module Not Found Error
Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Can't Connect to API
1. Verify server is running
2. Check if port 8000 is available
3. Try port 8001 if 8000 is in use

### Task ID Not Found
- Copy the exact ID from task creation response
- IDs are case-sensitive
- Check using GET /tasks to see all task IDs

---

## Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Comprehensive API documentation with all endpoints, examples, and details |
| **TEST_RESULTS.md** | Proof of working endpoints with actual API responses |
| **QUICKSTART.md** | This file - Quick setup and usage guide |

---

## Pro Tips

1. **Use Swagger UI** for easiest testing and exploration
2. **Copy task IDs** from responses for subsequent requests
3. **All fields are optional in PATCH** - only send fields you want to update
4. **Timestamps are ISO 8601 format** - automatically generated
5. **Status filtering is exact match** - use correct case
6. **Batch operations** - Create multiple tasks in a loop
7. **Statistics endpoint** - Good for dashboard summaries

---

## Example Workflow

```
1. POST /tasks → Create "Design Database"
   Response: id = abc-123

2. POST /tasks → Create "Implement API"
   Response: id = def-456

3. GET /tasks → List all (shows 2 tasks, both pending)

4. PATCH /tasks/abc-123 → Update status to "in_progress"

5. GET /tasks?status=in_progress → Shows only "Design Database"

6. PATCH /tasks/def-456 → Update status to "completed"

7. GET /tasks/stats/summary → Shows: 1 pending, 1 in_progress, 0 completed

8. DELETE /tasks/abc-123 → Remove "Design Database"

9. GET /tasks → Now shows only 1 task
```

---

## What Makes This API Great

**Clean Code** - Well-organized, documented, and maintainable
**Complete** - All required features implemented
**Tested** - Comprehensive test suite with 11 passing tests
**User-Friendly** - Interactive API documentation
**Robust** - Proper error handling and validation
**Fast** - In-memory storage for quick response times
**RESTful** - Follows REST API best practices
**Pydantic Models** - Type-safe with automatic validation

---

## Support

For more information:
- Refer to README.md for detailed API documentation
- Check TEST_RESULTS.md for proof of working endpoints
- Visit http://localhost:8000/docs for interactive testing
- Review app.py source code for implementation details

---

## Learning Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **Uvicorn Documentation:** https://www.uvicorn.org/
- **Python UUID Documentation:** https://docs.python.org/3/library/uuid.html

---

## Verification Checklist

Before using the API, verify:

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server running (`python app.py`)
- [ ] Can access http://localhost:8000/docs
- [ ] Health check responds (GET /)
- [ ] Can create a task (POST /tasks)
- [ ] Can list tasks (GET /tasks)
- [ ] Can update task status (PATCH /tasks/{id})
- [ ] Test suite passes (`python test_api.py`)

---

## You're Ready!

Your Task Management API is now ready to use. Start with the Swagger UI at:

**http://localhost:8000/docs**

Happy task managing!

---

**Created:** February 9, 2026
**Status:** Production Ready for Demonstration
**Tests:** All 11 Tests Passing
