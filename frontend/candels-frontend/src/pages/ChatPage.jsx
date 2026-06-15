import React, { useEffect, useState } from 'react';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  let ws;

  useEffect(() => {
    ws = new WebSocket('ws://localhost:8000/ws/chat/1/');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, data]);
    };

    return () => ws.close();
  }, []);

  const sendMessage = () => {
    ws.send(JSON.stringify({ message: input }));
    setInput('');
  };

  return (
    <div>
      <h1>Чат</h1>
      <div>
        {messages.map((msg, i) => (
          <div key={i}>{msg.sender}: {msg.text}</div>
        ))}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={sendMessage}>Отправить</button>
    </div>
  );
}
