const test = require('node:test');
const assert = require('node:assert/strict');
const { collectVotesFromResult } = require('../votes');

test('returns zero counts when the database has no votes', () => {
  assert.deepEqual(collectVotesFromResult({ rows: [] }), { a: 0, b: 0 });
});

test('maps database counts to the two vote options', () => {
  const result = { rows: [{ vote: 'a', count: '3' }, { vote: 'b', count: '2' }] };

  assert.deepEqual(collectVotesFromResult(result), { a: 3, b: 2 });
});

test('keeps the missing option at zero', () => {
  assert.deepEqual(collectVotesFromResult({ rows: [{ vote: 'b', count: '4' }] }), { a: 0, b: 4 });
});
