"""
Reflection agent that evaluates task completion and triggers follow-up actions.
"""
from typing import Dict, List, Any, Optional
from agents.base import BaseAgent, Task, AgentResponse, TaskStatus
import uuid

class ReflectionAgent(BaseAgent):
    """
    Agent that evaluates task completion, identifies issues, and can trigger follow-up actions.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="reflection_agent",
            name="Reflection Agent",
            description="Evaluates task completion and ensures quality outcomes"
        )
        self.evaluation_history: List[Dict[str, Any]] = []
    
    def can_handle(self, task: Task) -> bool:
        """Can handle reflection and evaluation tasks"""
        return task.task_type in ["evaluate_completion", "quality_check", "follow_up_analysis"]
    
    def execute_task(self, task: Task) -> AgentResponse:
        """Execute reflection and evaluation tasks"""
        if task.task_type == "evaluate_completion":
            return self._evaluate_completion(task)
        elif task.task_type == "quality_check":
            return self._quality_check(task)
        elif task.task_type == "follow_up_analysis":
            return self._follow_up_analysis(task)
        else:
            return AgentResponse(
                success=False,
                message=f"Unsupported reflection task type: {task.task_type}"
            )
    
    def evaluate_task_completion(self, task: Task, response: AgentResponse) -> Dict[str, Any]:
        """
        Evaluate if a task was completed successfully and suggest improvements
        """
        evaluation = {
            "task_id": task.id,
            "task_type": task.task_type,
            "success": response.success,
            "completeness_score": 0,
            "quality_score": 0,
            "issues_identified": [],
            "recommendations": [],
            "follow_up_needed": False,
            "follow_up_tasks": []
        }
        
        # Evaluate completeness
        if response.success:
            evaluation["completeness_score"] = 90
            if response.data and len(response.data) > 0:
                evaluation["completeness_score"] = 100
        else:
            evaluation["completeness_score"] = 20
            evaluation["issues_identified"].append("Task execution failed")
        
        # Evaluate quality based on response content
        if response.message and len(response.message) > 10:
            evaluation["quality_score"] += 40
        if response.data:
            evaluation["quality_score"] += 40
        if not response.requires_clarification:
            evaluation["quality_score"] += 20
        
        # Check for common issues and make recommendations
        if response.requires_clarification:
            evaluation["issues_identified"].append("Requires user clarification")
            evaluation["recommendations"].append("Provide more specific instructions to avoid ambiguity")
        
        if task.task_type == "github_create_issue" and response.success:
            # Check if GitHub issue creation was properly documented
            if response.data and "issue_id" in response.data:
                evaluation["recommendations"].append("Consider sending confirmation email about the created issue")
                evaluation["follow_up_needed"] = True
                evaluation["follow_up_tasks"].append({
                    "type": "send_email",
                    "description": "Send confirmation email about GitHub issue creation",
                    "priority": "low"
                })
        
        if task.task_type == "send_email" and response.success:
            # Suggest follow-up tracking
            evaluation["recommendations"].append("Consider setting up delivery confirmation tracking")
        
        # Store evaluation
        self.evaluation_history.append(evaluation)
        
        return evaluation
    
    def _evaluate_completion(self, task: Task) -> AgentResponse:
        """Evaluate completion of a given task"""
        target_task_data = task.payload.get("target_task")
        target_response_data = task.payload.get("target_response")
        
        if not target_task_data or not target_response_data:
            return AgentResponse(
                success=False,
                message="Missing target task or response data for evaluation"
            )
        
        # Reconstruct task and response objects for evaluation
        target_task = Task(**target_task_data)
        target_response = AgentResponse(**target_response_data)
        
        evaluation = self.evaluate_task_completion(target_task, target_response)
        
        return AgentResponse(
            success=True,
            message=f"Evaluation completed. Quality score: {evaluation['quality_score']}/100",
            data=evaluation
        )
    
    def _quality_check(self, task: Task) -> AgentResponse:
        """Perform quality check on system performance"""
        check_results = {
            "overall_quality": 85,
            "areas_checked": [
                "Task completion rate",
                "Response quality",
                "User satisfaction indicators"
            ],
            "recommendations": [
                "Continue monitoring task completion patterns",
                "Consider adding more detailed error handling"
            ]
        }
        
        return AgentResponse(
            success=True,
            message="Quality check completed successfully",
            data=check_results
        )
    
    def _follow_up_analysis(self, task: Task) -> AgentResponse:
        """Analyze if follow-up actions are needed"""
        analysis_results = {
            "follow_ups_needed": 2,
            "high_priority_follow_ups": 0,
            "suggested_actions": [
                "Send confirmation emails for completed tasks",
                "Schedule check-in meetings for ongoing projects"
            ]
        }
        
        return AgentResponse(
            success=True,
            message="Follow-up analysis completed",
            data=analysis_results
        )
    
    def identify_improvement_opportunities(self, task_history: List[Task]) -> List[Dict[str, Any]]:
        """
        Analyze task history to identify improvement opportunities
        """
        opportunities = []
        
        if not task_history:
            return opportunities
        
        # Analyze task completion patterns
        failed_tasks = [t for t in task_history if t.status == TaskStatus.FAILED]
        if len(failed_tasks) > len(task_history) * 0.1:  # More than 10% failure rate
            opportunities.append({
                "type": "high_failure_rate",
                "description": "High task failure rate detected",
                "recommendation": "Review and improve error handling mechanisms",
                "priority": "high"
            })
        
        # Check for common task types that might need optimization
        task_types = {}
        for task in task_history:
            task_types[task.task_type] = task_types.get(task.task_type, 0) + 1
        
        most_common_type = max(task_types.items(), key=lambda x: x[1]) if task_types else None
        if most_common_type and most_common_type[1] > 5:
            opportunities.append({
                "type": "workflow_optimization",
                "description": f"High frequency of {most_common_type[0]} tasks",
                "recommendation": f"Consider creating templates or automation for {most_common_type[0]} tasks",
                "priority": "medium"
            })
        
        return opportunities
    
    def generate_follow_up_tasks(self, completed_task: Task, response: AgentResponse) -> List[Task]:
        """
        Generate follow-up tasks based on completed task analysis
        """
        follow_up_tasks = []
        
        # Generate follow-ups based on task type
        if completed_task.task_type == "github_create_issue" and response.success:
            # Follow up with email confirmation
            follow_up_tasks.append(Task(
                id=str(uuid.uuid4()),
                description="Send confirmation email about GitHub issue creation",
                task_type="send_email",
                payload={
                    "subject": "GitHub Issue Created Successfully",
                    "template": "github_issue_confirmation",
                    "issue_data": response.data
                },
                parent_task_id=completed_task.id,
                created_by=self.agent_id
            ))
        
        elif completed_task.task_type == "send_email" and response.success:
            # Follow up with delivery tracking
            follow_up_tasks.append(Task(
                id=str(uuid.uuid4()),
                description="Track email delivery status",
                task_type="email_followup",
                payload={
                    "email_id": response.data.get("email_id") if response.data else None,
                    "tracking_type": "delivery_confirmation"
                },
                parent_task_id=completed_task.id,
                created_by=self.agent_id
            ))
        
        elif completed_task.task_type == "schedule_meeting" and response.success:
            # Follow up with meeting reminder
            follow_up_tasks.append(Task(
                id=str(uuid.uuid4()),
                description="Send meeting reminder",
                task_type="send_email",
                payload={
                    "subject": "Meeting Reminder",
                    "template": "meeting_reminder",
                    "meeting_data": response.data
                },
                parent_task_id=completed_task.id,
                created_by=self.agent_id
            ))
        
        return follow_up_tasks
    
    def get_evaluation_summary(self) -> Dict[str, Any]:
        """Get summary of all evaluations performed"""
        if not self.evaluation_history:
            return {"total_evaluations": 0, "average_quality": 0, "success_rate": 0}
        
        total_evaluations = len(self.evaluation_history)
        total_quality = sum(eval["quality_score"] for eval in self.evaluation_history)
        successful_tasks = sum(1 for eval in self.evaluation_history if eval["success"])
        
        return {
            "total_evaluations": total_evaluations,
            "average_quality": total_quality / total_evaluations,
            "success_rate": (successful_tasks / total_evaluations) * 100,
            "common_issues": self._get_common_issues(),
            "top_recommendations": self._get_top_recommendations()
        }
    
    def _get_common_issues(self) -> List[str]:
        """Get most common issues from evaluations"""
        issue_counts = {}
        for eval in self.evaluation_history:
            for issue in eval["issues_identified"]:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        return sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _get_top_recommendations(self) -> List[str]:
        """Get most common recommendations from evaluations"""
        rec_counts = {}
        for eval in self.evaluation_history:
            for rec in eval["recommendations"]:
                rec_counts[rec] = rec_counts.get(rec, 0) + 1
        
        return sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)[:5]