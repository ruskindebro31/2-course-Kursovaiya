import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import api from '../api/client';
import FavoriteButton from '../components/FavoriteButton';

export default function FavoritesPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['favorites'],
    queryFn: () => api.get('favorites/').then((r) => r.data.results || r.data),
  });

  if (isLoading) return <p>Загрузка...</p>;

  return (
    <section>
      <h1>Избранное</h1>
      <div className="grid">
        {(data || []).map((fav) => (
          <article key={fav.id} className="card">
            <Link to={`/candles/${fav.candle}`}>
              <h3>{fav.candle_detail?.name || `Свеча #${fav.candle}`}</h3>
              <p>{fav.candle_detail?.price} ₽</p>
            </Link>
            <FavoriteButton candleId={fav.candle} favorited />
          </article>
        ))}
      </div>
    </section>
  );
}
