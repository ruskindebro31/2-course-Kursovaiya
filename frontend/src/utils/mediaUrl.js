import { getApiBase } from './apiConfig';

const siteOrigin = () => getApiBase().replace(/\/api\/?$/, '');

export function mediaUrl(path) {
  if (!path) return null;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return `${siteOrigin()}${normalized}`;
}
