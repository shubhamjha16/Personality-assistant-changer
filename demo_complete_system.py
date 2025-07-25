#!/usr/bin/env python3
"""
Comprehensive demonstration of the Modular AI Assistant System.
Shows real-world usage scenarios with all components working together.
"""
import requests
import json
import time
import sys
import subprocess
import os
from typing import Dict, Any

API_BASE = "http://localhost:8000"

def check_api_available():
    """Check if the FastAPI backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def start_backend_if_needed():
    """Start the backend if it's not running"""
    if check_api_available():
        print("✅ Backend is already running")
        return None
    
    print("🚀 Starting FastAPI backend...")
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    backend_process = subprocess.Popen(
        ["python", "main.py"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for backend to start
    for i in range(10):
        time.sleep(2)
        if check_api_available():
            print("✅ Backend started successfully")
            return backend_process
        print(f"⏳ Waiting for backend to start... ({i+1}/10)")
    
    print("❌ Failed to start backend")
    backend_process.terminate()
    return None

def make_api_call(method: str, endpoint: str, data: Dict[Any, Any] = None):
    """Make an API call and return the response"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*80}")
    print(f"🎯 {title}")
    print('='*80)

def print_response(response: Dict[Any, Any], description: str = ""):
    """Print a formatted API response"""
    if description:
        print(f"📋 {description}")
    print(f"📊 Response: {json.dumps(response, indent=2)}")

def demonstrate_system():
    """Demonstrate the complete system functionality"""
    print("🤖 MODULAR AI ASSISTANT SYSTEM DEMONSTRATION")
    print("=" * 80)
    print("This demo shows the complete workflow from persona selection to task execution")
    print()
    
    # Start backend if needed
    backend_process = start_backend_if_needed()
    
    if not check_api_available():
        print("❌ Cannot connect to backend API. Exiting.")
        return
    
    try:
        # 1. System Health Check
        print_section("System Health Check")
        status = make_api_call("GET", "/system/status")
        print_response(status, "System Status")
        
        # 2. Available Personas
        print_section("Available Personas")
        personas = make_api_call("GET", "/personas")
        print_response(personas, "Available AI Personas")
        
        # 3. HR Manager Onboarding Scenario
        print_section("HR Manager Onboarding Scenario")
        print("🎭 Scenario: New employee onboarding with GitHub access and welcome email")
        
        hr_conversation = make_api_call("POST", "/conversation", {
            "persona": "hr_manager",
            "message": "I need to onboard a new software developer named Alice Johnson. She needs GitHub access to our repositories and should receive a welcome email with onboarding instructions."
        })
        print_response(hr_conversation, "HR Manager Response & Task Creation")
        
        # 4. IT Support Ticket Creation
        print_section("IT Support Ticket Creation")
        print("🎭 Scenario: Employee reporting technical issues")
        
        it_conversation = make_api_call("POST", "/conversation", {
            "persona": "it_support", 
            "message": "My laptop has been running very slowly for the past few days, and I can't connect to our company VPN. The WiFi keeps disconnecting too. Can you help me resolve these issues?"
        })
        print_response(it_conversation, "IT Support Response & Ticket Creation")
        
        # 5. Doctor Consultation Scheduling
        print_section("Medical Consultation Scheduling")
        print("🎭 Scenario: Patient requesting medical appointment")
        
        doctor_conversation = make_api_call("POST", "/conversation", {
            "persona": "doctor",
            "message": "I've been experiencing persistent headaches for about two weeks now, especially in the mornings. They're getting worse and I'm concerned. Can I schedule an appointment to discuss this?"
        })
        print_response(doctor_conversation, "Doctor Response & Appointment Scheduling")
        
        # 6. Direct Task Execution
        print_section("Direct Task Execution")
        print("🎯 Demonstrating direct task creation without persona conversation")
        
        github_task = make_api_call("POST", "/tasks", {
            "description": "Create GitHub issue for new dashboard feature",
            "task_type": "github_create_issue",
            "payload": {
                "title": "Add Real-time Analytics Dashboard",
                "description": "Implement a new analytics dashboard with real-time data visualization for user metrics and system performance.",
                "repository": "company/webapp"
            },
            "priority": "high"
        })
        print_response(github_task, "GitHub Issue Creation Task")
        
        # 7. Workflow Orchestration
        print_section("Workflow Orchestration")
        print("🔄 Demonstrating multi-step workflow execution")
        
        workflow = make_api_call("POST", "/workflow", {
            "mode": "serial",
            "tasks": [
                {
                    "description": "Create project kickoff GitHub issue",
                    "task_type": "github_create_issue",
                    "payload": {
                        "title": "Project Kickoff: Q1 2024 Features",
                        "description": "Track progress for Q1 2024 feature development",
                        "repository": "company/projects"
                    }
                },
                {
                    "description": "Send project announcement email",
                    "task_type": "send_email",
                    "payload": {
                        "subject": "Q1 2024 Project Kickoff",
                        "recipient": "dev-team@company.com",
                        "template": "project_announcement"
                    }
                },
                {
                    "description": "Schedule project planning meeting",
                    "task_type": "schedule_meeting",
                    "payload": {
                        "title": "Q1 2024 Project Planning",
                        "duration": 60,
                        "type": "project_planning"
                    }
                }
            ]
        })
        print_response(workflow, "Multi-step Workflow Execution")
        
        # 8. System Evaluation
        print_section("System Evaluation & Reflection")
        evaluation = make_api_call("GET", "/system/evaluation")
        print_response(evaluation, "Reflection Agent Evaluation Summary")
        
        # 9. Task History
        print_section("Task History")
        tasks = make_api_call("GET", "/tasks")
        print_response(tasks, "All Executed Tasks")
        
        # 10. Final Status Check
        print_section("Final System Status")
        final_status = make_api_call("GET", "/system/status")
        print_response(final_status, "Updated System Status")
        
        print_section("Demo Summary")
        print("🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print()
        print("✅ Key Features Demonstrated:")
        print("   • Multiple AI personas (HR Manager, IT Support, Doctor)")
        print("   • Intelligent task creation from natural language")
        print("   • Hierarchical agent routing and orchestration")
        print("   • Platform-specific task execution (GitHub, Email, Calendar, Jira)")
        print("   • Quality evaluation with reflection agent")
        print("   • Multi-step workflow orchestration")
        print("   • Real-time system monitoring")
        print()
        print("🌐 Web Interface:")
        print("   • Backend API: http://localhost:8000")
        print("   • API Documentation: http://localhost:8000/docs")
        print("   • Frontend (if running): http://localhost:3000")
        print()
        print("💡 Next Steps:")
        print("   • Try the React frontend: cd frontend && npm install && npm start")
        print("   • Add custom personas for your specific use cases")
        print("   • Configure real API tokens for actual platform integration")
        print("   • Extend with new platform agents (Slack, Teams, etc.)")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    
    finally:
        if backend_process:
            print("\n🔄 Cleaning up backend process...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--backend-only":
        # Just start the backend without demo
        backend_process = start_backend_if_needed()
        if backend_process:
            print("🌐 Backend running at http://localhost:8000")
            print("📚 API docs at http://localhost:8000/docs")
            print("Press Ctrl+C to stop")
            try:
                backend_process.wait()
            except KeyboardInterrupt:
                backend_process.terminate()
    else:
        demonstrate_system()