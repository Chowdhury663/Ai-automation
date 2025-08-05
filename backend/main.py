from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from backend.database import create_tables
from backend.routers import auth, workflows, agents, tasks, analytics
from backend.core.ai_manager import AIManager
from backend.core.workflow_engine import WorkflowEngine

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_tables()
    
    # Initialize AI Manager
    ai_manager = AIManager()
    app.state.ai_manager = ai_manager
    
    # Initialize Workflow Engine
    workflow_engine = WorkflowEngine(ai_manager)
    app.state.workflow_engine = workflow_engine
    
    yield
    
    # Shutdown
    pass

app = FastAPI(
    title="AI Automation Platform",
    description="A comprehensive AI-powered automation platform suite",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(agents.router, prefix="/api/agents", tags=["ai-agents"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {
        "message": "AI Automation Platform API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )