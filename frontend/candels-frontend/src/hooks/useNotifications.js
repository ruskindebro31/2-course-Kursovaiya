import { useEffect, useState } from 'react';

export default function useNotifications() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/notifications/');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotifications(prev => [...prev, data.message]);
    };

    return () => ws.close();
  }, []);

  return notifications;
}
