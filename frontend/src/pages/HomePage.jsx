import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <section className="hero-page">
      <h1>Candels</h1>
      <p>Интернет-магазин свечей ручной работы</p>
      <Link to="/catalog" className="btn">Смотреть каталог</Link>
    </section>
  );
}
