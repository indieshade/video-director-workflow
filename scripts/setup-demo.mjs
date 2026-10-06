import {copyFile, mkdir} from 'node:fs/promises';
const root = new URL('../', import.meta.url);
const dest = new URL('examples/collage-paper-study/assets/', root);
await mkdir(dest, {recursive: true});
await copyFile(new URL('node_modules/gsap/dist/gsap.min.js', root), new URL('gsap.min.js', dest));
console.log('Local GSAP copied from the pinned npm dependency. Its upstream license applies.');
await import('./setup-probes.mjs');
