from typing import Dict, List, Any, Optional
import openai
import anthropic
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
import os
import asyncio
import json
from datetime import datetime

class AIManager:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.agents = {}
        self.tools = {}
        self._initialize_clients()
        self._initialize_default_tools()
    
    def _initialize_clients(self):
        """Initialize AI provider clients"""
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if openai_key:
            openai.api_key = openai_key
            self.openai_client = ChatOpenAI(
                temperature=0.7,
                model_name="gpt-4-turbo-preview"
            )
        
        if anthropic_key:
            self.anthropic_client = ChatAnthropic(
                anthropic_api_key=anthropic_key,
                model="claude-3-sonnet-20240229"
            )
    
    def _initialize_default_tools(self):
        """Initialize default tools for AI agents"""
        self.tools = {
            "web_search": Tool(
                name="Web Search",
                description="Search the web for information",
                func=self._web_search_tool
            ),
            "data_analysis": Tool(
                name="Data Analysis",
                description="Analyze data and generate insights",
                func=self._data_analysis_tool
            ),
            "email_sender": Tool(
                name="Email Sender",
                description="Send emails to specified recipients",
                func=self._email_sender_tool
            ),
            "file_processor": Tool(
                name="File Processor",
                description="Process and analyze files",
                func=self._file_processor_tool
            ),
            "api_caller": Tool(
                name="API Caller",
                description="Make API calls to external services",
                func=self._api_caller_tool
            ),
            "scheduler": Tool(
                name="Scheduler",
                description="Schedule tasks and reminders",
                func=self._scheduler_tool
            )
        }
    
    async def create_agent(self, agent_config: Dict[str, Any]) -> str:
        """Create a new AI agent with specified configuration"""
        agent_id = f"agent_{len(self.agents) + 1}_{int(datetime.now().timestamp())}"
        
        agent_type = agent_config.get("type", "openai")
        tools = [self.tools[tool] for tool in agent_config.get("tools", [])]
        
        if agent_type == "openai" and self.openai_client:
            llm = self.openai_client
        elif agent_type == "anthropic" and self.anthropic_client:
            llm = self.anthropic_client
        else:
            raise ValueError(f"Unsupported agent type: {agent_type}")
        
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=memory,
            verbose=True
        )
        
        self.agents[agent_id] = {
            "agent": agent,
            "config": agent_config,
            "created_at": datetime.now(),
            "status": "active"
        }
        
        return agent_id
    
    async def execute_task(self, agent_id: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the specified agent"""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        agent_info = self.agents[agent_id]
        agent = agent_info["agent"]
        
        try:
            task_input = task.get("input", "")
            context = task.get("context", {})
            
            # Prepare the input with context
            full_input = f"""
            Task: {task_input}
            Context: {json.dumps(context, indent=2)}
            
            Please execute this task and provide a detailed response.
            """
            
            result = await asyncio.to_thread(agent.run, full_input)
            
            return {
                "success": True,
                "result": result,
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _web_search_tool(self, query: str) -> str:
        """Tool for web searching"""
        # Implement web search functionality
        return f"Web search results for: {query}"
    
    async def _data_analysis_tool(self, data: str) -> str:
        """Tool for data analysis"""
        # Implement data analysis functionality
        return f"Data analysis completed for: {data}"
    
    async def _email_sender_tool(self, email_data: str) -> str:
        """Tool for sending emails"""
        # Implement email sending functionality
        return f"Email sent: {email_data}"
    
    async def _file_processor_tool(self, file_path: str) -> str:
        """Tool for file processing"""
        # Implement file processing functionality
        return f"File processed: {file_path}"
    
    async def _api_caller_tool(self, api_config: str) -> str:
        """Tool for making API calls"""
        # Implement API calling functionality
        return f"API call completed: {api_config}"
    
    async def _scheduler_tool(self, schedule_data: str) -> str:
        """Tool for scheduling tasks"""
        # Implement scheduling functionality
        return f"Task scheduled: {schedule_data}"
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        if agent_id not in self.agents:
            return {"error": "Agent not found"}
        
        agent_info = self.agents[agent_id]
        return {
            "agent_id": agent_id,
            "status": agent_info["status"],
            "created_at": agent_info["created_at"].isoformat(),
            "config": agent_info["config"]
        }
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all agents"""
        return [
            {
                "agent_id": agent_id,
                "status": info["status"],
                "created_at": info["created_at"].isoformat(),
                "config": info["config"]
            }
            for agent_id, info in self.agents.items()
        ]
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False