/** Базовый URL API: относительный /api/ — один origin с Django или Vite proxy. */
export function getApiBase() {
  const env = import.meta.env.VITE_API_URL;
  if (env) {
    return env.endsWith('/') ? env : `${env}/`;
  }
  return `${window.location.origin}/api/`;
}

/** WebSocket на том же хосте (Vite proxy /ws или Django :8000). */
export function getWsBase() {
  if (import.meta.env.VITE_WS_URL) {
    return import.meta.env.VITE_WS_URL.replace(/\/$/, '');
  }
  const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${proto}//${window.location.host}`;
}
