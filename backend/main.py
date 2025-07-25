"""
FastAPI backend for the modular AI assistant system.
Provides REST API endpoints for persona selection, conversations, and task management.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
from datetime import datetime

# Import our agent system
from agents.base import Task, TaskStatus, TaskPriority, AgentResponse
from agents.supervisor import HierarchicalSupervisor  
from agents.personas import HRManagerAgent, ITSupportAgent, DoctorAgent
from agents.platforms import (
    GitHubPlatformAgent, GmailPlatformAgent, 
    JiraPlatformAgent, CalendarPlatformAgent
)
from agents.reflection import ReflectionAgent

# Pydantic models for API requests/responses
class ConversationRequest(BaseModel):
    persona: str
    message: str
    context: Optional[Dict[str, Any]] = {}

class ConversationResponse(BaseModel):
    message: str
    tasks_created: List[Dict[str, Any]] = []
    persona: str
    timestamp: datetime

class TaskRequest(BaseModel):
    description: str
    task_type: str
    payload: Dict[str, Any]
    priority: str = "medium"

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    message: str

class PersonaInfo(BaseModel):
    id: str
    name: str
    description: str
    capabilities: List[str]

class SystemStatus(BaseModel):
    active_personas: List[str]
    platform_status: Dict[str, bool]
    total_tasks_processed: int
    system_health: str

# Initialize FastAPI app
app = FastAPI(
    title="Modular AI Assistant API",
    description="API for workplace automation with multiple conversational personas and hierarchical agent orchestration",
    version="1.0.0"
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent system
supervisor = HierarchicalSupervisor()
reflection_agent = ReflectionAgent()

# Initialize persona agents
personas = {
    "hr_manager": HRManagerAgent(),
    "it_support": ITSupportAgent(),
    "doctor": DoctorAgent()
}

# Initialize platform agents
github_agent = GitHubPlatformAgent()
gmail_agent = GmailPlatformAgent()
jira_agent = JiraPlatformAgent()
calendar_agent = CalendarPlatformAgent()

# Register platform agents with supervisor
supervisor.register_platform_agent("github", github_agent)
supervisor.register_platform_agent("gmail", gmail_agent)
supervisor.register_platform_agent("jira", jira_agent)
supervisor.register_platform_agent("calendar", calendar_agent)

# Global state management
conversation_history: Dict[str, List[Dict[str, Any]]] = {}
task_store: Dict[str, Task] = {}
tasks_processed = 0

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Modular AI Assistant API",
        "version": "1.0.0",
        "description": "Workplace automation with multiple personas and hierarchical agents",
        "endpoints": {
            "personas": "/personas",
            "conversation": "/conversation",
            "tasks": "/tasks",
            "status": "/system/status"
        }
    }

@app.get("/personas", response_model=List[PersonaInfo])
def get_personas():
    """Get list of available persona agents"""
    persona_list = []
    
    for persona_id, persona_agent in personas.items():
        persona_list.append(PersonaInfo(
            id=persona_id,
            name=persona_agent.name,
            description=persona_agent.description,
            capabilities=persona_agent.get_capabilities()
        ))
    
    return persona_list

@app.post("/conversation", response_model=ConversationResponse)
def have_conversation(request: ConversationRequest):
    """Have a conversation with a selected persona"""
    global tasks_processed
    
    # Validate persona
    if request.persona not in personas:
        raise HTTPException(status_code=400, detail=f"Unknown persona: {request.persona}")
    
    persona_agent = personas[request.persona]
    
    # Create conversation task
    conversation_task = Task(
        id=str(uuid.uuid4()),
        description=f"Conversation with {persona_agent.name}",
        task_type="conversation",
        payload={"message": request.message},
        created_by=request.persona
    )
    
    # Execute conversation
    try:
        response = persona_agent.execute_task(conversation_task)
        tasks_processed += 1
        
        # Store conversation in history
        session_id = f"{request.persona}_session"
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        conversation_history[session_id].append({
            "user_message": request.message,
            "agent_response": response.message,
            "timestamp": datetime.now().isoformat(),
            "tasks_created": len(response.tasks_created or [])
        })
        
        # Process any tasks created by the persona
        created_tasks = []
        if response.tasks_created:
            for task in response.tasks_created:
                task_store[task.id] = task
                # Execute task through supervisor
                task_response = supervisor.execute_task(task)
                
                # Evaluate task with reflection agent
                evaluation = reflection_agent.evaluate_task_completion(task, task_response)
                
                created_tasks.append({
                    "task_id": task.id,
                    "task_type": task.task_type,
                    "description": task.description,
                    "status": task.status.value,
                    "result": task_response.data,
                    "evaluation_score": evaluation.get("quality_score", 0)
                })
        
        return ConversationResponse(
            message=response.message,
            tasks_created=created_tasks,
            persona=request.persona,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in conversation: {str(e)}")

@app.post("/tasks", response_model=TaskResponse)
def create_task(request: TaskRequest):
    """Create and execute a task directly"""
    global tasks_processed
    
    # Convert priority string to enum
    priority_map = {
        "low": TaskPriority.LOW,
        "medium": TaskPriority.MEDIUM,
        "high": TaskPriority.HIGH,
        "urgent": TaskPriority.URGENT
    }
    
    task = Task(
        id=str(uuid.uuid4()),
        description=request.description,
        task_type=request.task_type,
        payload=request.payload,
        priority=priority_map.get(request.priority, TaskPriority.MEDIUM),
        created_by="api_user"
    )
    
    # Store task
    task_store[task.id] = task
    
    # Execute task through supervisor
    try:
        response = supervisor.execute_task(task)
        tasks_processed += 1
        
        # Evaluate with reflection agent
        evaluation = reflection_agent.evaluate_task_completion(task, response)
        
        return TaskResponse(
            task_id=task.id,
            status=task.status.value,
            result=response.data,
            message=response.message
        )
        
    except Exception as e:
        task.status = TaskStatus.FAILED
        task.error_message = str(e)
        raise HTTPException(status_code=500, detail=f"Error executing task: {str(e)}")

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    """Get status and result of a specific task"""
    if task_id not in task_store:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = task_store[task_id]
    
    return TaskResponse(
        task_id=task.id,
        status=task.status.value,
        result=task.result,
        message=task.error_message or "Task completed successfully"
    )

@app.get("/tasks", response_model=List[TaskResponse])
def get_all_tasks():
    """Get all tasks and their statuses"""
    task_list = []
    
    for task in task_store.values():
        task_list.append(TaskResponse(
            task_id=task.id,
            status=task.status.value,
            result=task.result,
            message=task.description
        ))
    
    return task_list

@app.get("/conversation/{persona}")
def get_conversation_history(persona: str):
    """Get conversation history for a specific persona"""
    session_id = f"{persona}_session"
    
    if session_id not in conversation_history:
        return {"persona": persona, "history": []}
    
    return {
        "persona": persona,
        "history": conversation_history[session_id]
    }

@app.get("/system/status", response_model=SystemStatus)
def get_system_status():
    """Get overall system status and health"""
    platform_status = supervisor.get_platform_status()
    
    return SystemStatus(
        active_personas=list(personas.keys()),
        platform_status=platform_status,
        total_tasks_processed=tasks_processed,
        system_health="healthy" if all(platform_status.values()) else "degraded"
    )

@app.get("/system/evaluation")
def get_evaluation_summary():
    """Get evaluation summary from reflection agent"""
    return reflection_agent.get_evaluation_summary()

@app.post("/workflow")
def execute_workflow(workflow_request: Dict[str, Any]):
    """Execute a workflow with multiple tasks"""
    tasks_data = workflow_request.get("tasks", [])
    execution_mode = workflow_request.get("mode", "serial")
    
    # Create task objects
    tasks = []
    for task_data in tasks_data:
        task = Task(
            id=str(uuid.uuid4()),
            description=task_data["description"],
            task_type=task_data["task_type"],
            payload=task_data.get("payload", {}),
            created_by="workflow_api"
        )
        tasks.append(task)
        task_store[task.id] = task
    
    # Execute workflow
    try:
        responses = supervisor.orchestrate_workflow(tasks, execution_mode)
        
        workflow_result = {
            "workflow_id": str(uuid.uuid4()),
            "execution_mode": execution_mode,
            "total_tasks": len(tasks),
            "completed_tasks": len([r for r in responses if r.success]),
            "failed_tasks": len([r for r in responses if not r.success]),
            "results": [
                {
                    "task_id": task.id,
                    "success": response.success,
                    "message": response.message,
                    "data": response.data
                }
                for task, response in zip(tasks, responses)
            ]
        }
        
        return workflow_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution error: {str(e)}")

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)