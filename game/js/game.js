const app = document.getElementById('app');

let currentView = 'library';
let currentStory = null;
let currentSceneId = null;

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
  return res.json();
}

function renderLibrary(catalog) {
  app.innerHTML = '';

  const header = document.createElement('header');
  header.className = 'library-header';
  header.innerHTML = '<h1>Choose Your Adventure</h1>';
  app.appendChild(header);

  if (!catalog.stories || catalog.stories.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'empty-library';
    empty.innerHTML = '<p>No stories yet. Adventures are being written\u2026</p>';
    app.appendChild(empty);
    return;
  }

  const grid = document.createElement('div');
  grid.className = 'story-grid';

  for (const entry of catalog.stories) {
    const card = document.createElement('div');
    card.className = 'story-card';

    const img = document.createElement('img');
    img.src = entry.cover;
    img.alt = entry.title;
    img.onerror = () => { img.style.display = 'none'; };

    const body = document.createElement('div');
    body.className = 'card-body';
    body.innerHTML = `<h2>${esc(entry.title)}</h2><p>${esc(entry.summary)}</p>`;

    card.appendChild(img);
    card.appendChild(body);
    card.addEventListener('click', () => startStory(entry.slug));
    grid.appendChild(card);
  }

  app.appendChild(grid);
}

function renderReader() {
  const scene = currentStory.scenes[currentSceneId];
  if (!scene) {
    app.innerHTML = `<p style="padding:2rem;text-align:center">Scene "${currentSceneId}" not found.</p>`;
    return;
  }

  app.innerHTML = '';

  const header = document.createElement('header');
  header.className = 'reader-header';
  const link = document.createElement('a');
  link.href = '#';
  link.textContent = currentStory.title;
  link.addEventListener('click', (e) => { e.preventDefault(); goToLibrary(); });
  header.appendChild(link);
  app.appendChild(header);

  const container = document.createElement('div');
  container.className = 'scene';

  if (scene.image) {
    const img = document.createElement('img');
    img.src = scene.image;
    img.alt = scene.title;
    img.className = 'scene-image';
    container.appendChild(img);
  }

  const title = document.createElement('h2');
  title.className = 'scene-title';
  title.textContent = scene.title;
  container.appendChild(title);

  const textDiv = document.createElement('div');
  textDiv.className = 'scene-text';
  const paragraphs = scene.text.split('\n').filter(p => p.trim());
  for (const p of paragraphs) {
    const el = document.createElement('p');
    el.textContent = p;
    textDiv.appendChild(el);
  }
  container.appendChild(textDiv);

  if (scene.choices.length === 0) {
    renderEnding(container);
  } else {
    renderChoices(container, scene.choices);
  }

  app.appendChild(container);
}

function renderChoices(container, choices) {
  const div = document.createElement('div');
  div.className = 'choices';
  for (const choice of choices) {
    const btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.textContent = choice.text;
    btn.addEventListener('click', () => navigateTo(choice.target));
    div.appendChild(btn);
  }
  container.appendChild(div);
}

function renderEnding(container) {
  const div = document.createElement('div');
  div.className = 'ending';
  div.innerHTML = '<p class="the-end">The End</p>';
  const btn = document.createElement('button');
  btn.className = 'choice-btn';
  btn.textContent = 'Return to Library';
  btn.addEventListener('click', goToLibrary);
  div.appendChild(btn);
  container.appendChild(div);
}

function navigateTo(sceneId) {
  currentSceneId = sceneId;
  renderReader();
  window.scrollTo(0, 0);
}

async function startStory(slug) {
  try {
    currentStory = await fetchJSON(`data/stories/${slug}.json`);
    currentSceneId = currentStory.startScene;
    currentView = 'reader';
    renderReader();
    window.scrollTo(0, 0);
  } catch (err) {
    console.error(err);
    app.innerHTML = `<p style="padding:2rem;text-align:center">Failed to load story.</p>`;
  }
}

async function goToLibrary() {
  currentStory = null;
  currentSceneId = null;
  currentView = 'library';
  try {
    const catalog = await fetchJSON('data/catalog.json');
    renderLibrary(catalog);
  } catch {
    renderLibrary({ stories: [] });
  }
}

function esc(str) {
  const el = document.createElement('span');
  el.textContent = str || '';
  return el.innerHTML;
}

goToLibrary();
