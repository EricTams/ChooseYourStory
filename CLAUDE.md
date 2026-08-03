# ChooseYourStory

A choose-your-own-adventure story game. Stories are JSON files in `game/data/stories/`, served statically from `game/`. Scene art is AI-generated in a needle-felted wool style.

## Story authoring and image generation

When creating or editing stories, or generating any story art, follow `docs/story-authoring.md`. Key points:

- Story text is refined and approved before any image work.
- Recurring characters/items live in the story JSON's `characters`/`items` registry, each with a reference image in `_refs/`.
- All images are generated with `node scripts/generate-image.mjs` (GPT Image 2; needs `OPENAI_API_KEY`). Scene images pass the registry reference images via ordered `--ref` args.
- `stormy-the-archer-intro` is the reference implementation of this process.
- Before shipping, run `npm run optimize-images` to convert scene art to WebP.

`docs/character-art.md` describes a superseded earlier system — do not follow it.
