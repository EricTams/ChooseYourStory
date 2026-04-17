const app = document.getElementById('app');

let currentView = 'library';
let currentStory = null;
let currentSceneId = null;
let currentCatalog = { stories: [] };
let isPhoneEditMode = false;
const imageAvailability = new Map();
const COVER_PLACEHOLDER = 'Cover art coming soon';
const SCENE_PLACEHOLDER = 'Scene art coming soon';
const LOCAL_DRAFT_PREFIX = 'cyoa-authoring-draft:';

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

function localDraftKey(slug) {
  return `${LOCAL_DRAFT_PREFIX}${slug}`;
}

function cloneStoryData(story) {
  return JSON.parse(JSON.stringify({
    slug: story.slug,
    title: story.title || '',
    startScene: story.startScene || '',
    scenes: story.scenes || {},
  }));
}

function normalizeStory(story, fallbackSlug) {
  const safeStory = story && typeof story === 'object' ? story : {};
  const safeScenes = safeStory.scenes && typeof safeStory.scenes === 'object' ? safeStory.scenes : {};
  return {
    slug: safeStory.slug || fallbackSlug || '',
    title: typeof safeStory.title === 'string' ? safeStory.title : '',
    startScene: typeof safeStory.startScene === 'string' ? safeStory.startScene : '',
    scenes: safeScenes,
  };
}

function saveCurrentStoryToLocal() {
  if (!currentStory || !currentStory.slug) return false;
  try {
    localStorage.setItem(localDraftKey(currentStory.slug), JSON.stringify(cloneStoryData(currentStory)));
    return true;
  } catch {
    return false;
  }
}

function loadStoryFromLocal(slug) {
  const raw = localStorage.getItem(localDraftKey(slug));
  if (!raw) return null;
  try {
    return normalizeStory(JSON.parse(raw), slug);
  } catch {
    return null;
  }
}

