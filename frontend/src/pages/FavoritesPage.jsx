import { useQuery } from '@tanstack/react-query';
import api from '../api/client';
import CandleCard from '../components/CandleCard';

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
          <CandleCard
            key={fav.id}
            candle={fav.candle_detail || { id: fav.candle, name: `Свеча #${fav.candle}`, price: '—' }}
            favorited
          />
        ))}
      </div>
    </section>
  );
}
