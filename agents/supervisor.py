"""
Hierarchical supervisor agent that routes tasks to platform supervisors.
"""
import uuid
from typing import Dict, List, Any, Optional
from agents.base import SupervisorAgent, Task, AgentResponse, TaskStatus, PlatformAgent

class HierarchicalSupervisor(SupervisorAgent):
    """
    Main supervisor agent that receives requests from persona agents
    and routes them to appropriate platform supervisors.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="hierarchical_supervisor",
            name="Hierarchical Supervisor",
            description="Routes tasks to appropriate platform supervisors and orchestrates workflows"
        )
        self.platform_agents: Dict[str, PlatformAgent] = {}
        self.task_history: List[Task] = []
        
    def register_platform_agent(self, platform_name: str, agent: PlatformAgent):
        """Register a platform-specific supervisor agent"""
        self.platform_agents[platform_name] = agent
        self.add_sub_agent(agent)
        
    def can_handle(self, task: Task) -> bool:
        """Can handle any task by routing to appropriate platform agent"""
        return True
    
    def execute_task(self, task: Task) -> AgentResponse:
        """Route task to appropriate platform agent"""
        self.task_history.append(task)
        
        # Determine which platform should handle this task
        platform_name = self._determine_platform(task)
        
        if platform_name and platform_name in self.platform_agents:
            platform_agent = self.platform_agents[platform_name]
            
            # Check if platform agent can handle the task
            if platform_agent.can_handle(task):
                task.assigned_agent = platform_agent.agent_id
                task.status = TaskStatus.IN_PROGRESS
                return platform_agent.execute_task(task)
            else:
                return AgentResponse(
                    success=False,
                    message=f"Platform agent {platform_name} cannot handle task type: {task.task_type}",
                    requires_clarification=True,
                    clarification_question=f"Could you specify more details about what you want to do with {platform_name}?"
                )
        else:
            return AgentResponse(
                success=False,
                message=f"No platform agent found for task type: {task.task_type}",
                requires_clarification=True,
                clarification_question="Could you specify which platform or service you want to use?"
            )
    
    def _determine_platform(self, task: Task) -> Optional[str]:
        """Determine which platform should handle this task based on task type"""
        platform_mappings = {
            # GitHub-related tasks
            'github_create_issue': 'github',
            'github_create_pr': 'github',
            'github_list_repos': 'github',
            'github_update_repo': 'github',
            'code_review': 'github',
            'repository_management': 'github',
            
            # Email-related tasks
            'send_email': 'gmail',
            'check_email': 'gmail',
            'schedule_email': 'gmail',
            'email_followup': 'gmail',
            
            # Jira-related tasks
            'create_ticket': 'jira',
            'update_ticket': 'jira',
            'assign_ticket': 'jira',
            'track_progress': 'jira',
            'project_management': 'jira',
            
            # Calendar-related tasks
            'schedule_meeting': 'calendar',
            'check_availability': 'calendar',
            'send_invite': 'calendar',
            'reschedule_meeting': 'calendar',
        }
        
        return platform_mappings.get(task.task_type)
    
    def orchestrate_workflow(self, tasks: List[Task], execution_mode: str = "serial") -> List[AgentResponse]:
        """
        Orchestrate multiple tasks in serial or parallel mode
        """
        responses = []
        
        if execution_mode == "serial":
            # Execute tasks one by one
            for task in tasks:
                response = self.execute_task(task)
                responses.append(response)
                
                # Stop if any task fails (unless it just needs clarification)
                if not response.success and not response.requires_clarification:
                    break
                    
        elif execution_mode == "parallel":
            # Execute all tasks simultaneously (simplified implementation)
            for task in tasks:
                response = self.execute_task(task)
                responses.append(response)
        
        return responses
    
    def create_subtasks(self, main_task: Task, subtask_descriptions: List[Dict[str, Any]]) -> List[Task]:
        """Create subtasks from a main task"""
        subtasks = []
        
        for subtask_desc in subtask_descriptions:
            subtask = Task(
                id=str(uuid.uuid4()),
                description=subtask_desc['description'],
                task_type=subtask_desc['task_type'],
                payload=subtask_desc.get('payload', {}),
                parent_task_id=main_task.id,
                created_by=self.agent_id
            )
            subtasks.append(subtask)
            
        return subtasks
    
    def get_task_history(self) -> List[Task]:
        """Get history of all tasks processed"""
        return self.task_history.copy()
    
    def get_platform_status(self) -> Dict[str, bool]:
        """Get status of all registered platform agents"""
        status = {}
        for platform_name, agent in self.platform_agents.items():
            try:
                status[platform_name] = agent.test_connection()
            except Exception:
                status[platform_name] = False
        return status