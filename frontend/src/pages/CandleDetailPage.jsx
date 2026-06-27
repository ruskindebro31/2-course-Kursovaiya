import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/client';
import { useAuth } from '../contexts/AuthContext';
import FavoriteButton from '../components/FavoriteButton';
import ReviewList from '../components/ReviewList';
import { useCartStore } from '../store/cartStore';
import { mediaUrl } from '../utils/mediaUrl';

export default function CandleDetailPage() {
  const { id } = useParams();
  const { isAuth } = useAuth();
  const addItem = useCartStore((s) => s.addItem);
  const [added, setAdded] = useState(false);
  const { data: candle, isLoading } = useQuery({
    queryKey: ['candle', id],
    queryFn: () => api.get(`candles/${id}/`).then((r) => r.data),
  });
  const { data: favorites } = useQuery({
    queryKey: ['favorites'],
    queryFn: () => api.get('favorites/').then((r) => r.data.results || r.data),
    enabled: isAuth,
    retry: false,
  });

  if (isLoading) return <p>Загрузка...</p>;
  if (!candle) return <p>Не найдено</p>;

  const favorited = (favorites || []).some((f) => f.candle === Number(id));

  const imageSrc = mediaUrl(candle.image);

  const handleAddToCart = () => {
    addItem(candle);
    setAdded(true);
    window.setTimeout(() => setAdded(false), 2500);
  };

  return (
    <section className="candle-detail">
      <div className="candle-detail-media">
        {imageSrc ? (
          <img className="candle-detail-image" src={imageSrc} alt={candle.name} />
        ) : (
          <div className="card-placeholder candle-detail-placeholder" aria-hidden>🕯</div>
        )}
      </div>
      <div className="candle-detail-info">
        <h1>{candle.name}</h1>
        <p>{candle.description}</p>
        <p className="price">{candle.price} ₽</p>
        <div className="candle-detail-actions">
          <button
            type="button"
            className={added ? 'btn btn-added' : 'btn'}
            onClick={handleAddToCart}
          >
            {added ? '✓ Добавлено в корзину' : 'В корзину'}
          </button>
          <FavoriteButton candleId={candle.id} favorited={favorited} />
        </div>
        {added && <p className="cart-toast" role="status">Товар добавлен. Перейдите в корзину для оформления.</p>}
        <ReviewList candleId={candle.id} />
      </div>
    </section>
  );
}
