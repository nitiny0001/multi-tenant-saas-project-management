from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

class Taskcreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    completed: bool = False
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5)

class Taskupdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=100)
    completed: Optional[bool] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)


class Taskresponse(Taskcreate):
    id: int

class Taskmutationresponse(BaseModel):
    message: str
    task: Taskresponse

class Taskcreateresponse(BaseModel):
    message: str
    task: Taskresponse

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
@app.get("/tasks", response_model = list[Taskresponse])
def get_tasks():
    return tasks

@app.post("/tasks", response_model = Taskmutationresponse)
def create_task(task: Taskcreate):
    new_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = Taskresponse(
        id = new_id,
        **task.model_dump()
    )
    tasks.append(new_task.model_dump())
    return{
        "message" : "Task created successfully",
        "task" : new_task
    }

@app.put("/tasks/{task_id}", response_model=Taskmutationresponse)
def update_task(task_id: int, updated_task: Taskcreate):
    for index,task in enumerate(tasks):
        if task["id"] == task_id:
            

            new_task = Taskresponse(
                id=task_id,
                **updated_task.model_dump()
            )

            tasks[index] = new_task.model_dump()

            return {
                "message": "Task replaced successfully",
                "task": new_task
            }

    raise HTTPException(status_code=404, detail="Task not found")

@app.patch("/tasks/{task_id}",response_model=Taskmutationresponse)
def patch_task(task_id: int, updates: Taskupdate):

    for task in tasks:
        if task["id"] == task_id:
            update_data = updates.model_dump(exclude_unset=True)
            for field in ("title", "completed", "priority"):
                if field in update_data and update_data[field] is None:
                    raise HTTPException(
                        status_code=422,
                        detail=f"{field} cannot be null"
                    )
            task.update(update_data)

            return {
                "message": "Task updated successfully",
                "task": task
            }


    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}",response_model=Taskmutationresponse)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }
    raise HTTPException(status_code=404, detail="Task not found")