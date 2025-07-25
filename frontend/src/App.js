import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [personas, setPersonas] = useState([]);
  const [selectedPersona, setSelectedPersona] = useState(null);
  const [messages, setMessages] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchPersonas();
    fetchSystemStatus();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchPersonas = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/personas`);
      setPersonas(response.data);
    } catch (error) {
      console.error('Error fetching personas:', error);
    }
  };

  const fetchSystemStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/system/status`);
      setSystemStatus(response.data);
    } catch (error) {
      console.error('Error fetching system status:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !selectedPersona || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setLoading(true);

    // Add user message to chat
    const newUserMessage = {
      id: Date.now(),
      text: userMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };
    setMessages(prev => [...prev, newUserMessage]);

    try {
      const response = await axios.post(`${API_BASE_URL}/conversation`, {
        persona: selectedPersona.id,
        message: userMessage
      });

      // Add assistant response to chat
      const assistantMessage = {
        id: Date.now() + 1,
        text: response.data.message,
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        persona: selectedPersona.name
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Add any created tasks
      if (response.data.tasks_created && response.data.tasks_created.length > 0) {
        setTasks(prev => [...prev, ...response.data.tasks_created]);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'assistant',
        timestamp: new Date().toLocaleTimeString(),
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const selectPersona = (persona) => {
    setSelectedPersona(persona);
    setMessages([]);
    setTasks([]);
    
    // Add welcome message
    const welcomeMessage = {
      id: Date.now(),
      text: `Hello! I'm your ${persona.name}. ${persona.description} How can I help you today?`,
      sender: 'assistant',
      timestamp: new Date().toLocaleTimeString(),
      persona: persona.name
    };
    setMessages([welcomeMessage]);
  };

  const getPersonaEmoji = (personaId) => {
    const emojiMap = {
      'hr_manager': '👩‍💼',
      'it_support': '🖥️',
      'doctor': '👩‍⚕️'
    };
    return emojiMap[personaId] || '🤖';
  };

  const getTaskStatusColor = (status) => {
    const colorMap = {
      'completed': '#4caf50',
      'failed': '#f44336',
      'pending': '#ff9800',
      'in_progress': '#2196f3'
    };
    return colorMap[status] || '#666';
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🤖 Modular AI Assistant System</h1>
        <p>Workplace automation with multiple conversational personas and hierarchical agent orchestration</p>
        {systemStatus && (
          <div style={{ marginTop: '10px', fontSize: '14px' }}>
            Status: {systemStatus.system_health} | Tasks Processed: {systemStatus.total_tasks_processed}
          </div>
        )}
      </header>

      <div className="persona-selection">
        <h2>Select Your AI Assistant Persona</h2>
        <div className="persona-grid">
          {personas.map(persona => (
            <div
              key={persona.id}
              className={`persona-card ${selectedPersona?.id === persona.id ? 'selected' : ''}`}
              onClick={() => selectPersona(persona)}
            >
              <div className="persona-name">
                {getPersonaEmoji(persona.id)} {persona.name}
              </div>
              <div className="persona-description">
                {persona.description}
              </div>
            </div>
          ))}
        </div>
      </div>

      {selectedPersona && (
        <div className="chat-interface">
          <div className="chat-section">
            <div className="chat-header">
              {getPersonaEmoji(selectedPersona.id)} Chat with {selectedPersona.name}
            </div>
            <div className="chat-messages">
              {messages.map(message => (
                <div
                  key={message.id}
                  className={`message ${message.sender} ${message.error ? 'error' : ''}`}
                >
                  <div style={{ marginBottom: '5px' }}>
                    {message.text}
                  </div>
                  <div style={{ fontSize: '11px', opacity: 0.7 }}>
                    {message.timestamp}
                    {message.persona && ` • ${message.persona}`}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="loading">
                  <div className="spinner"></div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            <div className="chat-input">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={`Type your message to ${selectedPersona.name}...`}
                disabled={loading}
              />
              <button onClick={sendMessage} disabled={loading || !inputMessage.trim()}>
                Send
              </button>
            </div>
          </div>

          <div className="tasks-section">
            <div className="tasks-header">
              📋 Tasks & Actions
            </div>
            <div className="tasks-list">
              {tasks.length === 0 ? (
                <div style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
                  No tasks created yet. Start a conversation to see automated tasks!
                </div>
              ) : (
                tasks.map(task => (
                  <div key={task.task_id} className={`task-item ${task.status}`}>
                    <div className="task-type">{task.task_type.replace('_', ' ').toUpperCase()}</div>
                    <div className="task-description">{task.description}</div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '10px' }}>
                      <span
                        className="task-status"
                        style={{ backgroundColor: getTaskStatusColor(task.status) }}
                      >
                        {task.status}
                      </span>
                      {task.evaluation_score && (
                        <span style={{ fontSize: '11px', color: '#666' }}>
                          Score: {task.evaluation_score}/100
                        </span>
                      )}
                    </div>
                    {task.result && (
                      <div style={{ marginTop: '10px', fontSize: '11px', color: '#666' }}>
                        <strong>Result:</strong>
                        {task.result.issue_id && ` Issue #${task.result.issue_id}`}
                        {task.result.email_id && ` Email sent to ${task.result.recipient}`}
                        {task.result.ticket_id && ` Ticket ${task.result.ticket_id}`}
                        {task.result.meeting_id && ` Meeting scheduled`}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      {!selectedPersona && (
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <h3>Welcome to the AI Assistant System</h3>
          <p>Please select a persona above to start your conversation and see automated task creation in action!</p>
          
          <div style={{ marginTop: '30px', textAlign: 'left', maxWidth: '600px', margin: '30px auto' }}>
            <h4>Example Workflow:</h4>
            <ol>
              <li><strong>Select HR Manager</strong> and say "I need to onboard a new developer"</li>
              <li>Watch as the AI creates <strong>GitHub access</strong> and <strong>welcome email</strong> tasks</li>
              <li>See the <strong>hierarchical supervisor</strong> route tasks to platform agents</li>
              <li>Monitor <strong>task completion</strong> and <strong>reflection agent</strong> evaluation</li>
            </ol>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;