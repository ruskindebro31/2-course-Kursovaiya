import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../api/client';
import CandleCard from './CandleCard';

export const SEASON_GROUPS = [
  { value: '', label: 'Все коллекции' },
  { value: 'spring', label: 'Весенние' },
  { value: 'summer', label: 'Летние' },
  { value: 'holiday', label: 'Праздничные' },
];

export default function ProductCatalog({ title = 'Каталог', showHero = false }) {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [season, setSeason] = useState('');
  const [query, setQuery] = useState({ search: '', season: '' });

  const { data: favorites } = useQuery({
    queryKey: ['favorites'],
    queryFn: () => api.get('favorites/').then((r) => r.data.results || r.data),
    retry: false,
  });

  const { data, isLoading } = useQuery({
    queryKey: ['candles', page, query],
    queryFn: () => api.get('candles/', {
      params: {
        page,
        search: query.search || undefined,
        season: query.season || undefined,
      },
    }).then((r) => r.data),
  });

  const favIds = new Set((favorites || []).map((f) => f.candle));

  const applySeason = (value) => {
    setSeason(value);
    setPage(1);
    setQuery((q) => ({ ...q, season: value }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    setQuery({ search, season });
  };

  return (
    <div className="page-with-sidebar">
      <aside className="sidebar">
        <h2 className="sidebar-title">Коллекции</h2>
        <ul className="sidebar-list">
          {SEASON_GROUPS.map((group) => (
            <li key={group.value || 'all'}>
              <button
                type="button"
                className={season === group.value ? 'sidebar-link active' : 'sidebar-link'}
                onClick={() => applySeason(group.value)}
              >
                {group.label}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      <div className="page-main">
        {showHero && (
          <section className="hero-compact">
            <h1>Candels</h1>
            <p>Интернет-магазин свечей ручной работы</p>
          </section>
        )}
        <section>
          <h1>{title}</h1>
          <form className="filters stack-form" onSubmit={handleSearch}>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Поиск..."
            />
            <button type="submit" className="btn">Найти</button>
          </form>
          {isLoading ? <p>Загрузка...</p> : (
            <div className="product-list">
              {(data?.results || []).map((candle) => (
                <CandleCard key={candle.id} candle={candle} favorited={favIds.has(candle.id)} />
              ))}
            </div>
          )}
          <div className="pagination">
            <button type="button" disabled={!data?.previous} onClick={() => setPage((p) => p - 1)}>Назад</button>
            <span>Стр. {page}</span>
            <button type="button" disabled={!data?.next} onClick={() => setPage((p) => p + 1)}>Вперёд</button>
          </div>
        </section>
      </div>
    </div>
  );
}
