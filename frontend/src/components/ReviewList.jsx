import { useEffect, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import api from '../api/client';
import { useAuth } from '../contexts/AuthContext';
import { getWsBase } from '../utils/apiConfig';

export default function ReviewList({ candleId }) {
  const { isAuth } = useAuth();
  const queryClient = useQueryClient();
  const [text, setText] = useState('');
  const [rating, setRating] = useState(5);

  const { data } = useQuery({
    queryKey: ['reviews', candleId],
    queryFn: () => api.get(`reviews/by-candle/${candleId}/`).then((r) => r.data.results || r.data),
  });

  useEffect(() => {
    const ws = new WebSocket(`${getWsBase()}/ws/reviews/${candleId}/`);
    ws.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      if (payload.type !== 'review') return;
      queryClient.setQueryData(['reviews', candleId], (old) => {
        const list = old || [];
        if (list.some((r) => r.id === payload.review.id)) return old;
        return [...list, payload.review];
      });
    };
    return () => ws.close();
  }, [candleId, queryClient]);

  const mutation = useMutation({
    mutationFn: (body) => api.post('reviews/', { candle: candleId, ...body }),
    onMutate: async (body) => {
      await queryClient.cancelQueries({ queryKey: ['reviews', candleId] });
      const previous = queryClient.getQueryData(['reviews', candleId]);
      const optimistic = {
        id: `opt-${Date.now()}`,
        user: 'Вы',
        rating: body.rating,
        comment: body.comment,
        created_at: new Date().toISOString(),
      };
      queryClient.setQueryData(['reviews', candleId], [...(previous || []), optimistic]);
      setText('');
      return { previous };
    },
    onError: (_error, _body, context) => {
      if (context?.previous) {
        queryClient.setQueryData(['reviews', candleId], context.previous);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['reviews', candleId] });
    },
  });

  const reviews = data || [];

  return (
    <section className="reviews">
      <h3>Отзывы</h3>
      <ul>
        {reviews.map((r) => (
          <li key={r.id}>
            <strong>{r.user}</strong> — {r.rating}★
            <p>{r.comment}</p>
          </li>
        ))}
      </ul>
      {isAuth && (
        <form className="stack-form review-form" onSubmit={(e) => { e.preventDefault(); mutation.mutate({ comment: text, rating: Number(rating) }); }}>
          <label className="field-label">
            Оценка
            <select value={rating} onChange={(e) => setRating(e.target.value)}>
              {[5, 4, 3, 2, 1].map((n) => <option key={n} value={n}>{n}</option>)}
            </select>
          </label>
          <label className="field-label">
            Комментарий
            <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Ваш отзыв" required rows={3} />
          </label>
          <button type="submit" className="btn" disabled={mutation.isPending}>
            {mutation.isPending ? 'Отправка...' : 'Отправить'}
          </button>
        </form>
      )}
    </section>
  );
}
