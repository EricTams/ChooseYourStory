export function orderChoices(choices, shuffle, random = Math.random) {
  const ordered = [...choices];
  if (!shuffle) return ordered;
  for (let i = ordered.length - 1; i > 0; i -= 1) {
    const j = Math.floor(random() * (i + 1));
    [ordered[i], ordered[j]] = [ordered[j], ordered[i]];
  }
  return ordered;
}
