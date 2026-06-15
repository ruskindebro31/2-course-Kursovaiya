import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useCartStore = create(
  persist(
    (set, get) => ({
      items: [],
      addItem: (candle, qty = 1) => {
        const items = get().items;
        const existing = items.find((i) => i.id === candle.id);
        if (existing) {
          set({ items: items.map((i) => i.id === candle.id ? { ...i, qty: i.qty + qty } : i) });
        } else {
          set({ items: [...items, { ...candle, qty }] });
        }
      },
      removeItem: (id) => set({ items: get().items.filter((i) => i.id !== id) }),
      clear: () => set({ items: [] }),
      total: () => get().items.reduce((s, i) => s + Number(i.price) * i.qty, 0),
    }),
    { name: 'candels-cart' },
  ),
);
