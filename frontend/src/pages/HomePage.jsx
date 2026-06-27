import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/client';
import CandleCard from '../components/CandleCard';

export default function HomePage() {
  const { data, isLoading } = useQuery({
    queryKey: ['candles', 'home'],
    queryFn: () => api.get('candles/', { params: { page: 1 } }).then((r) => r.data),
  });

  const featured = (data?.results || []).slice(0, 6);

  return (
    <div className="home-page">
      <section className="hero-page hero-compact">
        <h1>Candels</h1>
        <p>Интернет-магазин свечей ручной работы — без регистрации можно смотреть каталог и собирать корзину</p>
        <div className="stack-actions home-actions">
          <Link to="/catalog" className="btn">Смотреть каталог</Link>
          <Link to="/cart" className="btn-secondary">Корзина</Link>
        </div>
      </section>

      <section className="home-featured">
        <h2>Популярные свечи</h2>
        {isLoading ? <p>Загрузка...</p> : (
          <div className="product-list">
            {featured.map((candle) => (
              <CandleCard key={candle.id} candle={candle} />
            ))}
          </div>
        )}
        {!isLoading && featured.length === 0 && <p>Скоро появятся новые ароматы.</p>}
        <div className="stack-actions">
          <Link to="/catalog" className="btn">Весь каталог</Link>
        </div>
      </section>
    </div>
  );
}
