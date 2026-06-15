import { useEffect, useState } from 'react';

const WS_BASE = import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000';

export default function useNotifications(userId) {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (!userId) return undefined;
    const ws = new WebSocket(`${WS_BASE}/ws/notifications/${userId}/`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotifications((prev) => [...prev, data.message]);
    };
    return () => ws.close();
  }, [userId]);

  return notifications;
}
