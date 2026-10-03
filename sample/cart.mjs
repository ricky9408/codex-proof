export function totalCents(items) { return items.reduce((sum, item) => sum + item.priceCents, 0); }
export function removeItem(items, id) {
  const remaining = items.filter(item => item.id !== id);
  return { items: remaining, totalCents: totalCents(remaining) };
}
