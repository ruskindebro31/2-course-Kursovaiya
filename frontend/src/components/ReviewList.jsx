import { useEffect, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../api/client';
import { useAuth } from '../contexts/AuthContext';

const WS_BASE = import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000';

export default function ReviewList({ candleId }) {
  const { isAuth } = useAuth();
  const queryClient = useQueryClient();
  const [text, setText] = useState('');
  const [rating, setRating] = useState(5);
  const [liveReviews, setLiveReviews] = useState([]);

  const { data } = useQuery({
    queryKey: ['reviews', candleId],
    queryFn: () => api.get(`reviews/by-candle/${candleId}/`).then((r) => r.data.results || r.data),
  });

  useEffect(() => {
    const ws = new WebSocket(`${WS_BASE}/ws/reviews/${candleId}/`);
    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      if (payload.type === 'review') {
        setLiveReviews((prev) => {
          if (prev.some((r) => r.id === payload.review.id)) return prev;
          return [...prev, payload.review];
        });
      }
    };
    return () => ws.close();
  }, [candleId]);

  const mutation = useMutation({
    mutationFn: (body) => api.post('reviews/', { candle: candleId, ...body }),
    onMutate: async (body) => {
      const optimistic = {
        id: `opt-${Date.now()}`,
        user: 'Вы',
        rating: body.rating,
        comment: body.comment,
        created_at: new Date().toISOString(),
      };
      setLiveReviews((prev) => [...prev, optimistic]);
      setText('');
      return { optimistic };
    },
    onError: (_e, _b, ctx) => {
      if (ctx?.optimistic) {
        setLiveReviews((prev) => prev.filter((r) => r.id !== ctx.optimistic.id));
      }
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['reviews', candleId] }),
  });

  const all = [...(data || []), ...liveReviews.filter((lr) => !(data || []).some((r) => r.id === lr.id))];

  return (
    <section className="reviews">
      <h3>Отзывы</h3>
      <ul>
        {all.map((r) => (
          <li key={r.id}>
            <strong>{r.user}</strong> — {r.rating}★
            <p>{r.comment}</p>
          </li>
        ))}
      </ul>
      {isAuth && (
        <form onSubmit={(e) => { e.preventDefault(); mutation.mutate({ comment: text, rating: Number(rating) }); }}>
          <select value={rating} onChange={(e) => setRating(e.target.value)}>
            {[5, 4, 3, 2, 1].map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
          <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Ваш отзыв" required />
          <button type="submit">Отправить</button>
        </form>
      )}
    </section>
  );
}
