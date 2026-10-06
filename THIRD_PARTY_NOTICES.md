# Attribution and license scope

The root MIT license covers original workflow documentation, scripts and original scene arrangement. It does not relicense dependencies, fonts, audio or third-party textures. Concept images and the sample video are shared as example assets; this is not a promise of exclusive rights to AI-generated imagery.

- **Generated reader/book atlas**: produced with the host imagegen tool for this original sample; conceptual subject, not the author's likeness or factual evidence. Normalized generation brief: `examples/collage-paper-study/evidence/image-prompt.txt`.
- **Noto Serif SC / Noto Sans SC subsets**: original Google font software, SIL Open Font License 1.1. The prepared subsets contain the five title characters; upstream notices and complete OFL text are included in the sample `assets/fonts/`. Fonts remain under OFL.
- **Paper sound**: prepared mix from the previously sourced Kenney Paper / Draw Knife 1, CC0, distributed via https://remotion.media/page-turn.wav. The frozen mix is included; provenance follows the original source attribution, not a newly claimed recording.
- **HyperFrames Registry adaptation**: the scene adapts stop-motion-cadence's quantize-first clock and grain-overlay's seeded texture mechanism; original layout and five-second arrangement. The concrete mask is distributed from `texture-mask-text`, and plaster-001 is its ambientCG material mask. HyperFrames is Copyright 2026 HeyGen, Inc., Apache-2.0. Full license: `licenses/HyperFrames-Apache-2.0.txt`. Upstream: https://github.com/heygen-com/hyperframes/tree/main/registry . Modified inline mechanisms are identified in the scene comments; full registry demo files are not redistributed.
- **ambientCG Plaster001**: CC0 asset, adapted mask provided by HyperFrames. https://ambientcg.com/a/Plaster001 · https://docs.ambientcg.com/license/ .
- **GSAP 3.13.0**: installed via npm, not checked in. Its header and npm license are retained when the setup script copies the browser file. https://gsap.com/standard-license/ .
- **HyperFrames CLI / FFmpeg**: separately installed runtime dependencies with their own licenses. No runtime binaries are distributed here.
- **External references**: skill documents retain source links and distinguish source findings from our application choices. Downloaded benchmark videos, reference screenshots and third-party skill bundles are not included. This project has no affiliation with Vox, Anthropic, OpenAI, HeyGen or the referenced creators.

## Gallery compositions

The gallery adds our finished compositions, not external benchmark films. Per-case notices include attribution, license links and changes; they govern third-party material within each film. Original arrangement does not change those licenses.

- [Collage](gallery/collage/CREDITS.md): the same sample assets described above.
- [PLAY / FORM](gallery/shape-play/CREDITS.md): Kevin MacLeod music, CC BY 4.0, and Pixabay sound effects within the edited film.
- [In Between](gallery/material-field/CREDITS.md): Kevin MacLeod music, CC BY 4.0, Pixabay sound effects and rendered OFL font text. The gallery delivery is resized and re-encoded; its metadata preserves the source hash.
- [Copper & Cyan](gallery/pixel-wizard/CREDITS.md): original procedural pixels; tutorial/reference links are not redistributed sprites.
- [SoftSignal](gallery/ui-morph/CREDITS.md): original synthesized audio and procedural layout; rendered Geist font, Lucide icons and D3 shapes retain the notices identified in the case.

No standalone third-party music or sound-effect files are included in these added cases.

## Style-prompt audit probes

Seven original silent six-second compositions and four raw AI-generated concept images are provided under `examples/style-prompt-audit/`. Exact image inputs and limits are recorded with each asset. No external reference pixels, original benchmark films, private voice recordings or user likeness assets are included. The host did not report the image model version; no exclusive-rights guarantee is made.

The private renders used installed Microsoft YaHei. Its font software is not redistributed; portable source uses an installed-font lookup and system fallbacks. GSAP 3.13.0 is prepared from the existing npm dependency by `setup:probes`, retaining its header and upstream license. HyperFrames and FFmpeg are separately installed tools. The original arrangement does not relicense any dependency or font.

## Research references

The primary style library cites external work and observed positions. Its HTML page uses YouTube's hosted players and an image hosted on Antoni Sendra's [Vox Earworm project page](https://podenco.tv/vox-earwormdub-music/); the README and research document also link/embed that author-hosted image. Those references remain the respective rights holders' work, are not covered by this project's MIT license and are not checked into this repository as media files. A project image is identified as static reference, not continuous motion evidence.
