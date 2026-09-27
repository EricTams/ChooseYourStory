# ChooseYourStory documentation

ChooseYourStory is a choose-your-own-adventure story game. Stories are JSON files in `game/data/stories/`, served statically from `game/`. Illustrations use a handmade needle-felted wool style.

Project guidance lives here as ordinary Markdown, independent of any editor or assistant.

## Start here

- [Story authoring](story-authoring.md): the current workflow for screen writing, choices and retries, character/item registries, references, scene art, and image optimization. Start with **Writing targets** and review the setup, choices, and outcomes together.
- [Development guidelines](development.md): coding conventions, state management, error handling, verification, and portable tooling.
- [Game design](design.md): library and reader behavior, navigation, and basic story schemas. Its original image-generation workflow is historical; use the story-authoring guide for current art work.
- [Tech stack](tech-stack.md): static player, local authoring server, and project structure. Legacy authoring-server integrations are identified separately from current story-art tooling.
- [Earlier character-art system](character-art.md): superseded historical documentation, retained for reference.

## Authoring essentials

The images show what is happening. The text explains the emotions and describes action when needed. Establish what the character wants and why it matters. Use clear, warm language; trying to sound clever is an explicit anti-goal.

Plan pictures, prose, and choices together. Review each setup and all its outcomes as a sequence: choices must remain open to the reader, results must follow understandable causes, and every meaningful choice deserves a consequence and reaction. Keep physical details simple and consistent. Use the [writing targets and sequence review](story-authoring.md#writing-targets), then edit sentences and check length.

Text and metadata are reviewed before scene art. Recurring characters and items have stable registry entries and reference images in each story's `_refs/` folder. Stormy is the reference implementation of the registry workflow. The story-authoring guide documents the repository image-generation script and WebP optimization step.

## Razzy and the Buried Secret

- [Act One roadmap](razzy/act-one-roadmap.md): the planning baseline, screen routes, setup/payoff ledger, and required references.
- [Act One script](razzy/act-one-script.md): readable copy of the playable text draft, with choices and illustration descriptions.
- [Act Two opening script](razzy/act-two-script.md): playable opening, choice results and scene art.
- [Act Two reference art](razzy/act-two-reference-art.md): eight location and prop references, with prompts and continuity notes.
- [Text-length audit](razzy/act-one-length-audit.md): page counts and results of the tightening pass.

The playable story JSON is the source of truth for implemented text and choices. Keep its review script and audit in sync when editing. Roadmap proposals are planning context and may be superseded by reviewed implementation changes.
