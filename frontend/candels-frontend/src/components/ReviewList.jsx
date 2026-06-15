import React from 'react';

export default function ReviewList({ reviews }) {
  return (
    <div>
      <h3>Отзывы</h3>
      {reviews.map(review => (
        <div key={review.id}>
          <strong>{review.user}</strong> — {review.rating}/5
          <p>{review.comment}</p>
        </div>
      ))}
    </div>
  );
}
