import { useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../api/client';
import { useAuth } from '../contexts/AuthContext';

export default function FavoriteButton({ candleId, favorited }) {
  const { isAuth } = useAuth();
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: () => api.post('favorites/toggle/', { candle: candleId }),
    onMutate: async () => {
      await queryClient.cancelQueries({ queryKey: ['favorites'] });
      const prev = queryClient.getQueryData(['favorites']);
      queryClient.setQueryData(['favorites'], (old = []) => {
        if (favorited) return old.filter((f) => f.candle !== candleId);
        return [...old, { candle: candleId, id: `temp-${candleId}` }];
      });
      return { prev };
    },
    onError: (_err, _vars, ctx) => {
      if (ctx?.prev) queryClient.setQueryData(['favorites'], ctx.prev);
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['favorites'] }),
  });

  if (!isAuth) return null;

  return (
    <button type="button" className="btn-fav" onClick={() => mutation.mutate()}>
      {favorited ? '★ В избранном' : '☆ В избранное'}
    </button>
  );
}
