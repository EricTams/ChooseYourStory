# Story Authoring Workflow

Workflow for refining CYOA story rooms and generating scene art. This is the process developed on `stormy-the-archer-intro` — use that story as the reference implementation.

Start with [Writing targets](#writing-targets) and the sequence review below when writing or evaluating a story.

When working on story JSON, proceed in small reviewable steps. Do not jump ahead to image generation before text and metadata are approved.

## JSON shape

Each story JSON (`game/data/stories/<slug>.json`) has top-level `artStyle`, `characters`, `locations`, and `items` blocks. `characters` and `items` are the registry — every recurring character and item lives there as a stable entry that scene descriptions and reference images both pull from.

```json
"characters": {
  "stormy": {
    "description": "A grey rabbit archer wearing a green cloak and carrying a wooden bow.",
    "referenceImage": "data/stories/<slug>/_refs/stormy.png"
  }
},
"items": {
  "skeleton_key": {
    "description": "A small iron skeleton key with a moon-and-door symbol carved into the handle.",
    "referenceImage": "data/stories/<slug>/_refs/skeleton_key.png"
  }
}
```

Items go in the registry when they recur or carry plot weight (key, cart, lantern). One-off props and crowds stay inside scene descriptions.

`referenceImage` paths are runtime-relative (same convention as the `image:` field on scenes), since the game serves from `game/`.

## File layout

Reference images live in a `_refs/` subfolder of the story slug folder, alongside scene images:

```
game/data/stories/<slug>/
  _refs/
    stormy.png
    skeleton_key.png
    ...
  gearing_up.png
  ...
```

`_refs/` stays PNG forever (author-only, never served). Scene images are generated as PNG and converted to WebP by the optimize step at the end.

## Reusable location references and movable props

Location references establish permanent architecture and normal furnishings. Keep scene-specific luggage, laundry carts, trap materials, damage, and mess out of the base view. Add those explicitly in each scene's description. A reusable prop that needs visual continuity gets its own item registry entry and reference; specify its contents and position per scene. Keep earlier dressed location concepts as variants, and point the location registry at the clean base. Fixed classroom apparatus may remain in a normal classroom reference, but specify any later removal or rearrangement.

## Image generation tool

Every image is produced by `scripts/generate-image.mjs`, which calls OpenAI GPT Image 2 (`OPENAI_API_KEY` must be set in the environment):

```
node scripts/generate-image.mjs \
  --prompt-file /path/to/prompt.txt \
  --ref game/data/stories/<slug>/_refs/stormy.png \
  --ref game/data/stories/<slug>/_refs/teacher.png \
  --out game/data/stories/<slug>/<scene_id>.png
```

- `--prompt` / `--prompt-file` — the scene's `LLMImageDescription` prose. Use `--prompt-file` for scene prompts (they are long); write the prompt to a temp file first.
- `--ref` — repeatable, one per reference image, **order matters** (see below). Omit entirely when generating a reference image itself. Paths are repo-relative or absolute.
- `--out` — final destination path. The tool writes directly into the story folder; there is no copy step.
- Defaults: `--size 1536x1024`, `--quality high`, `--model gpt-image-2`. Reference images and scenes both use the landscape default.
- With no `--ref`, the tool uses the generations endpoint; with refs, the edits endpoint, passing the refs as input images in the given order.
- If characters drift from their references, retry with `--input-fidelity high`.

**Reference images are unlabeled.** The refs are a flat ordered list — the API does not tag which file is which character. The prompt must map every reference to an entity by **order** and **name**, and assign each pose to the correct entity. Without this, multi-character scenes often swap roles (e.g. the teacher running the course instead of Stormy).

**Reference order when calling the tool:**
1. The protagonist first whenever they appear (Stormy in the Stormy story)
2. Other characters alphabetically by registry id (`jerboa`, `rival`, `sister`, `teacher`)
3. Items alphabetically by registry id (`lantern`, `skeleton_key`, `tonic_cart`)

**In `LLMImageDescription`, after the location block, state the order explicitly:**
"Reference images are provided in this order: first Stormy, second the teacher."

**For each character or item with a reference, tie it to that slot before the registry description:**
"Stormy, matching the first reference image — A grey rabbit archer wearing a green cloak… — crouches at the starting line…"

**When two characters share a similar pose or could be swapped, add a disambiguation line:**
"Stormy alone crouches at the starting line; the teacher watches from the background only. Do not swap their roles or poses."

## Writing targets

These targets apply across stories. Review the whole sequence as well as the individual sentences.

1. **Give the reader someone to care about.** Establish what the character wants, why it matters to them, and what they hope will happen next. Introduce personality through actions, expectations, and dialogue rather than a list of traits.
2. **Let pictures show events and text explain their emotional meaning.** Illustrations carry setting, expressions, physical action, and visual humour. Text supplies thoughts, feelings, dialogue, timing, and any explanation needed to understand events. Some overlap is worthwhile when it makes the story clearer.
3. **Make cause and effect understandable.** The reader should understand how an action produces its result. Surprises can be unexpected, but they should make sense afterward. Neither text nor illustration should require the reader to invent a missing connection.
4. **Give the reader a real decision.** Establish the situation and relevant clues before offering choices. Do not have the character already commit to an option, or show its outcome, before the reader chooses. Choices should describe understandable actions.
5. **Give every meaningful choice a satisfying result.** Show what happened and allow the character to react before moving to the next challenge. Success deserves attention as much as failure. Retry scenes should make the mistake understandable and return the reader to a useful decision.
6. **Let strengths and flaws affect events.** Characters should contribute to their successes and difficulties through their behaviour. Their feelings can be stated directly; judgments about their character and the story's moral should emerge from what happens.
7. **Use clear, warm language.** Trying to sound clever is an explicit anti-goal. Humour should come from situations and character reactions. Remove confusing quips, but preserve excitement, disappointment, affection, and anticipation. Brevity should not make the prose mechanical.
8. **Keep the action simple enough to depict consistently.** Use only the physical details needed to understand the scene. Establish important objects and relationships before relying on them, and preserve them across outcomes. Simplify a confusing setup before adding explanations or repairing individual pictures.

## Text and image share the storytelling

**The images show us what is happening. The text explains the emotions and describes what happens when required.**

Direct emotional language and dialogue are welcome. A visible expression does not replace understanding what the character wants, hopes, fears, or expects. Avoid retelling an already clear picture, but retain action and explanation needed to follow events or make a fair choice. Do not turn this division of labour into a rigid ban on overlap.

Plan the illustration, narrative, and choices together before generating art. A text-only preview is incomplete by design; do not fill a missing illustration with descriptive narration. The reader sees the image above the text, so its moment must agree with what has and has not happened yet.

### Plan the sequence before polishing the screens

Outline the setup, available actions, and every outcome together. Identify who acts, what causes any movement or change, and which established objects make each outcome possible. Story logic can be playful or fantastical, but it must remain consistent with what the reader has been shown.

Each meaningful choice needs a clear consequence before a new challenge begins. A separate result screen can confirm the outcome and give the character time to react. Routine continuation buttons do not require additional result screens. Do not undermine a successful choice merely to demonstrate a character flaw or force the plot forward.

### Make a screen card before writing prose

Keep these short notes in the working outline or review document, not in player-facing text:

| Note | Question to answer |
|---|---|
| Story beat | What changes for the character or reader on this screen? |
| Emotional context | What does the character want, expect, or feel, and why does this moment matter? |
| Picture tells | What single visible moment supplies the action, setting, relationship, clue, or visual joke? |
| Words add | What feeling, dialogue, timing, intention, or explanation does the reader need beyond the picture? |
| Choice needs | What must the reader understand before deciding? Has the decision been left to them? |
| Cause and consequence | What established action causes this result, and what remains consistent across the sequence? |

Draft `imageDescription` and `text` together from this card. Do not finish a standalone prose scene and attach an illustration summary afterward.

### Review the sequence, then the sentences

Review the setup, every choice, and each outcome together, with text, buttons, and illustration descriptions side by side. Repeat the review against the actual illustrations after generation.

- What does the character want, and how do they feel?
- What can the reader reasonably understand and choose?
- Does each result follow from that choice, using the situation already established?
- Do the words and pictures agree about the action, objects, participants, and timing?
- Have we given the result and the character's reaction enough room to matter?

If the sequence fails these checks, revise its setup or action before polishing sentences or repeatedly patching individual images. A prompt describing the intended mechanism is not evidence that the generated image shows it.

Then edit sentences for contribution. Keep language that supplies emotional context, character, cause, timing, a clue, or necessary orientation. Remove redundant visual description, explanations of an already clear joke, and narrator asides whose main purpose is to sound clever. Make speakers and pronouns unambiguous. Do not remove warmth or useful causal facts merely to shorten a page.

Check word counts after meaning and pacing. Length targets guide readability; they are not quotas. Do not pad a short effective scene or rush a meaningful result to meet a target. Accessibility descriptions, when supported, belong in a separate channel rather than being used as narrative paragraphs.

## Workflow

1. **Plan the picture and refine room text together, before generating art.**
   - Use the screen card and sequence review in **Text and image share the storytelling** above for every room and branch. Begin `imageDescription` here, alongside `text`; do not defer the visual beat until the prose is finished.
   - Match the existing kid-readable style: concrete action, simple emotions, short present-tense story beats.
   - For joke/fail rooms, let the image carry the visual gag. Text should advance the action, realization, or emotion rather than literally describing the funny picture.
   - Fail-room return targets: loop back to the nearest decision point by default. Returning further back is fine when the replayed stretch still has branching choices ahead of it — what's not OK is forcing a re-walk through choice-less corridor scenes, or a return label that contradicts its destination.
   - Multi-choice rooms should always contain a winnable option — never a room where every choice fails.
   - Check length. Split rooms when a beat contains both setup and punchline, or when one image cannot represent the whole moment clearly.

2. **Lock the registry.**
   - Finalize every recurring character and item in `characters` and `items` before generating any images.
   - Each entry has a stable id (the JSON key) and a `description` clear enough that someone could draw it without guessing.
   - Refer to each entity by the same name in every later description (always "Stormy", never "the rabbit") — the registry's `description` is the single source of truth for that wording.

3. **Generate one reference image per registry entry.**
   - Done before any scene-level work, so the references are settled when scene descriptions get written.
   - For each entry, the prompt is the story's `artStyle` preamble pasted verbatim, plus the registry `description`, plus enough framing to keep the image clean (entity alone on a plain backdrop, full body or full object visible, no props or scenery).
   - Run the tool with no `--ref` args and `--out game/data/stories/<slug>/_refs/<id>.png`, then set `referenceImage` on the registry entry.
   - Show each reference to the user for approval. If the reference looks off (outfit, proportions, marks), regenerate before continuing — every later scene inherits this.

4. **Finalize the short `imageDescription` fields drafted with the text.**
   - Compact and human-readable: pose, emotion, composition, and the visual beat.
   - Do not overload these with full character designs, art style, or setting detail. Those belong in `LLMImageDescription`.
   - Each scene gets its own image; do not plan to reuse images between rooms.

5. **Compose `LLMImageDescription` from registry pieces.**
   - Build the scene's description by pasting registry pieces together into one continuous block of prose, in this order:
     - The story's `artStyle` preamble verbatim.
     - The scene's `locations[location].description` verbatim.
     - If the scene uses reference images, one sentence listing reference order (see **Reference images are unlabeled** above).
     - For each character and item present in the scene, an explicit reference tie ("Stormy, matching the first reference image —"), then the registry `description` verbatim, then scene-specific action, pose, expression, and visible state.
     - Layout in natural language ("left foreground", "between them", "in the background").
     - Role disambiguation when two characters could be swapped (who performs the main action, who watches only).
     - Scene-specific lighting and mood.
     - Any deliberate deviation from a reference image, called out explicitly (e.g. "Stormy is upside-down in the dirt with steam curling from his ears, cloak rumpled — outfit and proportions otherwise match the first reference"). Without this, the model has to guess whether the deviation is intentional and may drift the rest of the entity.
   - The prose has no labelled sections in the actual text — no "Subject:" or "Style:" headers.

6. **Generate scene images one scene at a time unless the user asks for a batch.**
   - Write the scene's `LLMImageDescription` to a temp file and run the tool with:
     - `--prompt-file` pointing at it.
     - `--ref` for every character and item present in the scene that has a `referenceImage` in the registry, in the fixed order above.
     - `--out game/data/stories/<slug>/<scene_id>.png`.
   - After acceptance: add `"image": "data/stories/<slug>/<scene_id>.png"` to the scene, validate JSON, confirm the file exists.

7. **Optimize before shipping.**
   - Run `npm run optimize-images` (optionally `--story=<slug>`). It resizes to max 1440px wide, converts scene PNGs and the cover to WebP, rewrites `image`/cover paths in the story JSON and catalog, and moves originals to `_originals/`. It leaves `_refs/` untouched.

## Keep recurring sets simple

Only make a set detail prominent when it supports a choice, a joke, character, or a later payoff. Prefer ordinary floors and a few recognizable landmarks over decorative tracks, elaborate machinery, or complicated routes that must match across many pictures.

For consecutive scenes in one room, edit from the established scene when possible. Preserve the permanent layout while changing the action. Keep the camera stable when that helps comparison; a new angle or closer framing must still show consistent spatial relationships. Compare the setup, retry, and success images together before treating the sequence as finished: equipment height relative to characters, doors and windows, fixed props, and any decision clue must agree. Adjust the pose to fit the equipment; never stretch the set to fit a gag.

Story-specific staging decisions belong in that story’s planning documents, not in this general guide.

## Worked example

`town_arrival` features Stormy, the rat, the jerboa, and the tonic cart, plus an unnamed crowd. The crowd does not go in the registry — they do not recur and do not need cross-scene consistency.

- `--ref` order: `stormy.png`, `jerboa.png`, `rat.png`, `tonic_cart.png`.
- The prompt opens with the story's `artStyle` preamble; then the `town_square` location description; "Reference images are provided in this order: first Stormy, second the jerboa, third the rat, fourth the tonic cart."; each entity tied to its slot plus registry description and scene action ("Stormy, matching the first reference image — … — stands at the edge of the crowd on the left…"; "the rat, matching the third reference image — … — beside the cart in the center holds out a tiny tonic bottle…"; etc.); a one-line note about a soft secondary crowd; lighting; and a constraints line stating no deliberate deviations from the references.
