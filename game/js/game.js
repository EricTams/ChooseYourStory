const app = document.getElementById('app');

let currentView = 'library';
let currentStory = null;
let currentSceneId = null;
const imageAvailability = new Map();
const COVER_PLACEHOLDER = 'Cover art coming soon';
const SCENE_PLACEHOLDER = 'Scene art coming soon';

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
  return res.json();
}

function normalizePath(path) {
  return typeof path === 'string' ? path.trim() : '';
}

function createPlaceholder(className, text) {
  const placeholder = document.createElement('div');
  placeholder.className = className;
  placeholder.textContent = text;
  return placeholder;
}

async function canLoadImage(path) {
  const cleanPath = normalizePath(path);
  if (!cleanPath) return false;
  if (imageAvailability.has(cleanPath)) return imageAvailability.get(cleanPath);
  try {
    const response = await fetch(cleanPath, { method: 'HEAD' });
    imageAvailability.set(cleanPath, response.ok);
    return response.ok;
  } catch {
    imageAvailability.set(cleanPath, false);
    return false;
  }
}

async function renderOptionalImage(container, options) {
  const placeholder = createPlaceholder(options.placeholderClass, options.placeholderText);
  container.appendChild(placeholder);
  const imagePath = normalizePath(options.path);
  if (!await canLoadImage(imagePath)) return;
  const image = document.createElement('img');
  image.src = imagePath;
  image.alt = options.altText;
  image.className = options.imageClass;
  image.onerror = () => placeholder.replaceWith(createPlaceholder(options.placeholderClass, options.placeholderText));
  placeholder.replaceWith(image);
}

function resolveStartScene(story) {
  if (!story || !story.scenes) return null;
  if (story.startScene && story.scenes[story.startScene]) return story.startScene;
  const sceneIds = Object.keys(story.scenes);
  return sceneIds.length > 0 ? sceneIds[0] : null;
}

function renderEmptyStoryMessage() {
  app.innerHTML = '<p style="padding:2rem;text-align:center">This story has no scenes yet.</p>';
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

    const body = document.createElement('div');
    body.className = 'card-body';
    body.innerHTML = `<h2>${esc(entry.title)}</h2><p>${esc(entry.summary || 'Story summary coming soon.')}</p>`;

    renderOptionalImage(card, {
      path: entry.cover,
      altText: entry.title,
      imageClass: 'story-cover',
      placeholderClass: 'story-cover-placeholder',
      placeholderText: COVER_PLACEHOLDER,
    });
    card.appendChild(body);
    card.addEventListener('click', () => startStory(entry.slug));
    grid.appendChild(card);
  }

  app.appendChild(grid);
}

function renderReader() {
  if (!currentSceneId) {
    renderEmptyStoryMessage();
    return;
  }
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

  const media = document.createElement('div');
  media.className = 'scene-media';
  renderOptionalImage(media, {
    path: scene.image,
    altText: scene.title || 'Scene image',
    imageClass: 'scene-image',
    placeholderClass: 'scene-image-placeholder',
    placeholderText: SCENE_PLACEHOLDER,
  });
  container.appendChild(media);

  const title = document.createElement('h2');
  title.className = 'scene-title';
  title.textContent = scene.title || 'Untitled Scene';
  container.appendChild(title);

  const textDiv = document.createElement('div');
  textDiv.className = 'scene-text';
  const paragraphs = (scene.text || '').split('\n').filter(p => p.trim());
  if (paragraphs.length === 0) paragraphs.push('Story text coming soon.');
  for (const p of paragraphs) {
    const el = document.createElement('p');
    el.textContent = p;
    textDiv.appendChild(el);
  }
  container.appendChild(textDiv);

  const sceneChoices = Array.isArray(scene.choices) ? scene.choices : [];
  if (sceneChoices.length === 0) {
    renderEnding(container);
  } else {
    renderChoices(container, sceneChoices);
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
    currentSceneId = resolveStartScene(currentStory);
    currentView = 'reader';
    if (!currentSceneId) {
      renderEmptyStoryMessage();
      return;
    }
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
