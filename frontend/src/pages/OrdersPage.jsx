import { useQuery } from '@tanstack/react-query';
import api from '../api/client';

function OrdersList() {
  const { data, isLoading } = useQuery({
    queryKey: ['orders'],
    queryFn: () => api.get('orders/').then((r) => r.data.results || r.data),
  });

  if (isLoading) return <p>Загрузка...</p>;

  return (
    <section>
      <h1>Мои заказы</h1>
      <ul>
        {(data || []).map((order) => (
          <li key={order.id}>
            Заказ #{order.id} — {order.total_price} ₽ — {order.status}
            <ul>
              {(order.items || []).map((item) => (
                <li key={item.id}>{item.candle_name} × {item.quantity}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function OrdersPage() {
  return <OrdersList />;
}
