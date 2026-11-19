// Entry program for the make.fun bounty "Sum up 19 November's world news in one image".
//
// It writes the front-page image for Thursday 19 November 2026 (entry.png,
// drawn by draw.py) to the output directory as entry.png. The grader sets
// MAKEFUN_OUTPUT_DIR to the output directory; outside the grader, it
// defaults to /output, so a local run looks like:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// The gate takes a whole PNG or JPEG of at most 1 MiB and 1024 by 1024
// pixels, so the program refuses to write an image that breaks the size
// limit instead of handing the judge a file it cannot use.

import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const IMAGE_NAME = 'entry.png';
const MAX_BYTES = 1024 * 1024;

const sourcePath = new URL(`./${IMAGE_NAME}`, import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const targetPath = join(outDir, IMAGE_NAME);

if (!existsSync(sourcePath)) {
  throw new Error(`${IMAGE_NAME} is missing next to main.ts`);
}

const size = statSync(sourcePath).size;
if (size > MAX_BYTES) {
  throw new Error(`${IMAGE_NAME} is ${size} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, readFileSync(sourcePath));
console.log(`wrote ${targetPath} (${size} bytes)`);
