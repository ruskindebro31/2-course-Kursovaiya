import React, { useEffect, useState } from 'react';
import api from '../api/client';

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    api.get('/users/me/')
      .then(res => setProfile(res.data))
      .catch(err => console.error(err));
  }, []);

  if (!profile) return <div>Загрузка...</div>;

  return (
    <div>
      <h1>Личный кабинет</h1>
      <p>Имя: {profile.first_name}</p>
      <p>Email: {profile.email}</p>
    </div>
  );
}
