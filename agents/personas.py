"""
Persona agents that interpret user intent and create actionable tasks.
Extends the existing personality system with task creation capabilities.
"""
import uuid
import re
from typing import Dict, List, Any, Optional
from agents.base import PersonaAgent, Task, AgentResponse, TaskStatus, TaskPriority
# Import AI agent functions with fallback for testing
try:
    from ai_agent import generate_system_prompt, ask_agent
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False
    def generate_system_prompt(personality_type):
        return f"You are a {personality_type} assistant."
    def ask_agent(user_query, personality_type):
        return f"As a {personality_type}, I would help you with: {user_query}"

class HRManagerAgent(PersonaAgent):
    """HR Manager persona that handles onboarding and HR-related tasks"""
    
    def __init__(self):
        super().__init__(
            agent_id="hr_manager",
            name="HR Manager",
            description="Handles employee onboarding, HR processes, and administrative tasks",
            personality_type="hr"
        )
    
    def can_handle(self, task: Task) -> bool:
        """Check if this is an HR-related conversational task"""
        return task.task_type in ["conversation", "hr_consultation", "onboarding"]
    
    def execute_task(self, task: Task) -> AgentResponse:
        """Execute conversational or HR-related tasks"""
        if task.task_type == "conversation":
            response_text = self.generate_response(task.payload.get("message", ""))
            
            # Check if the conversation implies actionable tasks
            tasks_created = self.interpret_user_intent(task.payload.get("message", ""))
            
            return AgentResponse(
                success=True,
                message=response_text,
                tasks_created=tasks_created
            )
        else:
            return AgentResponse(
                success=False,
                message="Task type not supported by HR Manager agent"
            )
    
    def interpret_user_intent(self, user_message: str) -> List[Task]:
        """Interpret user message and create actionable tasks for onboarding scenarios"""
        tasks = []
        
        # Onboarding-related keywords and patterns
        onboarding_patterns = [
            r"onboard|new hire|new employee|joining",
            r"set up|setup|create account|access",
            r"first day|orientation|welcome"
        ]
        
        github_patterns = [
            r"github|repository|repo|code access|development",
            r"create.*issue|ticket|bug report"
        ]
        
        email_patterns = [
            r"email|send.*message|notify|announcement",
            r"welcome.*email|introduction"
        ]
        
        # Check for onboarding requests
        if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in onboarding_patterns):
            
            # Check if GitHub access is needed
            if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in github_patterns):
                tasks.append(Task(
                    id=str(uuid.uuid4()),
                    description="Set up GitHub access for new employee",
                    task_type="github_create_issue",
                    payload={
                        "title": "New Employee GitHub Access Setup",
                        "description": "Create repository access and permissions for new hire",
                        "repository": "company/onboarding"
                    },
                    priority=TaskPriority.HIGH,
                    created_by=self.agent_id
                ))
            
            # Check if welcome email is needed
            if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in email_patterns):
                tasks.append(Task(
                    id=str(uuid.uuid4()),
                    description="Send welcome email to new employee",
                    task_type="send_email",
                    payload={
                        "subject": "Welcome to the Team!",
                        "template": "welcome_new_hire",
                        "recipient_type": "new_employee"
                    },
                    priority=TaskPriority.MEDIUM,
                    created_by=self.agent_id
                ))
        
        return tasks
    
    def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate HR Manager personality response using existing system"""
        try:
            if AI_AVAILABLE:
                return ask_agent(user_query=user_message, personality_type=self.personality_type)
            else:
                return f"Hello! As your HR Manager, I understand you're asking about: '{user_message}'. I can help you with onboarding, employee processes, and administrative tasks. I've analyzed your request and will create appropriate tasks to assist you."
        except Exception as e:
            return f"I'm here to help with HR matters! However, I'm experiencing some technical difficulties: {str(e)}"

class ITSupportAgent(PersonaAgent):
    """IT Support persona that handles technical requests"""
    
    def __init__(self):
        super().__init__(
            agent_id="it_support",
            name="IT Support",
            description="Handles technical issues, software requests, and IT infrastructure",
            personality_type="it support specialist"
        )
    
    def can_handle(self, task: Task) -> bool:
        """Check if this is a technical support task"""
        return task.task_type in ["conversation", "tech_support", "software_request"]
    
    def execute_task(self, task: Task) -> AgentResponse:
        """Execute IT support tasks"""
        if task.task_type == "conversation":
            response_text = self.generate_response(task.payload.get("message", ""))
            tasks_created = self.interpret_user_intent(task.payload.get("message", ""))
            
            return AgentResponse(
                success=True,
                message=response_text,
                tasks_created=tasks_created
            )
        else:
            return AgentResponse(
                success=False,
                message="Task type not supported by IT Support agent"
            )
    
    def interpret_user_intent(self, user_message: str) -> List[Task]:
        """Interpret user message and create IT-related tasks"""
        tasks = []
        
        # IT support patterns
        issue_patterns = [
            r"bug|error|problem|issue|not working|broken",
            r"help|support|assist|fix"
        ]
        
        software_patterns = [
            r"install|software|application|program|tool",
            r"access|permission|login|credential"
        ]
        
        # Check for issue creation requests
        if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in issue_patterns):
            tasks.append(Task(
                id=str(uuid.uuid4()),
                description="Create IT support ticket for reported issue",
                task_type="create_ticket",
                payload={
                    "title": "IT Support Request",
                    "description": user_message,
                    "category": "technical_support",
                    "priority": "medium"
                },
                priority=TaskPriority.MEDIUM,
                created_by=self.agent_id
            ))
        
        # Check for software requests
        if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in software_patterns):
            tasks.append(Task(
                id=str(uuid.uuid4()),
                description="Process software installation request",
                task_type="create_ticket",
                payload={
                    "title": "Software Installation Request",
                    "description": user_message,
                    "category": "software_request",
                    "priority": "low"
                },
                priority=TaskPriority.LOW,
                created_by=self.agent_id
            ))
        
        return tasks
    
    def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate IT Support personality response"""
        try:
            if AI_AVAILABLE:
                return ask_agent(user_query=user_message, personality_type=self.personality_type)
            else:
                return f"Hello! As your IT Support specialist, I can help you with: '{user_message}'. I'll analyze your technical issue and create the appropriate support tickets and tasks to resolve your problem efficiently."
        except Exception as e:
            return f"I'm here to help with your technical issues! However, I'm experiencing some system difficulties: {str(e)}"

