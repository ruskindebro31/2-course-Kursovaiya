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
      <form className="stack-form profile-form" onSubmit={handleSave}>
        <label className="field-label">
          О себе
          <textarea value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} placeholder="Расскажите о себе" rows={4} />
        </label>
        <label className="field-label">
          Телефон
          <input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} placeholder="+7 ..." />
        </label>
        <button type="submit" className="btn">Сохранить</button>
      </form>
      {saved && <p>Сохранено!</p>}
    </section>
  );
}
