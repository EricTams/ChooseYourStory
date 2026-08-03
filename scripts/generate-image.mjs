#!/usr/bin/env node
// Generate story art with OpenAI's GPT Image 2.
//
// Two modes, picked automatically:
//   - No --ref args  -> POST /v1/images/generations  (used for registry reference images)
//   - One+ --ref args -> POST /v1/images/edits        (used for scene images; the refs are
//     passed as input images IN ORDER, so the prompt's "first reference image, second
//     reference image..." sentences line up with the files given here)
//
// Usage:
//   node scripts/generate-image.mjs --prompt "..." --out game/data/stories/<slug>/_refs/stormy.png
//   node scripts/generate-image.mjs --prompt-file /path/to/prompt.txt \
//     --ref game/data/stories/<slug>/_refs/stormy.png \
//     --ref game/data/stories/<slug>/_refs/teacher.png \
//     --out game/data/stories/<slug>/gearing_up.png
//
// Options:
//   --prompt "<text>"        prompt text inline
//   --prompt-file <path>     read prompt from a file (use for long scene prompts)
//   --out <path>             output image path; directories are created as needed
//   --ref <path>             reference image, repeatable, ORDER MATTERS (edits mode)
//   --size <WxH|auto>        default 1536x1024
//   --quality <low|medium|high|auto>   default high
//   --model <id>             default gpt-image-2
//   --input-fidelity <low|high>        edits mode only; omitted from the request unless set.
//                            Try --input-fidelity high if characters drift from their refs.
//
// Requires OPENAI_API_KEY in the environment.

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

function parseArgs(argv) {
  const opts = {
    prompt: null,
    promptFile: null,
    out: null,
    refs: [],
    size: '1536x1024',
    quality: 'high',
    model: 'gpt-image-2',
    inputFidelity: null,
  };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) throw new Error(`Missing value for ${arg}`);
      return argv[++i];
    };
    switch (arg) {
      case '--prompt': opts.prompt = next(); break;
      case '--prompt-file': opts.promptFile = next(); break;
      case '--out': opts.out = next(); break;
      case '--ref': opts.refs.push(next()); break;
      case '--size': opts.size = next(); break;
      case '--quality': opts.quality = next(); break;
      case '--model': opts.model = next(); break;
      case '--input-fidelity': opts.inputFidelity = next(); break;
      default: throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return opts;
}

function mimeFor(file) {
  const ext = path.extname(file).toLowerCase();
  if (ext === '.png') return 'image/png';
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
  if (ext === '.webp') return 'image/webp';
  throw new Error(`Unsupported reference image type: ${file}`);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error('OPENAI_API_KEY is not set');
  if (!opts.out) throw new Error('--out is required');
  if (!opts.prompt && !opts.promptFile) throw new Error('Provide --prompt or --prompt-file');
  if (opts.prompt && opts.promptFile) throw new Error('Use only one of --prompt / --prompt-file');

  const prompt = (opts.prompt ?? (await readFile(opts.promptFile, 'utf8'))).trim();
  if (!prompt) throw new Error('Prompt is empty');

  const headers = { Authorization: `Bearer ${apiKey}` };
  let response;

  if (opts.refs.length === 0) {
    response = await fetch('https://api.openai.com/v1/images/generations', {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: opts.model,
        prompt,
        size: opts.size,
        quality: opts.quality,
        output_format: 'png',
        moderation: 'low',
        n: 1,
      }),
    });
  } else {
    const form = new FormData();
    form.append('model', opts.model);
    form.append('prompt', prompt);
    form.append('size', opts.size);
    form.append('quality', opts.quality);
    form.append('output_format', 'png');
    form.append('n', '1');
    if (opts.inputFidelity) form.append('input_fidelity', opts.inputFidelity);
    for (const ref of opts.refs) {
      const data = await readFile(ref);
      form.append('image[]', new Blob([data], { type: mimeFor(ref) }), path.basename(ref));
    }
    response = await fetch('https://api.openai.com/v1/images/edits', {
      method: 'POST',
      headers,
      body: form,
    });
  }

  const bodyText = await response.text();
  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${bodyText}`);
  }
  const body = JSON.parse(bodyText);
  const b64 = body?.data?.[0]?.b64_json;
  if (!b64) throw new Error(`No image data in response: ${bodyText.slice(0, 500)}`);

  await mkdir(path.dirname(path.resolve(opts.out)), { recursive: true });
  await writeFile(opts.out, Buffer.from(b64, 'base64'));

  const usage = body.usage ? ` (tokens: ${body.usage.total_tokens})` : '';
  console.log(`Wrote ${opts.out} [${opts.model}, ${opts.size}, ${opts.quality}, refs: ${opts.refs.length}]${usage}`);
}

main().catch((err) => {
  console.error(err.message ?? err);
  process.exit(1);
});
