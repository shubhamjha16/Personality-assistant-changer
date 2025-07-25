#!/bin/bash

# Startup script for the Modular AI Assistant System
echo "🤖 Starting Modular AI Assistant System"
echo "========================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Test the agent system first
echo "🧪 Testing agent system..."
python test_agent_system.py

if [ $? -ne 0 ]; then
    echo "❌ Agent system test failed. Please check the logs."
    exit 1
fi

echo "✅ Agent system test passed!"

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Start FastAPI backend
echo "🚀 Starting FastAPI backend on port 8000..."
if check_port 8000; then
    echo "⚠️  Port 8000 is already in use. Killing existing process..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

cd backend
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend API
echo "🔍 Testing backend API..."
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend API is running!"
else
    echo "❌ Backend API failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Check if Node.js is available for frontend
if command -v npm &> /dev/null; then
    echo "🌐 Starting React frontend..."
    cd frontend
    
    # Install npm dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📦 Installing npm dependencies..."
        npm install
    fi
    
    # Check if port 3000 is in use
    if check_port 3000; then
        echo "⚠️  Port 3000 is already in use. Frontend may conflict."
    fi
    
    # Start React app
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    echo ""
    echo "🎉 System started successfully!"
    echo "================================"
    echo "🔗 Backend API: http://localhost:8000"
    echo "🔗 API Docs: http://localhost:8000/docs"
    echo "🔗 Frontend: http://localhost:3000"
    echo ""
    echo "💡 Example API calls:"
    echo "curl http://localhost:8000/personas"
    echo "curl -X POST http://localhost:8000/conversation -H 'Content-Type: application/json' -d '{\"persona\": \"hr_manager\", \"message\": \"I need to onboard a new developer\"}'"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    # Wait for user interrupt
    trap 'echo "🛑 Stopping services..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit 0' INT
    wait
else
    echo "⚠️  Node.js/npm not found. Skipping frontend startup."
    echo ""
    echo "🎉 Backend started successfully!"
    echo "================================"
    echo "🔗 Backend API: http://localhost:8000"
    echo "🔗 API Docs: http://localhost:8000/docs"
    echo ""
    echo "💡 To start frontend manually:"
    echo "cd frontend && npm install && npm start"
    echo ""
    echo "Press Ctrl+C to stop backend service"
    
    # Wait for user interrupt
    trap 'echo "🛑 Stopping backend..."; kill $BACKEND_PID 2>/dev/null || true; exit 0' INT
    wait $BACKEND_PID
fi