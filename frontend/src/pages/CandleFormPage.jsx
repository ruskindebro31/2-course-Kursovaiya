import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../api/client';
import { mediaUrl } from '../utils/mediaUrl';
import ProtectedRoute from '../components/ProtectedRoute';

function CandleForm() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '', description: '', price: '', category: '', is_published: true,
  });
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [error, setError] = useState('');

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.get('categories/').then((r) => r.data),
  });

  useEffect(() => {
    if (!isEdit) return;
    api.get(`candles/${id}/`).then((res) => {
      const c = res.data;
      setForm({
        name: c.name,
        description: c.description,
        price: c.price,
        category: c.category,
        is_published: c.is_published,
      });
      setImagePreview(mediaUrl(c.image));
    });
  }, [id, isEdit]);

  const handleImageChange = (e) => {
    const file = e.target.files?.[0];
    setImageFile(file || null);
    setImagePreview(file ? URL.createObjectURL(file) : imagePreview);
  };

  const buildPayload = () => {
    if (imageFile) {
      const formData = new FormData();
      formData.append('name', form.name);
      formData.append('description', form.description);
      formData.append('price', form.price);
      formData.append('category', form.category);
      formData.append('is_published', form.is_published);
      formData.append('image', imageFile);
      return formData;
    }
    return { ...form, price: Number(form.price), category: Number(form.category) };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const payload = buildPayload();
    try {
      if (isEdit) {
        await api.patch(`candles/${id}/`, payload);
      } else {
        await api.post('candles/', payload);
      }
      navigate('/my-candles');
    } catch {
      setError('Не удалось сохранить. Проверьте поля.');
    }
  };

  return (
    <section className="auth">
      <h1>{isEdit ? 'Редактировать свечу' : 'Новая свеча'}</h1>
      <form onSubmit={handleSubmit}>
        <input placeholder="Название" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <textarea placeholder="Описание" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required />
        <input type="number" step="0.01" placeholder="Цена" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} required />
        <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} required>
          <option value="">Категория</option>
          {(categories || []).map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
        <label>
          <input type="checkbox" checked={form.is_published} onChange={(e) => setForm({ ...form, is_published: e.target.checked })} />
          Опубликовано
        </label>
        <label className="file-label">
          Фото свечи
          <input type="file" accept="image/*" onChange={handleImageChange} />
        </label>
        {imagePreview && <img className="form-preview" src={imagePreview} alt="Превью" />}
        {error && <p className="error">{error}</p>}
        <button type="submit">Сохранить</button>
      </form>
    </section>
  );
}

export default function CandleFormPage() {
  return <ProtectedRoute><CandleForm /></ProtectedRoute>;
}
