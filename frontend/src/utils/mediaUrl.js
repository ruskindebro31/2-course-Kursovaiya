const API_ROOT = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/').replace(/\/api\/?$/, '');

export function mediaUrl(path) {
  if (!path) return null;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return `${API_ROOT}${normalized}`;
}