async function copyCurrentStoryJSON() {
  if (!currentStory) return false;
  const payload = JSON.stringify(cloneStoryData(currentStory), null, 2);
  if (navigator.clipboard && navigator.clipboard.writeText) {
    try {
      await navigator.clipboard.writeText(payload);
      return true;
    } catch {
      // fall through
    }
  }
  window.prompt('Copy story JSON', payload);
  return false;
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

function ensureSceneDefaults(scene) {
  const safeScene = scene && typeof scene === 'object' ? scene : {};
  const safeChoices = Array.isArray(safeScene.choices) ? safeScene.choices : [];
  return {
    title: typeof safeScene.title === 'string' ? safeScene.title : '',
    text: typeof safeScene.text === 'string' ? safeScene.text : '',
    image: typeof safeScene.image === 'string' ? safeScene.image : '',
    choices: safeChoices.map((choice) => ({
      text: typeof choice?.text === 'string' ? choice.text : '',
      target: typeof choice?.target === 'string' ? choice.target : '',
    })),
  };
}

function renderEmptyStoryMessage() {
  app.innerHTML = '<p style="padding:2rem;text-align:center">This story has no scenes yet.</p>';
}

function buildLibraryActions(catalog) {
  const actions = document.createElement('div');
  actions.className = 'library-actions';
  const btn = document.createElement('button');
  btn.className = 'phone-edit-btn';
  btn.textContent = 'Phone Edit Mode';
  btn.addEventListener('click', () => startPhoneEditMode(catalog));
  actions.appendChild(btn);
  return actions;
}

function renderLibrary(catalog) {
  app.innerHTML = '';
  currentCatalog = catalog;
  isPhoneEditMode = false;

  const header = document.createElement('header');
  header.className = 'library-header';
  header.innerHTML = '<h1>Choose Your Adventure</h1>';
  app.appendChild(header);
  app.appendChild(buildLibraryActions(catalog));

  if (!catalog.stories || catalog.stories.length === 0) {
    const empty = document.createElement('div');
    empty.className = 'empty-library';
    empty.innerHTML = '<p>No stories yet. Adventures are being written…</p>';
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

function createPhoneEditHeader() {
  const header = document.createElement('header');
  header.className = 'reader-header';

  const title = document.createElement('span');
  title.className = 'phone-edit-title';
  title.textContent = 'Phone Edit Mode';
  header.appendChild(title);

  const actions = document.createElement('div');
  actions.className = 'reader-actions';

  const saveBtn = document.createElement('button');
  saveBtn.className = 'reader-action-btn';
  saveBtn.textContent = 'Save Local';
  saveBtn.addEventListener('click', () => {
    collectPhoneEdits();
    toast(saveCurrentStoryToLocal() ? 'Local draft saved' : 'Local save failed');
  });
  actions.appendChild(saveBtn);

  const loadBtn = document.createElement('button');
  loadBtn.className = 'reader-action-btn';
  loadBtn.textContent = 'Load Local';
  loadBtn.addEventListener('click', () => {
    const loaded = loadStoryFromLocal(currentStory.slug);
    if (!loaded) {
      toast('No local draft found');
      return;
    }
    currentStory = loaded;
    currentSceneId = resolveStartScene(currentStory);
    if (!currentSceneId) {
      const firstId = `scene_${Date.now()}`;
      currentStory.scenes[firstId] = ensureSceneDefaults({});
      currentStory.startScene = firstId;
      currentSceneId = firstId;
    }
    renderReader();
    toast('Local draft loaded');
  });
  actions.appendChild(loadBtn);

  const copyBtn = document.createElement('button');
  copyBtn.className = 'reader-action-btn';
  copyBtn.textContent = 'Copy JSON';
  copyBtn.addEventListener('click', async () => {
    collectPhoneEdits();
    const copied = await copyCurrentStoryJSON();
    toast(copied ? 'Story JSON copied' : 'JSON ready to copy');
  });
  actions.appendChild(copyBtn);

  const exitBtn = document.createElement('button');
  exitBtn.className = 'reader-action-btn reader-action-secondary';
  exitBtn.textContent = 'Exit Edit';
  exitBtn.addEventListener('click', goToLibrary);
  actions.appendChild(exitBtn);

  header.appendChild(actions);
  return header;
}

function createReaderHeader() {
  if (isPhoneEditMode) return createPhoneEditHeader();

  const header = document.createElement('header');
  header.className = 'reader-header';
  const link = document.createElement('a');
  link.href = '#';
  link.textContent = currentStory.title;
  link.addEventListener('click', (e) => {
    e.preventDefault();
    goToLibrary();
  });
  header.appendChild(link);
  return header;
}

function renderEditableText(container, scene) {
  const titleInput = document.createElement('input');
  titleInput.className = 'scene-title scene-title-input';
  titleInput.value = scene.title || '';
  titleInput.placeholder = 'Scene title';
  titleInput.addEventListener('input', collectPhoneEdits);
  container.appendChild(titleInput);

  const textInput = document.createElement('textarea');
  textInput.className = 'scene-text scene-text-input';
  textInput.value = scene.text || '';
  textInput.placeholder = 'Write scene text...';
  textInput.addEventListener('input', collectPhoneEdits);
  container.appendChild(textInput);
}

function renderReadOnlyText(container, scene) {
  const title = document.createElement('h2');
  title.className = 'scene-title';
  title.textContent = scene.title || 'Untitled Scene';
  container.appendChild(title);

  const textDiv = document.createElement('div');
  textDiv.className = 'scene-text';
  const paragraphs = (scene.text || '').split('\n').filter((p) => p.trim());
  if (paragraphs.length === 0) paragraphs.push('Story text coming soon.');
  for (const p of paragraphs) {
    const el = document.createElement('p');
    el.textContent = p;
    textDiv.appendChild(el);
  }
  container.appendChild(textDiv);
}

function renderEditableChoices(container, choices) {
  const wrapper = document.createElement('div');
  wrapper.className = 'choices phone-edit-choices';

  choices.forEach((choice, index) => {
    const row = document.createElement('div');
    row.className = 'phone-choice-row';

    const textInput = document.createElement('input');
    textInput.className = 'choice-btn choice-input';
    textInput.placeholder = 'Choice text';
    textInput.value = choice.text || '';
    textInput.addEventListener('input', collectPhoneEdits);
    textInput.dataset.choiceIndex = String(index);
    textInput.dataset.field = 'text';
    row.appendChild(textInput);

    const targetInput = document.createElement('input');
    targetInput.className = 'choice-target-input';
    targetInput.placeholder = 'target_scene';
    targetInput.value = choice.target || '';
    targetInput.addEventListener('input', collectPhoneEdits);
    targetInput.dataset.choiceIndex = String(index);
    targetInput.dataset.field = 'target';
    row.appendChild(targetInput);

    wrapper.appendChild(row);
  });

  const addBtn = document.createElement('button');
  addBtn.className = 'choice-btn add-choice-btn';
  addBtn.textContent = '+ Add option';
  addBtn.addEventListener('click', () => {
    collectPhoneEdits();
    currentStory.scenes[currentSceneId].choices.push({ text: '', target: '' });
    renderReader();
  });
  wrapper.appendChild(addBtn);

  container.appendChild(wrapper);
}

function renderChoices(container, choices) {
  if (isPhoneEditMode) {
    renderEditableChoices(container, choices);
    return;
  }

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
  if (isPhoneEditMode) {
    renderEditableChoices(container, []);
    return;
  }

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

function collectPhoneEdits() {
  if (!isPhoneEditMode || !currentStory || !currentSceneId) return;
  const scene = ensureSceneDefaults(currentStory.scenes[currentSceneId]);
  const titleInput = app.querySelector('.scene-title-input');
  const textInput = app.querySelector('.scene-text-input');
  if (titleInput) scene.title = titleInput.value;
  if (textInput) scene.text = textInput.value;

  const choiceRows = app.querySelectorAll('.phone-choice-row');
  const nextChoices = [];
  choiceRows.forEach((row) => {
    const text = row.querySelector('[data-field="text"]')?.value || '';
    const target = row.querySelector('[data-field="target"]')?.value || '';
    if (!text.trim() && !target.trim()) return;
    nextChoices.push({ text, target });
  });
  scene.choices = nextChoices;
  currentStory.scenes[currentSceneId] = scene;
}

function renderReader() {
  if (!currentSceneId) {
    renderEmptyStoryMessage();
    return;
  }

  const scene = ensureSceneDefaults(currentStory.scenes[currentSceneId]);
  currentStory.scenes[currentSceneId] = scene;

  app.innerHTML = '';
  const header = createReaderHeader();
  app.appendChild(header);

  const container = document.createElement('div');
  container.className = `scene${isPhoneEditMode ? ' scene-edit-mode' : ''}`;

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

  if (isPhoneEditMode) {
    renderEditableText(container, scene);
  } else {
    renderReadOnlyText(container, scene);
  }

  const sceneChoices = Array.isArray(scene.choices) ? scene.choices : [];
  if (sceneChoices.length === 0) {
    renderEnding(container);
  } else {
    renderChoices(container, sceneChoices);
  }

  app.appendChild(container);
}

function navigateTo(sceneId) {
  if (isPhoneEditMode) {
    collectPhoneEdits();
    saveCurrentStoryToLocal();
  }
  currentSceneId = sceneId;
  renderReader();
  window.scrollTo(0, 0);
}

async function startStory(slug) {
  try {
    currentStory = await fetchJSON(`data/stories/${slug}.json`);
    currentSceneId = resolveStartScene(currentStory);
    currentView = 'reader';
    isPhoneEditMode = false;
    if (!currentSceneId) {
      renderEmptyStoryMessage();
      return;
    }
    renderReader();
    window.scrollTo(0, 0);
  } catch (err) {
    console.error(err);
    app.innerHTML = '<p style="padding:2rem;text-align:center">Failed to load story.</p>';
  }
}

function startPhoneEditMode(catalog) {
  const stories = catalog?.stories || [];
  if (stories.length === 0) {
    app.innerHTML = '<p style="padding:2rem;text-align:center">No stories available for editing yet.</p>';
    return;
  }
  const firstSlug = stories[0].slug;
  loadStoryForPhoneEdit(firstSlug);
}

async function loadStoryForPhoneEdit(slug) {
  const localStory = loadStoryFromLocal(slug);
  if (localStory) {
    currentStory = localStory;
  } else {
    currentStory = await fetchJSON(`data/stories/${slug}.json`);
  }

  currentSceneId = resolveStartScene(currentStory);
  if (!currentSceneId) {
    const firstId = 'intro';
    currentStory.scenes[firstId] = ensureSceneDefaults({});
    currentStory.startScene = firstId;
    currentSceneId = firstId;
  }
  currentView = 'reader';
  isPhoneEditMode = true;
  renderReader();
}

async function goToLibrary() {
  if (isPhoneEditMode) {
    collectPhoneEdits();
    saveCurrentStoryToLocal();
  }
  currentStory = null;
  currentSceneId = null;
  currentView = 'library';
  isPhoneEditMode = false;
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

function toast(message) {
  let toastEl = document.getElementById('phone-edit-toast');
  if (!toastEl) {
    toastEl = document.createElement('div');
    toastEl.id = 'phone-edit-toast';
    toastEl.className = 'phone-edit-toast';
    document.body.appendChild(toastEl);
  }
  toastEl.textContent = message;
  toastEl.classList.add('show');
  window.setTimeout(() => toastEl.classList.remove('show'), 1400);
}

goToLibrary();
