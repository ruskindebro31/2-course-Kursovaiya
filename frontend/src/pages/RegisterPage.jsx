import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '', email: '', first_name: '', last_name: '', password: '', password_confirm: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await register(form);
      navigate('/catalog');
    } catch (err) {
      const detail = err.response?.data;
      const msg = typeof detail === 'object'
        ? Object.entries(detail).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`).join('; ')
        : null;
      setError(msg || 'Ошибка регистрации. Проверьте данные.');
    }
  };

  return (
    <section className="auth">
      <h1>Регистрация</h1>
      <form onSubmit={handleSubmit}>
        {['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm'].map((field) => (
          <input
            key={field}
            type={field.includes('password') ? 'password' : field === 'email' ? 'email' : 'text'}
            placeholder={field}
            value={form[field]}
            onChange={(e) => setForm({ ...form, [field]: e.target.value })}
            required
          />
        ))}
        {error && <p className="error">{error}</p>}
        <button type="submit">Зарегистрироваться</button>
      </form>
      <p>Уже есть аккаунт? <Link to="/login">Вход</Link></p>
    </section>
  );
}
