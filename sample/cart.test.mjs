import { test } from 'node:test';
import assert from 'node:assert/strict';
const { removeItem, totalCents } = await import(process.env.PROOF_VARIANT === 'before' ? './cart.buggy.mjs' : './cart.mjs');
const items = [{id:'notebook',priceCents:1200},{id:'mug',priceCents:1800}];
test('Removing notebook preserves the remaining mug total ($18.00)', () => {
  const result = removeItem(items, 'notebook');
  assert.deepEqual(result.items, [items[1]]);
  assert.equal(result.totalCents, 1800);
});
test('Removing last item yields an empty cart and zero total', () => {
  assert.deepEqual(removeItem([items[0]], 'notebook'), {items:[],totalCents:0});
});
test('Unknown item leaves total unchanged', () => {
  assert.equal(removeItem(items, 'unknown').totalCents, totalCents(items));
});
