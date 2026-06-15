import { Link } from 'react-router-dom';
import { useCartStore } from '../store/cartStore';

export default function CartPage() {
  const { items, removeItem, total, clear } = useCartStore();

  return (
    <section>
      <h1>Корзина</h1>
      {items.length === 0 ? <p>Корзина пуста</p> : (
        <>
          <ul>
            {items.map((item) => (
              <li key={item.id}>
                {item.name} × {item.qty} — {Number(item.price) * item.qty} ₽
                <button type="button" onClick={() => removeItem(item.id)}>Удалить</button>
              </li>
            ))}
          </ul>
          <p>Итого: {total()} ₽</p>
          <button type="button" onClick={clear}>Очистить</button>
          <Link to="/catalog" className="btn">Продолжить покупки</Link>
        </>
      )}
    </section>
  );
}
