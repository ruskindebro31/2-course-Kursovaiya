import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/client';
import FavoriteButton from '../components/FavoriteButton';
import ReviewList from '../components/ReviewList';

export default function CandleDetailPage() {
  const { id } = useParams();
  const { data: candle, isLoading } = useQuery({
    queryKey: ['candle', id],
    queryFn: () => api.get(`candles/${id}/`).then((r) => r.data),
  });
  const { data: favorites } = useQuery({
    queryKey: ['favorites'],
    queryFn: () => api.get('favorites/').then((r) => r.data.results || r.data),
    retry: false,
  });

  if (isLoading) return <p>Загрузка...</p>;
  if (!candle) return <p>Не найдено</p>;

  const favorited = (favorites || []).some((f) => f.candle === Number(id));

  return (
    <section>
      <h1>{candle.name}</h1>
      <p>{candle.description}</p>
      <p className="price">{candle.price} ₽</p>
      <FavoriteButton candleId={candle.id} favorited={favorited} />
      <ReviewList candleId={candle.id} />
    </section>
  );
}