class DoctorAgent(PersonaAgent):
    """Doctor persona that handles medical consultations and health-related tasks"""
    
    def __init__(self):
        super().__init__(
            agent_id="doctor",
            name="Doctor",
            description="Provides medical consultations and health guidance",
            personality_type="doctor"
        )
    
    def can_handle(self, task: Task) -> bool:
        """Check if this is a medical consultation task"""
        return task.task_type in ["conversation", "medical_consultation", "health_advice"]
    
    def execute_task(self, task: Task) -> AgentResponse:
        """Execute medical consultation tasks"""
        if task.task_type == "conversation":
            response_text = self.generate_response(task.payload.get("message", ""))
            tasks_created = self.interpret_user_intent(task.payload.get("message", ""))
            
            return AgentResponse(
                success=True,
                message=response_text,
                tasks_created=tasks_created
            )
        else:
            return AgentResponse(
                success=False,
                message="Task type not supported by Doctor agent"
            )
    
    def interpret_user_intent(self, user_message: str) -> List[Task]:
        """Interpret user message and create health-related tasks"""
        tasks = []
        
        # Medical appointment patterns
        appointment_patterns = [
            r"appointment|schedule|book|reserve",
            r"see.*doctor|consultation|checkup"
        ]
        
        followup_patterns = [
            r"follow.*up|followup|reminder|check.*progress",
            r"test.*result|lab.*result|medication.*reminder"
        ]
        
        # Check for appointment scheduling
        if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in appointment_patterns):
            tasks.append(Task(
                id=str(uuid.uuid4()),
                description="Schedule medical appointment",
                task_type="schedule_meeting",
                payload={
                    "title": "Medical Consultation",
                    "type": "medical_appointment",
                    "duration": 30,
                    "description": "Medical consultation based on patient request"
                },
                priority=TaskPriority.MEDIUM,
                created_by=self.agent_id
            ))
        
        # Check for follow-up requirements
        if any(re.search(pattern, user_message, re.IGNORECASE) for pattern in followup_patterns):
            tasks.append(Task(
                id=str(uuid.uuid4()),
                description="Send follow-up email with health information",
                task_type="send_email",
                payload={
                    "subject": "Health Follow-up Information",
                    "template": "medical_followup",
                    "content": "Follow-up information based on consultation"
                },
                priority=TaskPriority.LOW,
                created_by=self.agent_id
            ))
        
        return tasks
    
    def generate_response(self, user_message: str, context: Dict[str, Any] = None) -> str:
        """Generate Doctor personality response"""
        try:
            if AI_AVAILABLE:
                return ask_agent(user_query=user_message, personality_type=self.personality_type)
            else:
                return f"Hello! As your healthcare provider, I'm concerned about: '{user_message}'. I'll help you schedule appropriate consultations and follow-up care. Please remember that this is general guidance and you should consult with a licensed medical professional for proper diagnosis and treatment."
        except Exception as e:
            return f"I'm here to help with your health concerns! However, I'm experiencing some technical difficulties: {str(e)}"