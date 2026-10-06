import {copyFile, mkdir, readFile} from 'node:fs/promises';
const root = new URL('../', import.meta.url);
const audit = new URL('examples/style-prompt-audit/', root);
const {cases} = JSON.parse(await readFile(new URL('cases.json', audit), 'utf8'));
for (const {id} of cases) {
  if (!/^[a-z0-9-]+$/.test(id)) throw new Error('Invalid case ID');
  const dest = new URL(`${id}/assets/`, audit);
  await mkdir(dest, {recursive: true});
  await copyFile(new URL('node_modules/gsap/dist/gsap.min.js', root), new URL('gsap.min.js', dest));
}
console.log(`Prepared pinned GSAP for ${cases.length} probes. Install a licensed Chinese font separately.`);
