"""
Base agent classes and interfaces for the modular AI assistant system.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REQUIRES_CLARIFICATION = "requires_clarification"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Task:
    """Represents a task that can be executed by agents"""
    id: str
    description: str
    task_type: str
    payload: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_agent: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    parent_task_id: Optional[str] = None
    created_by: Optional[str] = None

@dataclass
class AgentResponse:
    """Standard response format from agents"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    tasks_created: List[Task] = None
    requires_clarification: bool = False
    clarification_question: Optional[str] = None

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.is_active = True
        
    @abstractmethod
    def can_handle(self, task: Task) -> bool:
        """Check if this agent can handle the given task"""
        pass
    
    @abstractmethod
    def execute_task(self, task: Task) -> AgentResponse:
        """Execute the given task and return a response"""
        pass
    
    def get_capabilities(self) -> List[str]:
        """Return list of task types this agent can handle"""
        return []
    
    def __str__(self):
        return f"{self.name} ({self.agent_id})"

class PersonaAgent(BaseAgent):
    """Base class for conversational persona agents"""
    
    def __init__(self, agent_id: str, name: str, description: str, personality_type: str):
        super().__init__(agent_id, name, description)
        self.personality_type = personality_type
        
    @abstractmethod
    def interpret_user_intent(self, user_message: str) -> List[Task]:
        """Interpret user message and create actionable tasks"""
        pass
    
    @abstractmethod
    def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate a conversational response to user message"""
        pass

class SupervisorAgent(BaseAgent):
    """Base class for supervisor agents that coordinate other agents"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description)
        self.sub_agents: List[BaseAgent] = []
        
    def add_sub_agent(self, agent: BaseAgent):
        """Add a sub-agent to this supervisor"""
        self.sub_agents.append(agent)
        
    def find_capable_agent(self, task: Task) -> Optional[BaseAgent]:
        """Find a sub-agent capable of handling the task"""
        for agent in self.sub_agents:
            if agent.is_active and agent.can_handle(task):
                return agent
        return None
    
    def delegate_task(self, task: Task) -> AgentResponse:
        """Delegate task to appropriate sub-agent"""
        capable_agent = self.find_capable_agent(task)
        if not capable_agent:
            return AgentResponse(
                success=False,
                message=f"No agent found capable of handling task: {task.task_type}",
                requires_clarification=True,
                clarification_question="Could you provide more details or rephrase your request?"
            )
        
        task.assigned_agent = capable_agent.agent_id
        task.status = TaskStatus.IN_PROGRESS
        return capable_agent.execute_task(task)

class PlatformAgent(SupervisorAgent):
    """Base class for platform-specific supervisor agents"""
    
    def __init__(self, agent_id: str, name: str, description: str, platform_name: str):
        super().__init__(agent_id, name, description)
        self.platform_name = platform_name
        
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the platform"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test connection to the platform"""
        pass

class SubAgent(BaseAgent):
    """Base class for focused, task-specific agents"""
    
    def __init__(self, agent_id: str, name: str, description: str, supported_tasks: List[str]):
        super().__init__(agent_id, name, description)
        self.supported_tasks = supported_tasks
        
    def can_handle(self, task: Task) -> bool:
        """Check if this agent can handle the task type"""
        return task.task_type in self.supported_tasks
    
    def get_capabilities(self) -> List[str]:
        """Return list of supported task types"""
        return self.supported_tasks.copy()