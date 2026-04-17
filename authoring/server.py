import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

from flask import Flask, render_template, request, jsonify, send_from_directory

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_DIR = os.path.join(PROJECT_ROOT, 'game')
DATA_DIR = os.path.join(GAME_DIR, 'data')
STORIES_DIR = os.path.join(DATA_DIR, 'stories')
ART_DIR = os.path.join(GAME_DIR, 'assets', 'art')
CATALOG_PATH = os.path.join(DATA_DIR, 'catalog.json')
IMAGINE_SCRIPT = os.path.join(PROJECT_ROOT, 'Imagine', 'imagine.py')

IMAGE_SIZE = '1536x1024'
IMAGE_QUALITY = 'medium'
ART_GENERATION_TIMEOUT_SEC = 120

STYLE_PROMPT = (
    "needle-felted wool craft style, soft fuzzy fiber texture, warm lighting, "
    "handcrafted felt diorama, miniature scene, shallow depth of field"
)

CHARACTERS = {
    "penguin_wizard": {
        "name": "Penguin Wizard",
        "prompt": (
            "a small round emperor penguin wizard wearing a deep purple robe "
            "with silver star embroidery and an oversized pointed hat, tiny "
            "spectacles on its beak, carrying a gnarled oak staff with a "
            "glowing blue crystal tip, leather satchel of scrolls at its "
            "side, singed robe hem"
        ),
    },
    "cat_thief": {
        "name": "Cat Thief",
        "prompt": (
            "a sleek black cat thief in a dark grey hooded cloak over a "
            "fitted leather vest with wrapped forearms, twin daggers strapped "
            "to its back, belt of lockpicks and small pouches, half-lidded "
            "confident eyes, sly grin, notched left ear, single gold earring "
            "on the right ear, tail tip wrapped in dark cloth"
        ),
    },
    "bunny_archer": {
        "name": "Bunny Archer",
        "prompt": (
            "a brown lop-eared rabbit archer in a forest green tunic with "
            "tan leather chest guard and arm bracer, carved shortbow across "
            "its back, quiver of white-fletched arrows, herb pouch at hip, "
            "calm focused eyes, one ear flopped forward, small leaf-shaped "
            "mark on forehead, wrapped footpads"
        ),
    },
}

LOCATIONS = {
    "crystal_cavern": {
        "name": "Crystal Cavern",
        "prompt": (
            "inside a vast underground cavern filled with towering luminous "
            "crystals, underground river reflecting purple and blue light"
        ),
    },
    "dragons_peak": {
        "name": "Dragon's Peak",
        "prompt": (
            "on a narrow mountain ridge above the clouds, ancient stone "
            "ruins and wind-torn banners, distant volcanic glow"
        ),
    },
    "whispering_forest": {
        "name": "Whispering Forest",
        "prompt": (
            "in a dense enchanted forest with enormous twisted trees, "
            "glowing mushrooms, shafts of golden light through the canopy"
        ),
    },
    "sunken_temple": {
        "name": "Sunken Temple",
        "prompt": (
            "inside a half-flooded stone temple overgrown with coral and "
            "kelp, shafts of light from cracks above, ancient mosaics on "
            "the walls"
        ),
    },
    "thieves_market": {
        "name": "Thieves' Market",
        "prompt": (
            "in a bustling underground market lit by hundreds of hanging "
            "lanterns, colorful tents and stalls carved into cavern walls"
        ),
    },
}

app = Flask(__name__)


# ── Helpers ──────────────────────────────────────────────────────────

def slugify(title):
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def load_catalog():
    if not os.path.exists(CATALOG_PATH):
        return {"stories": []}
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_catalog(catalog):
    os.makedirs(os.path.dirname(CATALOG_PATH), exist_ok=True)
    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2)


