import { useEffect, useState } from 'react';
import api from '../api/client';
import { useAuth } from '../contexts/AuthContext';

export default function ProfilePage() {
  const { user } = useAuth();
  const [form, setForm] = useState({ bio: '', phone: '' });
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api.get('auth/profile/').then((res) => {
      setForm({ bio: res.data.bio || '', phone: res.data.phone || res.data.user?.phone || '' });
    });
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    await api.patch('auth/profile/', form);
    setSaved(true);
  };

  return (
    <section>
      <h1>Профиль</h1>
      {user && <p>{user.first_name} {user.last_name} ({user.email})</p>}
      <form onSubmit={handleSave}>
        <textarea value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} placeholder="О себе" />
        <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="Телефон" />
        <button type="submit">Сохранить</button>
      </form>
      {saved && <p>Сохранено!</p>}
    </section>
  );
}
