import { describe, it, expect } from 'vitest';

describe('auth tokens', () => {
  it('stores access token in localStorage', () => {
    localStorage.setItem('access_token', 'test-token');
    expect(localStorage.getItem('access_token')).toBe('test-token');
    localStorage.removeItem('access_token');
  });
});
