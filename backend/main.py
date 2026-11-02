from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

class Task(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=100)
    completed: bool = False
    description: Optional[str] = None

app = FastAPI(
    title="SaaS Project Management API",
    description="Multi-tenant project management platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to SaaS Project Management API"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

tasks = []
@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task.model_dump())
    return{
        "message" : "Task created successfully",
        "task" : task
    }

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: dict):
    for index,task in enumerate(tasks):
        if task["id"] == task_id:
            task[index] = updated_task
            return {
                "message": "Task replaced successfully",
                "task": updated_task
            }

    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/task/{task_id}")
def patch_task(task_id: int, updates: dict):

    for task in tasks:
        if task["id"] == task_id:
            task.update(updates)

            return {
                "message": "Task updated successfully",
                "task": task
            }

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }
        raise HTTPException(status_code=404, detail="Task not found")