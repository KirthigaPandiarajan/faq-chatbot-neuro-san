import React, { useState } from 'react';

const ChatWindow = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [context, setContext] = useState([]); // Crucial for Multi-turn memory

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMsg = { role: 'user', text: input };
        setMessages(prev => [...prev, userMsg]);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input, context: context }),
            });
            const data = await response.json();

            setMessages(prev => [...prev, { role: 'bot', text: data.reply }]);
            setContext(data.context); // Update state with Neuro-SAN's returned context
        } catch (err) {
            setMessages(prev => [...prev, { role: 'bot', text: "Error connecting to service." }]);
        }
        setInput('');
    };

    return (
        <div className="chat-container">
            <div className="history">
                {messages.map((m, i) => <div key={i} className={m.role}>{m.text}</div>)}
            </div>
            <input value={input} onChange={(e) => setInput(e.target.value)} />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};
export default ChatWindow;