import React from 'react';
import useCartStore from '../store/cartStore';

export default function CartPage() {
  const { items, getTotal, removeItem } = useCartStore();

  return (
    <div>
      <h1>Корзина</h1>
      {items.length === 0 ? (
        <p>Корзина пуста</p>
      ) : (
        <ul>
          {items.map(item => (
            <li key={item.id}>
              {item.name} — {item.price} x {item.quantity}
              <button onClick={() => removeItem(item.id)}>Удалить</button>
            </li>
          ))}
        </ul>
      )}
      <h3>Итого: {getTotal()} руб.</h3>
    </div>
  );
}
