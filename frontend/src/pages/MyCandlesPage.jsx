import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import api from '../api/client';
import { useAuth } from '../contexts/AuthContext';

export default function MyCandlesPage() {
  const { isAuth } = useAuth();
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ['my-candles'],
    queryFn: () => api.get('candles/mine/').then((r) => r.data.results || r.data),
    enabled: isAuth,
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`candles/${id}/`),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['my-candles'] }),
  });

  if (!isAuth) return <p><Link to="/login">Войдите</Link>, чтобы видеть свои свечи.</p>;
  if (isLoading) return <p>Загрузка...</p>;

  return (
    <section>
      <h1>Мои свечи</h1>
      <Link to="/candles/new" className="btn">Добавить свечу</Link>
      <ul className="my-list">
        {(data || []).map((c) => (
          <li key={c.id}>
            <Link to={`/candles/${c.id}/edit`}>{c.name}</Link> — {c.price} ₽
            <button type="button" onClick={() => deleteMutation.mutate(c.id)}>Удалить</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
