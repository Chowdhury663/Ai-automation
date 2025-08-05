from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from backend.database import get_db, User, Task, Workflow, Agent
from backend.routers.auth import get_current_user

router = APIRouter()

class AnalyticsResponse(BaseModel):
    period: str
    data: Dict[str, Any]

@router.get("/dashboard")
async def get_dashboard_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard analytics"""
    
    # Time periods
    now = datetime.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    # Task statistics
    total_tasks = db.query(Task).filter(Task.user_id == current_user.id).count()
    tasks_24h = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.created_at >= last_24h
    ).count()
    
    completed_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "completed"
    ).count()
    
    failed_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == "failed"
    ).count()
    
    # Workflow statistics
    total_workflows = db.query(Workflow).filter(Workflow.owner_id == current_user.id).count()
    active_workflows = db.query(Workflow).filter(
        Workflow.owner_id == current_user.id,
        Workflow.is_active == True
    ).count()
    
    # Agent statistics
    total_agents = db.query(Agent).filter(Agent.is_active == True).count()
    
    # Recent activity
    recent_tasks = db.query(Task).filter(
        Task.user_id == current_user.id
    ).order_by(Task.created_at.desc()).limit(10).all()
    
    # Task completion rate over time (last 7 days)
    completion_rate_data = []
    for i in range(7):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_total = db.query(Task).filter(
            Task.user_id == current_user.id,
            Task.created_at >= day_start,
            Task.created_at < day_end
        ).count()
        
        day_completed = db.query(Task).filter(
            Task.user_id == current_user.id,
            Task.created_at >= day_start,
            Task.created_at < day_end,
            Task.status == "completed"
        ).count()
        
        completion_rate = (day_completed / day_total * 100) if day_total > 0 else 0
        
        completion_rate_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "total_tasks": day_total,
            "completed_tasks": day_completed,
            "completion_rate": completion_rate
        })
    
    return {
        "summary": {
            "total_tasks": total_tasks,
            "tasks_24h": tasks_24h,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "success_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "total_workflows": total_workflows,
            "active_workflows": active_workflows,
            "total_agents": total_agents
        },
        "recent_activity": [
            {
                "id": task.id,
                "name": task.name,
                "status": task.status,
                "created_at": task.created_at.isoformat(),
                "workflow_id": task.workflow_id
            } for task in recent_tasks
        ],
        "completion_rate_trend": completion_rate_data
    }

@router.get("/tasks/timeline")
async def get_tasks_timeline(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get task execution timeline"""
    
    now = datetime.now()
    start_date = now - timedelta(days=days)
    
    # Group tasks by day and status
    timeline_data = []
    
    for i in range(days):
        day = start_date + timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        # Get task counts by status for this day
        day_tasks = db.query(
            Task.status,
            func.count(Task.id).label('count')
        ).filter(
            Task.user_id == current_user.id,
            Task.created_at >= day_start,
            Task.created_at < day_end
        ).group_by(Task.status).all()
        
        status_counts = {status: count for status, count in day_tasks}
        
        timeline_data.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "pending": status_counts.get("pending", 0),
            "running": status_counts.get("running", 0),
            "completed": status_counts.get("completed", 0),
            "failed": status_counts.get("failed", 0),
            "total": sum(status_counts.values())
        })
    
    return {"timeline": timeline_data}

@router.get("/workflows/performance")
async def get_workflow_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow performance metrics"""
    
    # Get workflow performance data
    workflow_stats = db.query(
        Workflow.id,
        Workflow.name,
        func.count(Task.id).label('total_tasks'),
        func.sum(func.case([(Task.status == 'completed', 1)], else_=0)).label('completed_tasks'),
        func.sum(func.case([(Task.status == 'failed', 1)], else_=0)).label('failed_tasks'),
        func.avg(
            func.case([
                (Task.completed_at.isnot(None), 
                 func.extract('epoch', Task.completed_at - Task.created_at))
            ], else_=None)
        ).label('avg_execution_time')
    ).join(
        Task, Workflow.id == Task.workflow_id, isouter=True
    ).filter(
        Workflow.owner_id == current_user.id
    ).group_by(Workflow.id, Workflow.name).all()
    
    performance_data = []
    for stat in workflow_stats:
        success_rate = (stat.completed_tasks / stat.total_tasks * 100) if stat.total_tasks > 0 else 0
        avg_time = stat.avg_execution_time or 0
        
        performance_data.append({
            "workflow_id": stat.id,
            "workflow_name": stat.name,
            "total_tasks": stat.total_tasks,
            "completed_tasks": stat.completed_tasks,
            "failed_tasks": stat.failed_tasks,
            "success_rate": success_rate,
            "avg_execution_time_seconds": avg_time
        })
    
    return {"workflows": performance_data}

@router.get("/agents/usage")
async def get_agent_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get agent usage statistics"""
    
    agent_stats = db.query(
        Agent.id,
        Agent.name,
        Agent.type,
        func.count(Task.id).label('total_tasks'),
        func.sum(func.case([(Task.status == 'completed', 1)], else_=0)).label('completed_tasks'),
        func.sum(func.case([(Task.status == 'failed', 1)], else_=0)).label('failed_tasks')
    ).join(
        Task, Agent.id == Task.agent_id, isouter=True
    ).filter(
        Task.user_id == current_user.id
    ).group_by(Agent.id, Agent.name, Agent.type).all()
    
    usage_data = []
    for stat in agent_stats:
        success_rate = (stat.completed_tasks / stat.total_tasks * 100) if stat.total_tasks > 0 else 0
        
        usage_data.append({
            "agent_id": stat.id,
            "agent_name": stat.name,
            "agent_type": stat.type,
            "total_tasks": stat.total_tasks,
            "completed_tasks": stat.completed_tasks,
            "failed_tasks": stat.failed_tasks,
            "success_rate": success_rate
        })
    
    return {"agents": usage_data}

@router.get("/system/health")
async def get_system_health(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system health metrics"""
    
    now = datetime.now()
    last_hour = now - timedelta(hours=1)
    
    # Recent error rate
    recent_tasks = db.query(Task).filter(
        Task.created_at >= last_hour
    ).count()
    
    recent_failures = db.query(Task).filter(
        Task.created_at >= last_hour,
        Task.status == "failed"
    ).count()
    
    error_rate = (recent_failures / recent_tasks * 100) if recent_tasks > 0 else 0
    
    # System status
    active_workflows = db.query(Workflow).filter(Workflow.is_active == True).count()
    active_agents = db.query(Agent).filter(Agent.is_active == True).count()
    
    # Running tasks
    running_tasks = db.query(Task).filter(Task.status == "running").count()
    
    return {
        "status": "healthy" if error_rate < 10 else "warning" if error_rate < 25 else "critical",
        "error_rate": error_rate,
        "active_workflows": active_workflows,
        "active_agents": active_agents,
        "running_tasks": running_tasks,
        "last_updated": now.isoformat()
    }