def load_story(slug):
    path = os.path.join(STORIES_DIR, f'{slug}.json')
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_story(story):
    os.makedirs(STORIES_DIR, exist_ok=True)
    path = os.path.join(STORIES_DIR, f'{story["slug"]}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(story, f, indent=2)


def art_config():
    return {
        "stylePrompt": STYLE_PROMPT,
        "characters": CHARACTERS,
        "locations": LOCATIONS,
    }


# ── Pages ────────────────────────────────────────────────────────────

@app.route('/')
def library_page():
    catalog = load_catalog()
    return render_template('library.html', catalog=catalog)


@app.route('/stories/<slug>')
def editor_page(slug):
    story = load_story(slug)
    if not story:
        return "Story not found", 404
    catalog = load_catalog()
    summary = ''
    for entry in catalog['stories']:
        if entry['slug'] == slug:
            summary = entry.get('summary', '')
            break
    return render_template(
        'editor.html',
        story=story,
        summary=summary,
        art_config=art_config(),
    )


# ── API ──────────────────────────────────────────────────────────────

@app.route('/api/stories', methods=['POST'])
def create_story():
    data = request.get_json()
    title = data.get('title', '').strip()
    if not title:
        return jsonify({"error": "Title is required"}), 400

    slug = slugify(title)
    catalog = load_catalog()

    if any(s['slug'] == slug for s in catalog['stories']):
        return jsonify({"error": "A story with that name already exists"}), 409

    story = {"slug": slug, "title": title, "startScene": "", "scenes": {}}
    save_story(story)

    os.makedirs(os.path.join(ART_DIR, slug), exist_ok=True)

    catalog['stories'].append({
        "slug": slug,
        "title": title,
        "cover": f"assets/art/{slug}/cover.png",
        "summary": "",
    })
    save_catalog(catalog)

    return jsonify({"slug": slug})


@app.route('/api/stories/<slug>', methods=['POST'])
def update_story(slug):
    data = request.get_json()
    data['slug'] = slug
    save_story(data)

    catalog = load_catalog()
    for entry in catalog['stories']:
        if entry['slug'] == slug:
            entry['title'] = data.get('title', entry['title'])
            if 'summary' in data:
                entry['summary'] = data['summary']
            break
    save_catalog(catalog)

    return jsonify({"ok": True})


@app.route('/api/stories/<slug>/generate-art', methods=['POST'])
def generate_art(slug):
    data = request.get_json()
    scene_id = data.get('scene_id')
    prompt = data.get('prompt', '')
    provider = data.get('provider', 'openai')

    if not scene_id or not prompt:
        return jsonify({"error": "scene_id and prompt are required"}), 400

    slug_art_dir = os.path.join(ART_DIR, slug)
    os.makedirs(slug_art_dir, exist_ok=True)

    filename = f'scene_{scene_id}.png'
    output_path = os.path.join(slug_art_dir, filename)
    image_rel = f'assets/art/{slug}/{filename}'

    cmd = [
        sys.executable, IMAGINE_SCRIPT,
        'generate', prompt, output_path,
        '--size', IMAGE_SIZE,
        '--quality', IMAGE_QUALITY,
        '--provider', provider,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=ART_GENERATION_TIMEOUT_SEC,
        )
        if result.returncode != 0:
            return jsonify({"error": result.stderr or "Generation failed"}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Image generation timed out"}), 504

    metadata = {
        "character": data.get('character', 'custom'),
        "location": data.get('location', 'custom'),
        "prompt": prompt,
        "provider": provider,
        "size": IMAGE_SIZE,
        "quality": IMAGE_QUALITY,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    meta_path = os.path.join(slug_art_dir, f'scene_{scene_id}.json')
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    story = load_story(slug)
    if story and scene_id in story['scenes']:
        story['scenes'][scene_id]['image'] = image_rel
        save_story(story)

    return jsonify({"image": image_rel})


# ── Static game files (preview) ─────────────────────────────────────

@app.route('/game/<path:path>')
def serve_game(path):
    return send_from_directory(GAME_DIR, path)


# ── Main ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    os.makedirs(STORIES_DIR, exist_ok=True)
    os.makedirs(ART_DIR, exist_ok=True)
    print(f"Project root : {PROJECT_ROOT}")
    print(f"Game dir     : {GAME_DIR}")
    print(f"Preview at   : http://localhost:5000/game/index.html")
    print()
    app.run(debug=True, port=5000)
