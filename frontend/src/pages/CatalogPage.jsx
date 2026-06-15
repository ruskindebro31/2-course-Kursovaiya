import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import api from '../api/client';
import FavoriteButton from '../components/FavoriteButton';

export default function CatalogPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [query, setQuery] = useState({ search: '', category: '' });

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.get('categories/').then((r) => r.data),
  });

  const { data: favorites } = useQuery({
    queryKey: ['favorites'],
    queryFn: () => api.get('favorites/').then((r) => r.data.results || r.data),
    retry: false,
  });

  const { data, isLoading } = useQuery({
    queryKey: ['candles', page, query],
    queryFn: () => api.get('candles/', {
      params: { page, search: query.search || undefined, category: query.category || undefined },
    }).then((r) => r.data),
  });

  const favIds = new Set((favorites || []).map((f) => f.candle));

  return (
    <section>
      <h1>Каталог</h1>
      <form className="filters" onSubmit={(e) => { e.preventDefault(); setPage(1); setQuery({ search, category }); }}>
        <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Поиск..." />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">Все категории</option>
          {(categories || []).map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <button type="submit">Найти</button>
      </form>
      {isLoading ? <p>Загрузка...</p> : (
        <div className="grid">
          {(data?.results || []).map((candle) => (
            <article key={candle.id} className="card">
              <Link to={`/candles/${candle.id}`}>
                <h3>{candle.name}</h3>
                <p>{candle.price} ₽</p>
              </Link>
              <FavoriteButton candleId={candle.id} favorited={favIds.has(candle.id)} />
            </article>
          ))}
        </div>
      )}
      <div className="pagination">
        <button type="button" disabled={!data?.previous} onClick={() => setPage((p) => p - 1)}>Назад</button>
        <span>Стр. {page}</span>
        <button type="button" disabled={!data?.next} onClick={() => setPage((p) => p + 1)}>Вперёд</button>
      </div>
    </section>
  );
}
