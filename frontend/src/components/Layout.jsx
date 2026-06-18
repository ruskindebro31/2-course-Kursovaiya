import { Link, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import useNotifications from '../hooks/useNotifications';
import { useCartStore } from '../store/cartStore';

export default function Layout() {
  const { isAuth, user, logout } = useAuth();
  const notifications = useNotifications(user?.id);
  const cartCount = useCartStore((s) => s.items.reduce((sum, item) => sum + item.qty, 0));

  return (
    <div className="layout">
      <header className="header">
        <Link to="/" className="logo">Candels</Link>
        <nav>
          <Link to="/catalog">Каталог</Link>
          <Link to="/my-candles">Мои свечи</Link>
          <Link to="/favorites">Избранное</Link>
          <Link to="/cart">
            Корзина
            {cartCount > 0 && <span className="badge">{cartCount}</span>}
          </Link>
          <Link to="/orders">Заказы</Link>
          {isAuth ? (
            <>
              <Link to="/profile">Профиль</Link>
              <button type="button" onClick={logout}>Выйти</button>
              {notifications.length > 0 && (
                <span className="badge">{notifications.length}</span>
              )}
            </>
          ) : (
            <>
              <Link to="/login">Вход</Link>
              <Link to="/register">Регистрация</Link>
            </>
          )}
        </nav>
      </header>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
