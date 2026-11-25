function collectVotesFromResult(result) {
  const votes = { a: 0, b: 0 };

  result.rows.forEach((row) => {
    votes[row.vote] = parseInt(row.count, 10);
  });

  return votes;
}

module.exports = { collectVotesFromResult };
