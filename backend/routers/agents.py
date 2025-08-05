from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from backend.database import get_db, User, Agent
from backend.routers.auth import get_current_user

router = APIRouter()

# Pydantic models
class AgentCreate(BaseModel):
    name: str
    type: str  # 'openai', 'anthropic', 'custom'
    description: Optional[str] = ""
    config: Dict[str, Any] = {}

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class AgentResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str
    config: Dict[str, Any]
    is_active: bool
    created_at: datetime

class TaskExecution(BaseModel):
    input: str
    context: Optional[Dict[str, Any]] = {}

@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent: AgentCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new AI agent"""
    ai_manager = request.app.state.ai_manager
    
    # Create agent in AI manager
    agent_config = {
        "type": agent.type,
        "name": agent.name,
        "description": agent.description,
        **agent.config
    }
    
    try:
        engine_agent_id = await ai_manager.create_agent(agent_config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create agent: {str(e)}")
    
    # Save to database
    db_agent = Agent(
        name=agent.name,
        type=agent.type,
        description=agent.description,
        config={
            "engine_agent_id": engine_agent_id,
            **agent.config
        }
    )
    
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    return db_agent

@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all available agents"""
    agents = db.query(Agent).filter(Agent.is_active == True).all()
    return agents

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Update fields
    if agent_update.name is not None:
        agent.name = agent_update.name
    if agent_update.description is not None:
        agent.description = agent_update.description
    if agent_update.is_active is not None:
        agent.is_active = agent_update.is_active
    if agent_update.config is not None:
        config = agent.config.copy()
        config.update(agent_update.config)
        agent.config = config
    
    db.commit()
    db.refresh(agent)
    
    return agent

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Delete from AI manager
    ai_manager = request.app.state.ai_manager
    engine_agent_id = agent.config.get("engine_agent_id")
    if engine_agent_id:
        ai_manager.delete_agent(engine_agent_id)
    
    # Delete from database
    db.delete(agent)
    db.commit()
    
    return {"message": "Agent deleted successfully"}

@router.post("/{agent_id}/execute")
async def execute_task(
    agent_id: int,
    task: TaskExecution,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute a task using the specified agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if not agent.is_active:
        raise HTTPException(status_code=400, detail="Agent is not active")
    
    # Execute task
    ai_manager = request.app.state.ai_manager
    engine_agent_id = agent.config.get("engine_agent_id")
    
    if not engine_agent_id:
        raise HTTPException(status_code=400, detail="Agent not properly configured")
    
    task_data = {
        "input": task.input,
        "context": task.context
    }
    
    result = await ai_manager.execute_task(engine_agent_id, task_data)
    
    return result

@router.get("/{agent_id}/status")
async def get_agent_status(
    agent_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get agent status"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    ai_manager = request.app.state.ai_manager
    engine_agent_id = agent.config.get("engine_agent_id")
    
    if not engine_agent_id:
        return {"status": "not_configured"}
    
    status = ai_manager.get_agent_status(engine_agent_id)
    
    return status

@router.get("/types/")
async def get_agent_types():
    """Get available agent types and their configurations"""
    return {
        "types": [
            {
                "id": "openai",
                "name": "OpenAI GPT",
                "description": "OpenAI's GPT models for general AI tasks",
                "config_schema": {
                    "model": {"type": "string", "default": "gpt-4-turbo-preview"},
                    "temperature": {"type": "number", "default": 0.7, "min": 0, "max": 2},
                    "max_tokens": {"type": "integer", "default": 1000},
                    "tools": {"type": "array", "items": {"type": "string"}}
                }
            },
            {
                "id": "anthropic",
                "name": "Anthropic Claude",
                "description": "Anthropic's Claude models for reasoning and analysis",
                "config_schema": {
                    "model": {"type": "string", "default": "claude-3-sonnet-20240229"},
                    "temperature": {"type": "number", "default": 0.7, "min": 0, "max": 1},
                    "max_tokens": {"type": "integer", "default": 1000},
                    "tools": {"type": "array", "items": {"type": "string"}}
                }
            }
        ],
        "tools": [
            {
                "id": "web_search",
                "name": "Web Search",
                "description": "Search the web for information"
            },
            {
                "id": "data_analysis",
                "name": "Data Analysis",
                "description": "Analyze data and generate insights"
            },
            {
                "id": "email_sender",
                "name": "Email Sender",
                "description": "Send emails to specified recipients"
            },
            {
                "id": "file_processor",
                "name": "File Processor",
                "description": "Process and analyze files"
            },
            {
                "id": "api_caller",
                "name": "API Caller",
                "description": "Make API calls to external services"
            },
            {
                "id": "scheduler",
                "name": "Scheduler",
                "description": "Schedule tasks and reminders"
            }
        ]
    }