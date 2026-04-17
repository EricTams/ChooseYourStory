# Game Design

## Overview

A choose-your-own-adventure (CYOA) book game. The player picks a story from a library, reads scene-by-scene, and makes choices that determine where the story goes. Each scene has an illustration, narrative text, and one or more choices (or none, marking an ending).

The game ships as a static site. Stories are authored offline using a local Python server and the `imagine.py` image generation tool.

## Player Screens

### Library Screen

Displayed on page load. Shows all available stories as a grid of cards.

Each card shows:
- Cover image
- Title
- Short summary

Clicking a card loads that story and transitions to the reader.

### Reader Screen

Displays the current scene of the chosen story.

Layout (top to bottom):
1. **Story title** (persistent header, clickable to return to library)
2. **Scene image** (wide, prominent)
3. **Scene title**
4. **Narrative text**
5. **Choices** -- a list of buttons, one per option

Clicking a choice button navigates to the target scene.

### Ending Screen

When a scene has no choices, the story is over. The reader shows:
1. The final scene image and text (same as any scene)
2. An "The End" marker
3. A button to return to the library

## Navigation State

The game tracks three values in JS:
- `currentView` -- `"library"` or `"reader"`
- `currentStory` -- the loaded story object (or `null`)
- `currentSceneId` -- the active scene id within the story (or `null`)

State flows one way: user action -> state update -> render. The render function reads state and rebuilds the visible screen.

## Data Schemas

### catalog.json

Lives at `game/data/catalog.json`. Lists every published story.

```json
{
  "stories": [
    {
      "slug": "crystal-quest",
      "title": "The Crystal Quest",
      "cover": "assets/art/crystal-quest/cover.png",
      "summary": "Pip the penguin wizard ventures into the Crystal Cavern to recover a stolen artifact."
    }
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `slug` | string | URL-safe identifier, matches the story filename and art folder |
| `title` | string | Display title |
| `cover` | string | Path to cover image relative to `game/` |
| `summary` | string | One or two sentences shown on the library card |

### stories/{slug}.json

One file per story at `game/data/stories/{slug}.json`.

```json
{
  "slug": "crystal-quest",
  "title": "The Crystal Quest",
  "startScene": "intro",
  "scenes": {
    "intro": {
      "title": "The Journey Begins",
      "text": "Pip adjusts his spectacles and peers into the dark cavern ahead. The air is cold and smells of damp stone. Faint blue light pulses from somewhere deep below.",
      "image": "assets/art/crystal-quest/scene_intro.png",
      "choices": [
        { "text": "Enter the cavern", "target": "cavern_entrance" },
        { "text": "Search for another path", "target": "forest_path" }
      ]
    },
    "cavern_entrance": {
      "title": "Into the Deep",
      "text": "The passage narrows...",
      "image": "assets/art/crystal-quest/scene_cavern_entrance.png",
      "choices": []
    }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `slug` | string | Matches catalog entry and folder name |
| `title` | string | Story title |
| `startScene` | string | Scene id to show first |
| `scenes` | object | Map of scene id to scene object |

**Scene object:**

| Field | Type | Description |
|---|---|---|
| `title` | string | Scene heading |
| `text` | string | Narrative text (plain text, may contain newlines) |
| `image` | string | Path to scene image relative to `game/` |
| `choices` | array | List of choice objects. Empty array = ending. |

**Choice object:**

| Field | Type | Description |
|---|---|---|
| `text` | string | Button label shown to the player |
| `target` | string | Scene id to navigate to |

## Directory Layout

```
game/
  index.html
  css/
    style.css
  js/
    game.js
  data/
    catalog.json
    stories/
      crystal-quest.json
  assets/
    art/
      crystal-quest/
        cover.png
        scene_intro.png
        scene_intro.json
        scene_cavern_entrance.png
        scene_cavern_entrance.json
```

Art metadata JSON files (the `.json` companions to each `.png`) follow the format defined in [character-art.md](character-art.md). They record the full prompt and generation parameters so images can be reproduced.

## Authoring Workflow

All authoring happens locally via the authoring server (`authoring/server.py`).

### Creating a new story

1. Author provides a title (slug is derived automatically).
2. Server creates `game/data/stories/{slug}.json` with an empty scene map.
3. Server creates `game/assets/art/{slug}/` directory.
4. Server adds an entry to `game/data/catalog.json`.

### Editing scenes

1. Author picks a story from the authoring UI.
2. Author adds/edits scenes: title, narrative text, choices, image settings.
3. Server writes changes to `game/data/stories/{slug}.json`.

### Generating scene art

1. Author selects a character and location for the scene (from the prompts in [character-art.md](character-art.md)), or writes a custom prompt.
2. Server calls `imagine.py generate` with the assembled prompt.
3. Image is saved to `game/assets/art/{slug}/{scene_id}.png`.
4. Prompt metadata is saved to `game/assets/art/{slug}/{scene_id}.json`.
5. The scene's `image` field in the story JSON is updated automatically.

### Previewing

The authoring server can serve the `game/` folder so the author can play through the story in a browser during development.

## Art Pipeline

Art generation follows the system defined in [character-art.md](character-art.md):

1. Pick a **character prompt fragment** (Pip, Mika, Hazel, or custom).
2. Pick a **location prompt fragment** (Crystal Cavern, Dragon's Peak, etc., or custom).
3. Append the **style prompt fragment** (needle-felted wool aesthetic).
4. Concatenate: `{character}, {location}, {style}`.
5. Pass the assembled prompt to `imagine.py generate`.

Cover images follow the same pipeline but may use a wider composition or multiple characters.

## Deployment

1. Push the repo to GitHub.
2. Configure GitHub Pages to serve from the `game/` folder on the `main` branch.
3. Only the contents of `game/` are public. The `authoring/`, `Imagine/`, and `docs/` directories are in the repo but not served.
