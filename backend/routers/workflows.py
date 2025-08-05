from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database import get_db, User, Workflow
from backend.routers.auth import get_current_user

router = APIRouter()

# Pydantic models
class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    tasks: List[Dict[str, Any]] = []
    triggers: List[Dict[str, Any]] = []

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tasks: Optional[List[Dict[str, Any]]] = None
    triggers: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None

class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str
    config: Dict[str, Any]
    is_active: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

class WorkflowExecution(BaseModel):
    input_data: Optional[Dict[str, Any]] = {}

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(
    workflow: WorkflowCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new workflow"""
    workflow_engine = request.app.state.workflow_engine
    
    # Create workflow in engine
    workflow_config = {
        "name": workflow.name,
        "description": workflow.description,
        "tasks": workflow.tasks,
        "triggers": workflow.triggers
    }
    
    engine_workflow_id = await workflow_engine.create_workflow(workflow_config)
    
    # Save to database
    db_workflow = Workflow(
        name=workflow.name,
        description=workflow.description,
        config={
            "engine_workflow_id": engine_workflow_id,
            "tasks": workflow.tasks,
            "triggers": workflow.triggers
        },
        owner_id=current_user.id
    )
    
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    
    return db_workflow

@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all workflows for the current user"""
    workflows = db.query(Workflow).filter(Workflow.owner_id == current_user.id).all()
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific workflow"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow

@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a workflow"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Update fields
    if workflow_update.name is not None:
        workflow.name = workflow_update.name
    if workflow_update.description is not None:
        workflow.description = workflow_update.description
    if workflow_update.is_active is not None:
        workflow.is_active = workflow_update.is_active
    
    # Update config
    if workflow_update.tasks is not None or workflow_update.triggers is not None:
        config = workflow.config.copy()
        if workflow_update.tasks is not None:
            config["tasks"] = workflow_update.tasks
        if workflow_update.triggers is not None:
            config["triggers"] = workflow_update.triggers
        workflow.config = config
    
    workflow.updated_at = datetime.now()
    
    db.commit()
    db.refresh(workflow)
    
    return workflow

@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a workflow"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Delete from engine
    workflow_engine = request.app.state.workflow_engine
    engine_workflow_id = workflow.config.get("engine_workflow_id")
    if engine_workflow_id:
        workflow_engine.delete_workflow(engine_workflow_id)
    
    # Delete from database
    db.delete(workflow)
    db.commit()
    
    return {"message": "Workflow deleted successfully"}

@router.post("/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: int,
    execution: WorkflowExecution,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a workflow"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if not workflow.is_active:
        raise HTTPException(status_code=400, detail="Workflow is not active")
    
    # Execute workflow
    workflow_engine = request.app.state.workflow_engine
    engine_workflow_id = workflow.config.get("engine_workflow_id")
    
    if not engine_workflow_id:
        raise HTTPException(status_code=400, detail="Workflow not properly configured")
    
    result = await workflow_engine.execute_workflow(engine_workflow_id, execution.input_data)
    
    return result

@router.get("/{workflow_id}/status")
async def get_workflow_status(
    workflow_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workflow execution status"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow_engine = request.app.state.workflow_engine
    engine_workflow_id = workflow.config.get("engine_workflow_id")
    
    if not engine_workflow_id:
        raise HTTPException(status_code=400, detail="Workflow not properly configured")
    
    status = workflow_engine.get_workflow_status(engine_workflow_id)
    
    return status

@router.post("/{workflow_id}/pause")
async def pause_workflow(
    workflow_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Pause a running workflow"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow_engine = request.app.state.workflow_engine
    engine_workflow_id = workflow.config.get("engine_workflow_id")
    
    if not engine_workflow_id:
        raise HTTPException(status_code=400, detail="Workflow not properly configured")
    
    success = await workflow_engine.pause_workflow(engine_workflow_id)
    
    if success:
        return {"message": "Workflow paused successfully"}
    else:
        raise HTTPException(status_code=400, detail="Could not pause workflow")

@router.post("/{workflow_id}/resume")
async def resume_workflow(
    workflow_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Resume a paused workflow"""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.owner_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow_engine = request.app.state.workflow_engine
    engine_workflow_id = workflow.config.get("engine_workflow_id")
    
    if not engine_workflow_id:
        raise HTTPException(status_code=400, detail="Workflow not properly configured")
    
    success = await workflow_engine.resume_workflow(engine_workflow_id)
    
    if success:
        return {"message": "Workflow resumed successfully"}
    else:
        raise HTTPException(status_code=400, detail="Could not resume workflow")

@router.get("/templates/")
async def get_workflow_templates():
    """Get predefined workflow templates"""
    templates = [
        {
            "id": "data_analysis",
            "name": "Data Analysis Workflow",
            "description": "Automated data analysis and reporting",
            "tasks": [
                {
                    "name": "Load Data",
                    "type": "data_processing",
                    "config": {"source": "file", "format": "csv"}
                },
                {
                    "name": "Analyze Data",
                    "type": "ai_task",
                    "agent": {"type": "openai", "tools": ["data_analysis"]},
                    "prompt": "Analyze the provided data and generate insights"
                },
                {
                    "name": "Generate Report",
                    "type": "ai_task",
                    "agent": {"type": "openai", "tools": ["file_processor"]},
                    "prompt": "Create a comprehensive report based on the analysis"
                }
            ]
        },
        {
            "id": "content_generation",
            "name": "Content Generation Workflow",
            "description": "AI-powered content creation and publishing",
            "tasks": [
                {
                    "name": "Generate Content",
                    "type": "ai_task",
                    "agent": {"type": "openai", "tools": ["web_search"]},
                    "prompt": "Generate engaging content based on the topic"
                },
                {
                    "name": "Review Content",
                    "type": "ai_task",
                    "agent": {"type": "anthropic", "tools": []},
                    "prompt": "Review and improve the generated content"
                },
                {
                    "name": "Publish Content",
                    "type": "api_call",
                    "config": {"endpoint": "/publish", "method": "POST"}
                }
            ]
        },
        {
            "id": "email_automation",
            "name": "Email Marketing Automation",
            "description": "Automated email campaigns with AI personalization",
            "tasks": [
                {
                    "name": "Segment Audience",
                    "type": "data_processing",
                    "config": {"criteria": "engagement_score"}
                },
                {
                    "name": "Personalize Content",
                    "type": "ai_task",
                    "agent": {"type": "openai", "tools": []},
                    "prompt": "Personalize email content for each segment"
                },
                {
                    "name": "Send Emails",
                    "type": "notification",
                    "config": {"type": "email", "batch_size": 100}
                }
            ]
        }
    ]
    
    return templates