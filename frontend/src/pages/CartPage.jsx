import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/client';
import { useCartStore } from '../store/cartStore';
import { useAuth } from '../contexts/AuthContext';

function CartContent() {
  const { items, removeItem, total, clear } = useCartStore();
  const { isAuth } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const checkout = async () => {
    if (!isAuth) {
      navigate('/login', { state: { from: { pathname: '/cart' } } });
      return;
    }
    setLoading(true);
    setError('');
    try {
      await api.post('orders/', {
        items: items.map((i) => ({
          candle: i.id,
          quantity: i.qty,
          price: i.price,
        })),
      });
      clear();
      navigate('/orders');
    } catch {
      setError('Ошибка оформления заказа');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="cart-page">
      <h1>Корзина</h1>
      {items.length === 0 ? <p>Корзина пуста</p> : (
        <>
          <ul className="cart-list">
            {items.map((item) => (
              <li key={item.id} className="cart-item">
                <span>{item.name} × {item.qty} — {Number(item.price) * item.qty} ₽</span>
                <button type="button" className="btn-secondary" onClick={() => removeItem(item.id)}>Удалить</button>
              </li>
            ))}
          </ul>
          <p className="cart-total">Итого: {total()} ₽</p>
          {error && <p className="error">{error}</p>}
          <div className="stack-actions">
            <button type="button" className="btn" onClick={checkout} disabled={loading}>
              {loading ? 'Оформление...' : 'Оформить заказ'}
            </button>
            <button type="button" className="btn-secondary" onClick={clear}>Очистить</button>
            <Link to="/catalog" className="btn">Продолжить покупки</Link>
          </div>
        </>
      )}
      {items.length === 0 && (
        <div className="stack-actions">
          <Link to="/catalog" className="btn">Продолжить покупки</Link>
        </div>
      )}
    </section>
  );
}

export default function CartPage() {
  return <CartContent />;
}
