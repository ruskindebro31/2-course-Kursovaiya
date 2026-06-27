import { useEffect, useState } from 'react';
import { getWsBase } from '../utils/apiConfig';

export default function useNotifications(userId) {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    if (!userId) return undefined;
    const ws = new WebSocket(`${getWsBase()}/ws/notifications/${userId}/`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setNotifications((prev) => [...prev, data.message]);
    };
    return () => ws.close();
  }, [userId]);

  return notifications;
}
