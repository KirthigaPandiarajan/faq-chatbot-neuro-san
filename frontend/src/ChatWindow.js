import React, { useState, useEffect } from 'react';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState('');

  useEffect(() => {
    // Generate unique session ID on component mount
    const id = `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(id);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: 'user', text: input }]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          session_id: sessionId,
          message: input 
        })
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error('API Error:', errorData);
        setMessages(prev => [
          ...prev,
          { role: 'bot', text: `Error: ${errorData.detail || 'Unknown error'}` }
        ]);
        return;
      }

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { role: 'bot', text: data.reply }
      ]);

    } catch (err) {
      console.error('Fetch error:', err);
      setMessages(prev => [
        ...prev,
        { role: 'bot', text: `Error: ${err.message || "Backend not reachable."}` }
      ]);
    }

    setInput('');
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h2>FAQ Chatbot</h2>
      <div style={{ 
        border: '1px solid #ccc', 
        height: '400px', 
        overflowY: 'auto', 
        marginBottom: '10px',
        padding: '10px',
        backgroundColor: '#f9f9f9'
      }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: '10px' }}>
            <b style={{ color: m.role === 'user' ? 'blue' : 'green' }}>
              {m.role.toUpperCase()}:
            </b>
            <p style={{ margin: '5px 0' }}>{m.text}</p>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: '10px' }}>
        <input 
          value={input} 
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && sendMessage()}
          placeholder="Ask a question..."
          style={{ flex: 1, padding: '10px' }}
        />
        <button 
          onClick={sendMessage}
          style={{ padding: '10px 20px', cursor: 'pointer' }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
