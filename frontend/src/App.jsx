import React, { useState, useEffect } from 'react';
import { Send, User, Bot, LayoutList, Cpu, Loader2, CheckCircle2, Circle } from 'lucide-react';
import './index.css';

const API_BASE = 'http://localhost:3001/api';

export default function App() {
  const [messages, setMessages] = useState([
    { id: 'init', type: 'agent', content: 'Hello! I am your Agentic AI assistant. How can I help you today?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [plan, setPlan] = useState([]);
  const [toolUsage, setToolUsage] = useState({ tool: 'none', status: 'idle', details: 'Waiting for task...' });

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    const userMessage = inputValue;
    setInputValue('');
    setMessages(prev => [...prev, { id: Date.now(), type: 'user', content: userMessage }]);
    setIsProcessing(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });
      
      const data = await res.json();
      
      setMessages(prev => [...prev, { id: Date.now() + 1, type: 'agent', content: data.message }]);
      if (data.plan) setPlan(data.plan);
      if (data.toolUsage) setToolUsage(data.toolUsage);

      // Simulate background tasks completing
      checkStatus();
      
    } catch (error) {
      console.error('Error sending message:', error);
      setIsProcessing(false);
    }
  };

  const checkStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/status/update`);
      const data = await res.json();
      
      if (data.plan) setPlan(data.plan);
      if (data.toolUsage) setToolUsage(data.toolUsage);
      
      if (data.finalResult) {
        setMessages(prev => [...prev, { id: Date.now() + 2, type: 'agent', content: data.finalResult }]);
      }
      setIsProcessing(false);
    } catch (error) {
      console.error('Error checking status:', error);
      setIsProcessing(false);
    }
  };

  return (
    <div className="app-container">
      {/* Main Content Area */}
      <div className="main-content">
        <div className="glass-panel chat-container">
          <div className="chat-messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.type}`}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', opacity: 0.8, fontSize: '0.85rem' }}>
                  {msg.type === 'user' ? <User size={16} /> : <Bot size={16} />}
                  <span>{msg.type === 'user' ? 'You' : 'Agentic AI'}</span>
                </div>
                <div>{msg.content}</div>
              </div>
            ))}
            {isProcessing && (
              <div className="message agent animate-pulse" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Loader2 size={16} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />
                <span>Thinking...</span>
              </div>
            )}
          </div>
          
          <form className="chat-input-container" onSubmit={handleSendMessage}>
            <input 
              type="text" 
              className="chat-input"
              placeholder="Ask the AI to perform a task..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isProcessing}
            />
            <button type="submit" className="send-button" disabled={!inputValue.trim() || isProcessing}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>

      {/* Side Panel for Agent Features */}
      <div className="side-panel">
        
        {/* Task Planner Widget */}
        <div className="glass-panel task-planner">
          <h3><LayoutList size={20} className="text-accent-primary" /> Task Plan</h3>
          {plan.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', textAlign: 'center', padding: '20px' }}>
              No active tasks
            </div>
          ) : (
            <div className="task-list">
              {plan.map((task) => (
                <div key={task.id} className={`task-item ${task.status}`}>
                  {task.status === 'completed' && <CheckCircle2 size={18} color="var(--success)" />}
                  {task.status === 'in-progress' && <Loader2 size={18} className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} color="var(--accent-primary)" />}
                  {task.status === 'pending' && <Circle size={18} color="var(--text-muted)" />}
                  <span style={{ fontSize: '0.9rem' }}>{task.step}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Agent Status Widget */}
        <div className="glass-panel agent-status">
          <h3><Cpu size={20} /> Agent Status</h3>
          
          <div>
            <div className={`status-badge ${isProcessing ? 'active animate-pulse' : ''}`}>
              {isProcessing ? 'Agent is Active' : 'Agent is Idle'}
            </div>
          </div>
          
          <div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '8px' }}>Current Tool Execution</div>
            <div className="tool-usage">
              <div style={{ marginBottom: '4px' }}><strong>Tool:</strong> {toolUsage.tool}</div>
              <div style={{ marginBottom: '4px' }}><strong>Status:</strong> {toolUsage.status}</div>
              <div>&gt; {toolUsage.details}</div>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
