from typing import Dict, List, Any, Optional
import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum
import schedule
import time
from threading import Thread

from backend.core.ai_manager import AIManager

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class WorkflowEngine:
    def __init__(self, ai_manager: AIManager):
        self.ai_manager = ai_manager
        self.workflows = {}
        self.running_workflows = {}
        self.scheduler_thread = None
        self.start_scheduler()
    
    def start_scheduler(self):
        """Start the background scheduler for automated workflows"""
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
    
    async def create_workflow(self, workflow_config: Dict[str, Any]) -> str:
        """Create a new workflow"""
        workflow_id = f"workflow_{len(self.workflows) + 1}_{int(datetime.now().timestamp())}"
        
        workflow = {
            "id": workflow_id,
            "name": workflow_config.get("name", f"Workflow {workflow_id}"),
            "description": workflow_config.get("description", ""),
            "tasks": workflow_config.get("tasks", []),
            "triggers": workflow_config.get("triggers", []),
            "status": WorkflowStatus.PENDING.value,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "execution_history": []
        }
        
        self.workflows[workflow_id] = workflow
        
        # Set up triggers
        await self._setup_triggers(workflow_id, workflow["triggers"])
        
        return workflow_id
    
    async def _setup_triggers(self, workflow_id: str, triggers: List[Dict[str, Any]]):
        """Set up triggers for a workflow"""
        for trigger in triggers:
            trigger_type = trigger.get("type")
            
            if trigger_type == "schedule":
                await self._setup_schedule_trigger(workflow_id, trigger)
            elif trigger_type == "webhook":
                await self._setup_webhook_trigger(workflow_id, trigger)
            elif trigger_type == "event":
                await self._setup_event_trigger(workflow_id, trigger)
    
    async def _setup_schedule_trigger(self, workflow_id: str, trigger: Dict[str, Any]):
        """Set up scheduled trigger"""
        schedule_config = trigger.get("config", {})
        interval = schedule_config.get("interval", "daily")
        time_str = schedule_config.get("time", "09:00")
        
        def trigger_workflow():
            asyncio.create_task(self.execute_workflow(workflow_id))
        
        if interval == "daily":
            schedule.every().day.at(time_str).do(trigger_workflow)
        elif interval == "hourly":
            schedule.every().hour.do(trigger_workflow)
        elif interval == "weekly":
            day = schedule_config.get("day", "monday")
            getattr(schedule.every(), day).at(time_str).do(trigger_workflow)
    
    async def _setup_webhook_trigger(self, workflow_id: str, trigger: Dict[str, Any]):
        """Set up webhook trigger"""
        # Webhook triggers would be handled by the API endpoints
        pass
    
    async def _setup_event_trigger(self, workflow_id: str, trigger: Dict[str, Any]):
        """Set up event-based trigger"""
        # Event triggers would be handled by event listeners
        pass
    
    async def execute_workflow(self, workflow_id: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a workflow"""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        
        if workflow_id in self.running_workflows:
            return {"error": "Workflow is already running"}
        
        execution_id = f"exec_{workflow_id}_{int(datetime.now().timestamp())}"
        
        execution = {
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "status": WorkflowStatus.RUNNING.value,
            "started_at": datetime.now(),
            "input_data": input_data or {},
            "tasks": [],
            "output_data": {},
            "error_message": None
        }
        
        self.running_workflows[workflow_id] = execution
        workflow["status"] = WorkflowStatus.RUNNING.value
        
        try:
            # Execute tasks in sequence
            context = input_data or {}
            
            for i, task_config in enumerate(workflow["tasks"]):
                task_result = await self._execute_task(
                    workflow_id, 
                    execution_id, 
                    task_config, 
                    context
                )
                
                execution["tasks"].append(task_result)
                
                if not task_result["success"]:
                    # Handle task failure
                    if task_config.get("on_failure") == "continue":
                        continue
                    else:
                        execution["status"] = WorkflowStatus.FAILED.value
                        execution["error_message"] = task_result.get("error")
                        break
                
                # Update context with task output
                context.update(task_result.get("output", {}))
            
            if execution["status"] == WorkflowStatus.RUNNING.value:
                execution["status"] = WorkflowStatus.COMPLETED.value
                execution["output_data"] = context
            
        except Exception as e:
            execution["status"] = WorkflowStatus.FAILED.value
            execution["error_message"] = str(e)
        
        finally:
            execution["completed_at"] = datetime.now()
            workflow["status"] = execution["status"]
            workflow["updated_at"] = datetime.now()
            workflow["execution_history"].append(execution)
            
            # Remove from running workflows
            if workflow_id in self.running_workflows:
                del self.running_workflows[workflow_id]
        
        return execution
    
    async def _execute_task(self, workflow_id: str, execution_id: str, task_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single task within a workflow"""
        task_result = {
            "task_name": task_config.get("name", "Unnamed Task"),
            "task_type": task_config.get("type", "ai_task"),
            "status": TaskStatus.RUNNING.value,
            "started_at": datetime.now(),
            "success": False,
            "output": {},
            "error": None
        }
        
        try:
            task_type = task_config.get("type", "ai_task")
            
            if task_type == "ai_task":
                result = await self._execute_ai_task(task_config, context)
            elif task_type == "api_call":
                result = await self._execute_api_call(task_config, context)
            elif task_type == "data_processing":
                result = await self._execute_data_processing(task_config, context)
            elif task_type == "notification":
                result = await self._execute_notification(task_config, context)
            else:
                result = {"success": False, "error": f"Unknown task type: {task_type}"}
            
            task_result["success"] = result.get("success", False)
            task_result["output"] = result.get("output", {})
            task_result["error"] = result.get("error")
            task_result["status"] = TaskStatus.COMPLETED.value if task_result["success"] else TaskStatus.FAILED.value
            
        except Exception as e:
            task_result["success"] = False
            task_result["error"] = str(e)
            task_result["status"] = TaskStatus.FAILED.value
        
        finally:
            task_result["completed_at"] = datetime.now()
        
        return task_result
    
    async def _execute_ai_task(self, task_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an AI-powered task"""
        agent_config = task_config.get("agent", {})
        
        # Create or get agent
        agent_id = await self.ai_manager.create_agent(agent_config)
        
        # Prepare task
        task = {
            "input": task_config.get("prompt", ""),
            "context": context
        }
        
        # Execute task
        result = await self.ai_manager.execute_task(agent_id, task)
        
        return {
            "success": result.get("success", False),
            "output": {"ai_response": result.get("result")},
            "error": result.get("error")
        }
    
    async def _execute_api_call(self, task_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an API call task"""
        # Implement API call functionality
        return {
            "success": True,
            "output": {"api_response": "API call completed"},
            "error": None
        }
    
    async def _execute_data_processing(self, task_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a data processing task"""
        # Implement data processing functionality
        return {
            "success": True,
            "output": {"processed_data": "Data processed"},
            "error": None
        }
    
    async def _execute_notification(self, task_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a notification task"""
        # Implement notification functionality
        return {
            "success": True,
            "output": {"notification_sent": True},
            "error": None
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the status of a workflow"""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "name": workflow["name"],
            "status": workflow["status"],
            "created_at": workflow["created_at"].isoformat(),
            "updated_at": workflow["updated_at"].isoformat(),
            "execution_count": len(workflow["execution_history"]),
            "is_running": workflow_id in self.running_workflows
        }
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows"""
        return [
            {
                "workflow_id": workflow_id,
                "name": workflow["name"],
                "description": workflow["description"],
                "status": workflow["status"],
                "created_at": workflow["created_at"].isoformat(),
                "task_count": len(workflow["tasks"])
            }
            for workflow_id, workflow in self.workflows.items()
        ]
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow"""
        if workflow_id in self.workflows:
            # Stop if running
            if workflow_id in self.running_workflows:
                del self.running_workflows[workflow_id]
            
            del self.workflows[workflow_id]
            return True
        return False
    
    async def pause_workflow(self, workflow_id: str) -> bool:
        """Pause a running workflow"""
        if workflow_id in self.running_workflows:
            self.running_workflows[workflow_id]["status"] = WorkflowStatus.PAUSED.value
            return True
        return False
    
    async def resume_workflow(self, workflow_id: str) -> bool:
        """Resume a paused workflow"""
        if workflow_id in self.running_workflows:
            self.running_workflows[workflow_id]["status"] = WorkflowStatus.RUNNING.value
            return True
        return False