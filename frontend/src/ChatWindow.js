import React, { useState } from 'react';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages(prev => [...prev, { role: 'user', text: input }]);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });

      const data = await res.json();

      setMessages(prev => [
        ...prev,
        { role: 'bot', text: data.reply }
      ]);

    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'bot', text: "Backend not reachable." }
      ]);
    }

    setInput('');
  };

  return (
    <div>
      {messages.map((m, i) => (
        <div key={i}><b>{m.role}:</b> {m.text}</div>
      ))}
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatWindow;
