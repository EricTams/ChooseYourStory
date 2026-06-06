#!/usr/bin/env node
// Optimize served story images: resize + convert PNG -> WebP, then rewrite
// the image/cover references in the JSON to point at the .webp files.
//
// What it touches:
//   - game/data/stories/<slug>/*.png        (scene art)      -> .webp + JSON "image"
//   - game/data/stories/<slug>/cover.png     (cover)          -> .webp + catalog "cover"
// What it leaves alone:
//   - game/data/stories/<slug>/_refs/*.png   (author-only reference sheets)
//
// Originals are moved into a sibling `_originals/` folder per story (so they are
// preserved and easy to exclude from deploys) unless --delete-originals is passed.
//
// Usage:
//   npm install            # one time, pulls in sharp
//   npm run optimize-images
//
// Options:
//   --width=1440           max width in px (no upscaling); default 1440
//   --quality=80           webp quality 1-100; default 80
//   --story=<slug>         only process one story folder; default all
//   --delete-originals     delete the .png instead of moving to _originals/
//   --dry-run              report what would happen, write nothing

import sharp from 'sharp';
import { readdir, readFile, writeFile, mkdir, rename, rm, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const STORIES_DIR = path.join(ROOT, 'game', 'data', 'stories');
const CATALOG = path.join(ROOT, 'game', 'data', 'catalog.json');

const SKIP_DIRS = new Set(['_refs', '_originals']);

function parseArgs(argv) {
  const opts = { width: 1440, quality: 80, story: null, deleteOriginals: false, dryRun: false };
  for (const arg of argv) {
    if (arg === '--dry-run') opts.dryRun = true;
    else if (arg === '--delete-originals') opts.deleteOriginals = true;
    else if (arg.startsWith('--width=')) opts.width = Number(arg.slice(8));
    else if (arg.startsWith('--quality=')) opts.quality = Number(arg.slice(10));
    else if (arg.startsWith('--story=')) opts.story = arg.slice(8);
  }
  return opts;
}

async function collectPngs(dir) {
  const out = [];
  const entries = await readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (SKIP_DIRS.has(e.name)) continue;
      out.push(...(await collectPngs(full)));
    } else if (e.isFile() && e.name.toLowerCase().endsWith('.png')) {
      out.push(full);
    }
  }
  return out;
}

function fmtKB(bytes) {
  return `${Math.round(bytes / 1024)} KB`;
}

async function convertOne(pngPath, opts) {
  const webpPath = pngPath.replace(/\.png$/i, '.webp');
  const before = (await stat(pngPath)).size;
  const image = sharp(pngPath);
  const meta = await image.metadata();
  let pipeline = image;
  if (meta.width && meta.width > opts.width) {
    pipeline = pipeline.resize({ width: opts.width, withoutEnlargement: true });
  }

  if (opts.dryRun) {
    const dims = `${meta.width}x${meta.height}`;
    console.log(`  [dry] ${path.relative(ROOT, pngPath)}  (${dims}, ${fmtKB(before)}) -> .webp`);
    return { before, after: 0 };
  }

  await pipeline.webp({ quality: opts.quality, effort: 5 }).toFile(webpPath);
  const after = (await stat(webpPath)).size;

  // Preserve or remove the original PNG.
  if (opts.deleteOriginals) {
    await rm(pngPath);
  } else {
    const storyDir = path.dirname(pngPath);
    const backupDir = path.join(storyDir, '_originals');
    await mkdir(backupDir, { recursive: true });
    await rename(pngPath, path.join(backupDir, path.basename(pngPath)));
  }

  const pct = Math.round((1 - after / before) * 100);
  console.log(`  ${path.relative(ROOT, pngPath)}  ${fmtKB(before)} -> ${fmtKB(after)} (-${pct}%)`);
  return { before, after };
}

// Rewrite only the given JSON keys' .png values to .webp (leaves referenceImage alone).
async function rewriteRefs(jsonPath, keys, opts) {
  if (!existsSync(jsonPath)) return 0;
  const original = await readFile(jsonPath, 'utf8');
  let updated = original;
  for (const key of keys) {
    const re = new RegExp(`("${key}"\\s*:\\s*")([^"]+?)\\.png(")`, 'g');
    updated = updated.replace(re, '$1$2.webp$3');
  }
  if (updated !== original && !opts.dryRun) {
    await writeFile(jsonPath, updated);
  }
  const count = (original.match(/\.png"/g) || []).length - (updated.match(/\.png"/g) || []).length;
  return count;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  console.log(
    `Optimizing images  width<=${opts.width}px  quality=${opts.quality}` +
      `${opts.dryRun ? '  [DRY RUN]' : ''}\n`
  );

  const storyEntries = await readdir(STORIES_DIR, { withFileTypes: true });
  let slugs = storyEntries.filter((e) => e.isDirectory() && !SKIP_DIRS.has(e.name)).map((e) => e.name);
  if (opts.story) slugs = slugs.filter((s) => s === opts.story);

  let totalBefore = 0;
  let totalAfter = 0;
  let fileCount = 0;

  for (const slug of slugs) {
    const dir = path.join(STORIES_DIR, slug);
    const pngs = await collectPngs(dir);
    if (pngs.length === 0) continue;
    console.log(`${slug}  (${pngs.length} images)`);
    for (const png of pngs) {
      const { before, after } = await convertOne(png, opts);
      totalBefore += before;
      totalAfter += after;
      fileCount += 1;
    }
    // Point the story JSON's scene "image" paths at the new .webp files.
    const storyJson = path.join(STORIES_DIR, `${slug}.json`);
    const n = await rewriteRefs(storyJson, ['image'], opts);
    if (n) console.log(`  updated ${n} "image" refs in ${slug}.json`);
    console.log('');
  }

  // Covers live in the catalog — only rewrite entries for stories we converted.
  if (existsSync(CATALOG)) {
    const original = await readFile(CATALOG, 'utf8');
    let updated = original;
    for (const slug of slugs) {
      const re = new RegExp(
        `("slug"\\s*:\\s*"${slug}"[^}]*"cover"\\s*:\\s*")([^"]+?)\\.png(")`,
        'g'
      );
      updated = updated.replace(re, '$1$2.webp$3');
    }
    if (updated !== original) {
      const count =
        (original.match(/\.png"/g) || []).length - (updated.match(/\.png"/g) || []).length;
      if (!opts.dryRun) await writeFile(CATALOG, updated);
      if (count) console.log(`Updated ${count} "cover" ref(s) in catalog.json\n`);
    }
  }

  if (!opts.dryRun && fileCount > 0) {
    const pct = Math.round((1 - totalAfter / totalBefore) * 100);
    console.log(`Done. ${fileCount} images: ${fmtKB(totalBefore)} -> ${fmtKB(totalAfter)} (-${pct}% total)`);
  } else if (opts.dryRun) {
    console.log('Dry run complete. Re-run without --dry-run to apply.');
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
