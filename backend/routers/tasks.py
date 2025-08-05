from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database import get_db, User, Task
from backend.routers.auth import get_current_user

router = APIRouter()

# Pydantic models
class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    error_message: Optional[str]
    workflow_id: Optional[int]
    agent_id: Optional[int]
    user_id: int
    created_at: datetime
    completed_at: Optional[datetime]

@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = None,
    workflow_id: Optional[int] = None,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List tasks for the current user"""
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    if status:
        query = query.filter(Task.status == status)
    
    if workflow_id:
        query = query.filter(Task.workflow_id == workflow_id)
    
    tasks = query.order_by(Task.created_at.desc()).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}

@router.get("/stats/summary")
async def get_task_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get task statistics summary"""
    total_tasks = db.query(Task).filter(Task.user_id == current_user.id).count()
    
    completed_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "completed"
    ).count()
    
    failed_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "failed"
    ).count()
    
    running_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "running"
    ).count()
    
    pending_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "pending"
    ).count()
    
    return {
        "total": total_tasks,
        "completed": completed_tasks,
        "failed": failed_tasks,
        "running": running_tasks,
        "pending": pending_tasks,
        "success_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }