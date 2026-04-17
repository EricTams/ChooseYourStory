# Character Art System

## Overview

Each scene in the game is illustrated by combining a **character description** with a **location description** and a shared **style prompt**. The character description stays consistent across scenes so the characters are always recognizable. The full prompt used to generate each image is saved alongside the output so it can be regenerated or tweaked later.

## Style

All art uses a **needle-felted wool** aesthetic: soft rounded forms, visible fiber texture, warm lighting, and slightly imperfect handcrafted charm. Characters and environments both follow this style.

**Style prompt fragment** (appended to every generation):

> needle-felted wool craft style, soft fuzzy fiber texture, warm lighting, handcrafted felt diorama, miniature scene, shallow depth of field

## Characters

### Penguin Wizard

| Trait | Description |
|---|---|
| Species | Emperor penguin, short and round |
| Outfit | Deep purple robe with silver star embroidery, pointed hat slightly too large |
| Accessories | Gnarled oak staff with a glowing blue crystal tip, leather satchel of scrolls |
| Expression | Wide curious eyes, determined beak |
| Distinguishing | Tiny spectacles perched on beak, robe hem singed from spell mishaps |

**Prompt fragment:**

> a small round emperor penguin wizard wearing a deep purple robe with silver star embroidery and an oversized pointed hat, tiny spectacles on its beak, carrying a gnarled oak staff with a glowing blue crystal tip, leather satchel of scrolls at its side, singed robe hem

### Cat Thief

| Trait | Description |
|---|---|
| Species | Sleek black cat, lean and agile |
| Outfit | Dark grey hooded cloak over a fitted leather vest, wrapped forearms |
| Accessories | Twin daggers strapped to lower back, belt of lockpicks and small pouches |
| Expression | Half-lidded confident eyes, sly grin |
| Distinguishing | Notched left ear, single gold earring on right ear, tail tip wrapped in dark cloth |

**Prompt fragment:**

> a sleek black cat thief in a dark grey hooded cloak over a fitted leather vest with wrapped forearms, twin daggers strapped to its back, belt of lockpicks and small pouches, half-lidded confident eyes, sly grin, notched left ear, single gold earring on the right ear, tail tip wrapped in dark cloth

### Bunny Archer

| Trait | Description |
|---|---|
| Species | Brown lop-eared rabbit, medium build |
| Outfit | Forest green tunic with a tan leather chest guard, arm bracer on the draw hand |
| Accessories | Carved shortbow slung across back, quiver of white-fletched arrows, herb pouch at hip |
| Expression | Alert upright posture, calm focused eyes |
| Distinguishing | One ear always flopped forward, small leaf-shaped birthmark on forehead, wrapped footpads |

**Prompt fragment:**

> a brown lop-eared rabbit archer in a forest green tunic with tan leather chest guard and arm bracer, carved shortbow across its back, quiver of white-fletched arrows, herb pouch at hip, calm focused eyes, one ear flopped forward, small leaf-shaped mark on forehead, wrapped footpads

## Locations

Location prompts describe the environment separately from the characters. Examples:

| Location | Prompt fragment |
|---|---|
| Crystal Cavern | inside a vast underground cavern filled with towering luminous crystals, underground river reflecting purple and blue light |
| Dragon's Peak | on a narrow mountain ridge above the clouds, ancient stone ruins and wind-torn banners, distant volcanic glow |
| Whispering Forest | in a dense enchanted forest with enormous twisted trees, glowing mushrooms, shafts of golden light through the canopy |
| Sunken Temple | inside a half-flooded stone temple overgrown with coral and kelp, shafts of light from cracks above, ancient mosaics on the walls |
| Thieves' Market | in a bustling underground market lit by hundreds of hanging lanterns, colorful tents and stalls carved into cavern walls |

## Prompt Assembly

A full prompt is built by concatenating three parts:

```
{character prompt fragment}, {location prompt fragment}, {style prompt fragment}
```

**Example — Penguin Wizard in the Crystal Cavern:**

> a small round emperor penguin wizard wearing a deep purple robe with silver star embroidery and an oversized pointed hat, tiny spectacles on its beak, carrying a gnarled oak staff with a glowing blue crystal tip, leather satchel of scrolls at its side, singed robe hem, inside a vast underground cavern filled with towering luminous crystals, underground river reflecting purple and blue light, needle-felted wool craft style, soft fuzzy fiber texture, warm lighting, handcrafted felt diorama, miniature scene, shallow depth of field

## Saving Prompts

Every generated image is saved with a companion `.json` file containing the full prompt and generation parameters, so the image can be reproduced or iterated on.

```
assets/art/scene_001.png
assets/art/scene_001.json
```

The JSON contains:

```json
{
  "character": "penguin_wizard",
  "location": "crystal_cavern",
  "prompt": "<full assembled prompt>",
  "provider": "openai",
  "model": "gpt-image-1.5",
  "size": "1536x1024",
  "quality": "high",
  "seed": null,
  "generated_at": "2026-03-31T12:00:00Z"
}
```

This makes it easy to regenerate with a different provider, tweak a description, or batch-produce variants.
