import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const demo = new URL('../examples/collage-paper-study/', import.meta.url);
const result = spawnSync(process.env.FFMPEG_PATH || 'ffmpeg', [
  '-v', 'error', '-y', '-i', 'renders/picture.mp4', '-i', 'assets/paper-mix.wav',
  '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
  '-t', '5', '-movflags', '+faststart', 'renders/reproduced.mp4'
], {cwd: fileURLToPath(demo), stdio: 'inherit'});
if (result.error) {console.error(result.error.message); process.exit(1);}
process.exit(result.status ?? 1);
