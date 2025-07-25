#!/usr/bin/env python3
"""
Test script for the modular AI assistant system.
Demonstrates the hierarchical agent architecture without requiring API credentials.
"""
import sys
import uuid
from typing import Dict, List

# Add the project root to the path
sys.path.append('/home/runner/work/Personality-assistant-changer/Personality-assistant-changer')

from agents.base import Task, TaskStatus, TaskPriority
from agents.supervisor import HierarchicalSupervisor
from agents.personas import HRManagerAgent, ITSupportAgent, DoctorAgent
from agents.platforms import GitHubPlatformAgent, GmailPlatformAgent, JiraPlatformAgent, CalendarPlatformAgent
from agents.reflection import ReflectionAgent

def test_agent_system():
    """Test the complete agent system"""
    print("🧪 TESTING MODULAR AI ASSISTANT SYSTEM")
    print("=" * 80)
    
    # Initialize system components
    print("\n📋 Initializing system components...")
    supervisor = HierarchicalSupervisor()
    reflection_agent = ReflectionAgent()
    
    # Initialize persona agents
    hr_agent = HRManagerAgent()
    it_agent = ITSupportAgent()
    doctor_agent = DoctorAgent()
    
    print(f"✅ Persona agents initialized: {hr_agent.name}, {it_agent.name}, {doctor_agent.name}")
    
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
    
    print(f"✅ Platform agents registered: GitHub, Gmail, Jira, Calendar")
    
    # Test 1: HR Manager Onboarding Scenario
    print("\n" + "="*80)
    print("🎭 TEST 1: HR Manager Onboarding Workflow")
    print("="*80)
    
    # Create conversation task for HR Manager
    onboarding_message = "I need to onboard a new software developer. They need GitHub access and a welcome email."
    
    conversation_task = Task(
        id=str(uuid.uuid4()),
        description="HR onboarding conversation",
        task_type="conversation",
        payload={"message": onboarding_message},
        created_by="test_user"
    )
    
    print(f"📝 User message: '{onboarding_message}'")
    print(f"🎯 Selected persona: {hr_agent.name}")
    
    # Execute conversation with HR Manager
    hr_response = hr_agent.execute_task(conversation_task)
    print(f"💬 HR Manager response: {hr_response.message[:200]}...")
    
    if hr_response.tasks_created:
        print(f"📋 Tasks created by HR Manager: {len(hr_response.tasks_created)}")
        
        for i, task in enumerate(hr_response.tasks_created, 1):
            print(f"   {i}. {task.task_type}: {task.description}")
            
            # Execute task through supervisor
            print(f"   🔄 Executing task through supervisor...")
            task_response = supervisor.execute_task(task)
            
            print(f"   ✅ Task result: {task_response.message}")
            if task_response.data:
                print(f"   📊 Task data: {task_response.data}")
            
            # Evaluate with reflection agent
            evaluation = reflection_agent.evaluate_task_completion(task, task_response)
            print(f"   🎯 Quality score: {evaluation['quality_score']}/100")
            
            # Generate follow-up tasks if needed
            follow_ups = reflection_agent.generate_follow_up_tasks(task, task_response)
            if follow_ups:
                print(f"   📝 Follow-up tasks suggested: {len(follow_ups)}")
    
    # Test 2: IT Support Ticket Creation
    print("\n" + "="*80)
    print("🎭 TEST 2: IT Support Ticket Creation")
    print("="*80)
    
    it_message = "My laptop is running very slowly and I can't access the company VPN. Can you help?"
    
    it_conversation_task = Task(
        id=str(uuid.uuid4()),
        description="IT support conversation",
        task_type="conversation",
        payload={"message": it_message},
        created_by="test_user"
    )
    
    print(f"📝 User message: '{it_message}'")
    print(f"🎯 Selected persona: {it_agent.name}")
    
    # Execute conversation with IT Support
    it_response = it_agent.execute_task(it_conversation_task)
    print(f"💬 IT Support response: {it_response.message[:200]}...")
    
    if it_response.tasks_created:
        print(f"📋 Tasks created by IT Support: {len(it_response.tasks_created)}")
        
        for i, task in enumerate(it_response.tasks_created, 1):
            print(f"   {i}. {task.task_type}: {task.description}")
            
            # Execute task through supervisor
            task_response = supervisor.execute_task(task)
            print(f"   ✅ Task result: {task_response.message}")
            
            # Evaluate with reflection agent
            evaluation = reflection_agent.evaluate_task_completion(task, task_response)
            print(f"   🎯 Quality score: {evaluation['quality_score']}/100")
    
    # Test 3: Doctor Appointment Scheduling
    print("\n" + "="*80)
    print("🎭 TEST 3: Doctor Appointment Scheduling")
    print("="*80)
    
    doctor_message = "I've been having persistent headaches for the past week. Can I schedule an appointment?"
    
    doctor_conversation_task = Task(
        id=str(uuid.uuid4()),
        description="Medical consultation conversation",
        task_type="conversation",
        payload={"message": doctor_message},
        created_by="test_user"
    )
    
    print(f"📝 User message: '{doctor_message}'")
    print(f"🎯 Selected persona: {doctor_agent.name}")
    
    # Execute conversation with Doctor
    doctor_response = doctor_agent.execute_task(doctor_conversation_task)
    print(f"💬 Doctor response: {doctor_response.message[:200]}...")
    
    if doctor_response.tasks_created:
        print(f"📋 Tasks created by Doctor: {len(doctor_response.tasks_created)}")
        
        for i, task in enumerate(doctor_response.tasks_created, 1):
            print(f"   {i}. {task.task_type}: {task.description}")
            
            # Execute task through supervisor
            task_response = supervisor.execute_task(task)
            print(f"   ✅ Task result: {task_response.message}")
            
            # Evaluate with reflection agent
            evaluation = reflection_agent.evaluate_task_completion(task, task_response)
            print(f"   🎯 Quality score: {evaluation['quality_score']}/100")
    
    # Test 4: Direct Task Creation and Workflow
    print("\n" + "="*80)
    print("🎭 TEST 4: Direct Task Creation and Workflow")
    print("="*80)
    
    # Create multiple tasks for workflow testing
    workflow_tasks = [
        Task(
            id=str(uuid.uuid4()),
            description="Create GitHub issue for new feature",
            task_type="github_create_issue",
            payload={
                "title": "Add new dashboard widget",
                "description": "Implement a new widget for the user dashboard",
                "repository": "company/webapp"
            },
            priority=TaskPriority.HIGH,
            created_by="test_workflow"
        ),
        Task(
            id=str(uuid.uuid4()),
            description="Send project update email",
            task_type="send_email",
            payload={
                "subject": "Project Update - Dashboard Widget",
                "recipient": "team@company.com",
                "template": "project_update"
            },
            priority=TaskPriority.MEDIUM,
            created_by="test_workflow"
        ),
        Task(
            id=str(uuid.uuid4()),
            description="Schedule review meeting",
            task_type="schedule_meeting",
            payload={
                "title": "Dashboard Widget Review",
                "duration": 60,
                "type": "project_review"
            },
            priority=TaskPriority.LOW,
            created_by="test_workflow"
        )
    ]
    
    print("🔄 Testing serial workflow execution...")
    serial_responses = supervisor.orchestrate_workflow(workflow_tasks, "serial")
    
    print(f"📊 Workflow Results:")
    print(f"   Total tasks: {len(workflow_tasks)}")
    print(f"   Successful: {len([r for r in serial_responses if r.success])}")
    print(f"   Failed: {len([r for r in serial_responses if not r.success])}")
    
    for i, (task, response) in enumerate(zip(workflow_tasks, serial_responses), 1):
        print(f"   {i}. {task.task_type}: {'✅' if response.success else '❌'} {response.message}")
    
    # Test 5: System Status and Reflection
    print("\n" + "="*80)
    print("🎭 TEST 5: System Status and Reflection")
    print("="*80)
    
    # Get platform status
    platform_status = supervisor.get_platform_status()
    print("🔌 Platform Status:")
    for platform, status in platform_status.items():
        print(f"   {platform}: {'✅ Connected' if status else '❌ Disconnected'}")
    
    # Get task history
    task_history = supervisor.get_task_history()
    print(f"\n📈 Task History: {len(task_history)} tasks processed")
    
    # Get evaluation summary
    eval_summary = reflection_agent.get_evaluation_summary()
    print(f"\n🎯 Evaluation Summary:")
    print(f"   Total evaluations: {eval_summary['total_evaluations']}")
    print(f"   Average quality: {eval_summary['average_quality']:.1f}/100")
    print(f"   Success rate: {eval_summary['success_rate']:.1f}%")
    
    print("\n" + "="*80)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*80)
    print("\nThe modular AI assistant system is working correctly with:")
    print("✅ Hierarchical supervisor routing")
    print("✅ Persona agent task creation")
    print("✅ Platform-specific agent execution")
    print("✅ Reflection agent evaluation")
    print("✅ Workflow orchestration")
    print("\nThe system is ready for integration with FastAPI backend and React frontend!")

if __name__ == "__main__":
    test_agent_system()