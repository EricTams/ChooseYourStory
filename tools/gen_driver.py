#!/usr/bin/env python3
"""Run image generations from pip_manifest.json with limited concurrency.
Usage: gen_driver.py refs|scenes [only_id ...]"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = '/Users/erictams/AIDev/ChooseYourStory'
HERE = os.path.dirname(os.path.abspath(__file__))
manifest = json.load(open(f'{HERE}/pip_manifest.json'))

group = sys.argv[1]
only = set(sys.argv[2:])
jobs = [j for j in manifest[group] if not only or j['id'] in only]

def run(job):
    cmd = ['node', f'{ROOT}/scripts/generate-image.mjs',
           '--prompt-file', job['prompt'], '--out', job['out']]
    for r in job['refs']:
        cmd += ['--ref', r]
    for attempt in (1, 2, 3):
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        if p.returncode == 0:
            return job['id'], 'ok', p.stdout.strip()
        err = (p.stderr or p.stdout).strip()[-300:]
        if attempt == 3:
            return job['id'], 'FAILED', err
    return job['id'], 'FAILED', 'unreachable'

results = []
with ThreadPoolExecutor(max_workers=3) as ex:
    futs = {ex.submit(run, j): j['id'] for j in jobs}
    for f in as_completed(futs):
        jid, status, msg = f.result()
        print(f"[{status}] {jid}: {msg}", flush=True)
        results.append(status)

fails = results.count('FAILED')
print(f"\nDone: {len(results) - fails}/{len(results)} succeeded")
sys.exit(1 if fails else 0)
