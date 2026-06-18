import { Link } from 'react-router-dom';
import { mediaUrl } from '../utils/mediaUrl';
import FavoriteButton from './FavoriteButton';

export default function CandleCard({ candle, favorited }) {
  const src = mediaUrl(candle.image);

  return (
    <article className="card">
      <Link to={`/candles/${candle.id}`} className="card-image-link">
        {src ? (
          <img className="card-image" src={src} alt={candle.name} loading="lazy" />
        ) : (
          <div className="card-placeholder" aria-hidden>🕯</div>
        )}
        <div className="card-body">
          <h3>{candle.name}</h3>
          <p className="card-price">{candle.price} ₽</p>
        </div>
      </Link>
      <div className="card-actions">
        <FavoriteButton candleId={candle.id} favorited={favorited} />
      </div>
    </article>
  );
}
