# Tech Stack

## Platform

| Layer | Choice | Notes |
|---|---|---|
| Game player | Static HTML / CSS / vanilla JS | No frameworks, no bundler, no transpiler. The `game/` folder is deployable as-is. |
| Authoring tool | Python local HTTP server | Runs on the author's machine only. Needs filesystem access and the ability to shell out to `imagine.py`. |
| Image generation | `Imagine/imagine.py` (existing) | Supports OpenAI, BFL, and fal.ai providers. Called by the authoring server. |
| Hosting | GitHub Pages | Serves the `game/` folder as a static site. |

## Languages

- **JavaScript (ES modules)** -- game engine, no transpilation
- **CSS** -- plain CSS, no preprocessor
- **HTML** -- single `index.html` entry point
- **Python 3.10+** -- authoring server (local only, not deployed)

## Game Player

The player is a single-page app driven entirely by JSON data.

- One `index.html` with a `<script type="module">` entry point
- `game/js/game.js` -- loads data, manages navigation state, renders screens
- `game/css/style.css` -- all visual styling
- Data fetched at runtime via `fetch()` from `game/data/`

No third-party JS libraries. No CSS frameworks.

## Authoring Server

A lightweight Python HTTP server for local use only.

| Concern | Approach |
|---|---|
| HTTP framework | Flask (minimal routes, simple templates) |
| Data persistence | Read/write JSON files directly to `game/data/` |
| Image generation | Subprocess call to `Imagine/imagine.py` |
| Art storage | Images saved to `game/assets/art/{story-slug}/` |

The authoring server is never deployed. It exists solely to provide a local UI for writing scenes and generating art.

### Python dependencies (authoring only)

- `flask` -- HTTP server

All other dependencies (openai, Pillow, requests, etc.) are already required by `imagine.py`.

## Data Format

All game data is plain JSON. No database.

- `game/data/catalog.json` -- story index (slug, title, cover, summary)
- `game/data/stories/{slug}.json` -- one file per story, contains all scenes
- `game/assets/art/{slug}/` -- scene images (PNG), one folder per story

See [design.md](design.md) for full schemas.

## Deployment

| Setting | Value |
|---|---|
| Hosting | GitHub Pages |
| Source | `game/` folder on `main` branch |
| Build step | None -- static files served directly |
| Custom domain | Optional, not required |

The `authoring/` and `Imagine/` directories are not deployed. Only the `game/` folder is public.

## Constraints

- No server-side code at runtime. The deployed game is purely static.
- No build tools (webpack, vite, etc.). Files are authored and served directly.
- All game state lives in the browser session (JS variables). No persistence of player progress across page reloads (can be added later if needed).
- Images are pre-generated during authoring, not created at runtime.
