"""
FastAPI Task Management System
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="Task Management API",
    description="A simple task management system with create, read, update, and delete operations",
    version="1.0.0"
)

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: str = Field(..., min_length=0, max_length=1000, description="Task description")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, min_length=0, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")


class Task(TaskBase):
    model_config = ConfigDict(use_enum_values=True)
    
    id: str = Field(..., description="Unique task ID")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current task status")
    created_at: datetime = Field(..., description="Task creation timestamp")
    updated_at: datetime = Field(..., description="Task last update timestamp")



tasks_db: dict = {}

def create_task_record(task_id: str, title: str, description: str) -> dict:

    now = datetime.now()
    return {
        "id": task_id,
        "title": title,
        "description": description,
        "status": TaskStatus.PENDING,
        "created_at": now,
        "updated_at": now
    }


def task_dict_to_model(task_dict: dict) -> Task:

    return Task(**task_dict)


# ==================== API Endpoints ====================

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Task Management API is running"}


@app.post("/tasks", response_model=Task, status_code=201, tags=["Tasks"])
async def create_task(task: TaskCreate):

    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Create and store task
    task_record = create_task_record(task_id, task.title, task.description)
    tasks_db[task_id] = task_record
    
    return task_dict_to_model(task_record)


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found"
        )
    
    return task_dict_to_model(tasks_db[task_id])


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def list_tasks(status: Optional[TaskStatus] = Query(None, description="Filter tasks by status")):
    if status is None:
        # Return all tasks
        return [task_dict_to_model(task) for task in tasks_db.values()]
    else:
        # Return filtered tasks
        filtered_tasks = [
            task_dict_to_model(task) 
            for task in tasks_db.values() 
            if task["status"] == status
        ]
        return filtered_tasks


@app.patch("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: str, task_update: TaskUpdate):
    # Check if task exists
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found"
        )
    
    # Get existing task
    existing_task = tasks_db[task_id]
    
    # Update only provided fields
    if task_update.title is not None:
        existing_task["title"] = task_update.title
    
    if task_update.description is not None:
        existing_task["description"] = task_update.description
    
    if task_update.status is not None:
        existing_task["status"] = task_update.status
    
    # Update the timestamp
    existing_task["updated_at"] = datetime.now()
    
    # Update in storage
    tasks_db[task_id] = existing_task
    
    return task_dict_to_model(existing_task)


@app.delete("/tasks/{task_id}", status_code=204, tags=["Tasks"])
async def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=404,
            detail=f"Task with ID '{task_id}' not found"
        )
    
    del tasks_db[task_id]
    return None


@app.get("/tasks/stats/summary", tags=["Statistics"])
async def get_task_summary():
 
    total = len(tasks_db)
    status_breakdown = {
        "pending": 0,
        "in_progress": 0,
        "completed": 0,
        "failed": 0
    }
    
    for task in tasks_db.values():
        status = task["status"]
        status_breakdown[status] += 1
    
    return {
        "total_tasks": total,
        "by_status": status_breakdown
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
