import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function ProtectedRoute({ children }) {
  const { isAuth, loading } = useAuth();
  if (loading) return <p>Загрузка...</p>;
  if (!isAuth) return <Navigate to="/login" replace />;
  return children;
}
