import { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Copy, Check } from 'lucide-react';
import { api } from '../services/api';
import SourceSection from './SourceSection';

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      role: 'ai',
      content: 'Hello! I have analyzed the video. What would you like to know about it?',
      sources: null
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const result = await api.chat(userMessage);
      setMessages(prev => [
        ...prev,
        {
          role: 'ai',
          content: result.answer,
          sources: result.sources
        }
      ]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          role: 'ai',
          content: 'Sorry, I encountered an error while trying to answer your question.',
          isError: true
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = (content, index) => {
    navigator.clipboard.writeText(content);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] w-full max-w-4xl mx-auto bg-surface rounded-2xl shadow-2xl border border-slate-700/50 overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-slate-700/50 bg-slate-800/50 flex items-center gap-3">
        <Bot className="w-6 h-6 text-primary" />
        <h2 className="font-semibold text-white">Video Assistant</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-primary' : 'bg-slate-700'}`}>
              {msg.role === 'user' ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-white" />}
            </div>
            
            <div className={`flex flex-col max-w-[80%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div className="group relative">
                <div className={`px-5 py-3 rounded-2xl ${
                  msg.role === 'user' 
                    ? 'bg-primary text-white rounded-tr-sm' 
                    : msg.isError 
                      ? 'bg-red-500/10 text-red-400 border border-red-500/20 rounded-tl-sm'
                      : 'bg-slate-800 text-slate-100 rounded-tl-sm'
                }`}>
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                </div>
                
                {msg.role === 'ai' && !msg.isError && (
                  <button 
                    onClick={() => handleCopy(msg.content, idx)}
                    className="absolute -right-10 top-2 p-1.5 text-slate-400 hover:text-white bg-slate-800 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
                    title="Copy response"
                  >
                    {copiedIndex === idx ? <Check className="w-4 h-4 text-green-400" /> : <Copy className="w-4 h-4" />}
                  </button>
                )}
              </div>
              
              {msg.sources && <SourceSection sources={msg.sources} />}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex gap-4">
            <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center shrink-0">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="bg-slate-800 px-5 py-4 rounded-2xl rounded-tl-sm flex gap-2 items-center">
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]"></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]"></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-4 bg-slate-800/50 border-t border-slate-700/50">
        <form onSubmit={handleSubmit} className="relative flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about the video..."
            className="w-full bg-slate-900 border border-slate-700 text-white rounded-xl pl-4 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="absolute right-2 p-2 bg-primary hover:bg-blue-600 disabled:bg-slate-700 disabled:text-slate-400 text-white rounded-lg transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
