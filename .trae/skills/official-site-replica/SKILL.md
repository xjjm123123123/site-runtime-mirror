---
name: "official-site-replica"
description: "Recreates official websites by replaying original runtime assets and scripts. Invoke when user asks for 1:1 site cloning with animations, loaders, Canvas/WebGL/Rive/3D models."
---

# Official Site Replica

Use this skill when the user asks to reproduce an existing website as faithfully as possible, especially when the target includes animated loading screens, Webflow/GSAP interactions, Canvas/WebGL/WebGPU, Rive animations, GLB/GLTF models, shader effects, compressed textures, custom fonts, or complex scroll-driven motion.

The goal is not to create a visually inspired page. The goal is to preserve and replay the original runtime chain wherever legally and technically possible, then verify the local result in a real browser before delivery. For front-end code, prefer “make the original runtime reach the same states locally” over “rebuild the visual result by hand.”

## Core Principle

Do not invent replacement animations when the user's requirement is a faithful replica.

Start from the source site's real HTML, CSS, JavaScript, assets, model files, animation files, textures, font atlases, decoders, and runtime configuration. Only rebuild manually when a source runtime component cannot be recovered or cannot run locally, and label that part clearly as a fallback.

For animated sites, a single screenshot is not enough. Screenshots verify only one frame. Use browser runtime evidence, timeline snapshots, resource coverage, and state comparison to prove that the original front-end code path is running.

## When To Invoke

Invoke this skill when the user says or implies:

- “1:1 复刻官网”
- “和源网站一模一样”
- “保留官网动效”
- “加载页也要一样”
- “模型 / WebGL / Canvas / Rive 动画要还原”
- “不是按风格创作”
- “先自己运行对比再给我”
- “本地运行不了，修复到能跑”

Do not use this skill for ordinary landing pages, generic UI redesign, static screenshot recreation, or cases where the user explicitly wants an original design inspired by a reference.

## Deliverables

The default deliverable is a local H5 project:

- `index.html` as the preferred entry when the official page is served from `/`
- a clearly named secondary entry HTML file only for debugging or alternate routes
- `assets/` containing localized runtime assets
- original or adapted runtime scripts
- any required model, texture, font, decoder, Rive, HDR, shader, or worker files
- `README.md` with local run instructions
- optional `.zip` package when the user asks for source code

Prefer a static HTTP server preview over direct `file://` opening. Many official runtimes require HTTP origins for fetch, worker, WASM, model, texture, font loading, route detection, and history APIs.

When the official page is the root URL, create and test `index.html` at the local server root and open `http://localhost:<port>/`. Do not rely only on `http://localhost:<port>/<named-replay>.html`, because route-aware front-end runtimes often branch on `location.pathname`, base URL, history state, or scroll restoration.

## Workflow

## Bundled Resources

Read these files when the task needs more operational detail:

- `references/runtime-acquisition.md`: step-by-step method for obtaining front-end runtime code and dynamic assets.
- `references/verification-checklist.md`: evidence checklist for deciding whether a replica is actually aligned with the official site.
- `references/pitfalls.md`: real pitfalls from previous replica attempts and how to avoid them.
- `scripts/timeline_compare.py`: optional Playwright-based helper for collecting official/local timeline screenshots, DOM state, network errors, and pixel diff.
- `scripts/asset_manifest_template.json`: manifest template for tracking mirrored runtime assets.
- `evals/evals.json`: realistic prompts for testing whether this skill produces source-runtime replicas rather than style-inspired imitations.

### Standard Front-End Runtime Acquisition Flow

Use this flow for every serious front-end replica. It is the default way to obtain and validate the front-end code path.

1. Fetch the official HTML and identify the framework/runtime, entry scripts, CSS, preload links, route assumptions, and visible DOM.
2. Run the official page in a browser and capture the real network graph, including dynamic chunks, animation JSON, media, WebGL assets, fonts, decoders, workers, and route-triggered assets.
3. Mirror assets locally while preserving the official path shape as much as possible.
4. Create `index.html` and serve from the local root when the official page is `/`; keep secondary replay files only for debugging.
5. Remove analytics/noise only when it is not part of the visual/runtime path.
6. Test the local root URL in a fresh browser profile through HTTP, not `file://`.
7. Fix every unexplained 4xx/5xx or missing dynamic resource before judging visuals.
8. Compare official and local timeline states at several timestamps, not just one screenshot.
9. If resources are clean but visuals differ, inspect route, storage, cookies, history state, scroll restoration, WebGL state, and animation/scroll timeline progress.
10. Only report completion when the same stable runtime state is reached locally, not merely when the DOM exists or the console is clean.

The important mental model: a front-end replica is successful when the original runtime reaches the same states locally. A screenshot is only one piece of evidence.

### 1. Capture The Real Source

Fetch and inspect the target page before writing any replica code.

Record:

- final resolved URL
- entry HTML structure
- linked CSS and JS
- inline boot config
- asset base URLs
- script order
- preload/prefetch links
- canvas, WebGL, WebGPU, Rive, iframe, worker, and video nodes
- loader/transition DOM
- framework/runtime identifiers such as Webflow, GSAP, Three.js, Rive, Pixi, OGL, Babylon, React, Next, Nuxt, Spline, or custom bundles

If `WebFetch` can retrieve the page, use it first. If richer browser state is required, use browser automation or a local HTTP capture script, but do not bypass domains blocked by retrieval policy.

### 2. Identify Runtime Surfaces

Before cloning assets, identify which runtime surface actually renders the target visual.

Check:

- number and dimensions of canvases
- parent containers and z-index
- WebGL/WebGPU context creation
- Rive canvas instances and `.riv` files
- worker scripts
- model and texture loaders
- scroll or pointer event bindings
- transition and loading-state classes

Avoid assuming that a detected library is responsible for the target effect. Bind every claim to observed DOM, network, console, or runtime evidence.

### 3. Localize The Runtime Chain

Mirror source assets into a stable local structure, for example:

```text
assets/official-runtime/
  original-runtime.js
  transitions.js
  rive/
  gl/
    models/
    textures/
      webp/
      ktx2/
    fonts/
    hdri/
    draco/
    basis/
```

Preserve relative paths expected by the original scripts where possible. If scripts expect `/gl/textures/...`, either mirror that path or patch the script path resolver minimally.

Common assets to localize:

- `.js`, `.css`, `.wasm`, `.worker.js`
- `.riv`
- `.glb`, `.gltf`, `.bin`
- `.ktx2`, `.webp`, `.png`, `.jpg`, `.hdr`, `.exr`
- MSDF font atlases and `.json`
- Draco decoders: `draco_decoder.wasm`, `draco_wasm_wrapper.js`
- Basis/KTX2 decoders: `basis_transcoder.js`, `basis_transcoder.wasm`
- shader chunks or external GLSL files

### 4. Preserve Script Semantics

Prefer replaying the official scripts instead of reimplementing the animation in CSS.

Patch only what is required for local operation:

- replace absolute CDN paths with local paths
- add cache-busting query strings while debugging
- disable editor/design flags that keep transition layers stuck
- patch origin assumptions only when needed
- add a narrow watchdog only after proving official initialization has completed but a transition layer did not exit

Do not replace the official loading animation, scroll motion, 3D model, Rive animation, or shader effect with a hand-made imitation unless the fallback is explicitly documented.

### 4.5. Reproduce The Official Route And Browser State

Many modern front-end sites initialize differently depending on URL, history state, storage, cookies, viewport, reduced-motion settings, autoplay policy, and whether the page is served from `/` or from a named HTML file.

Before judging visual mismatch, align these inputs with the official site:

- serve the local copy from the same effective path, usually `/` with `index.html`
- keep same viewport size and device scale factor for comparisons
- compare `location.href`, `location.pathname`, `document.referrer`, body attributes, and root classes
- compare `localStorage`, `sessionStorage`, and relevant cookies when they affect loaders, intro states, consent banners, or “already visited” branches
- disable or normalize browser features only when both official and local runs use the same flags
- avoid reusing a dirty browser profile when testing first-load animations; use fresh profiles for timeline comparisons
- if a site has a cookie consent or first-visit intro, test both fresh and accepted-cookie states

If the local replay looks wrong but has no 4xx or console errors, suspect route/state mismatch before rewriting visuals.

### 5. Loading Screen Discipline

Loading pages often remain visible because one resource group failed.

Before adding a forced hide:

- inspect console errors
- inspect failed network requests
- verify expected model, texture, font, WASM, and Rive paths
- confirm whether the original loader waits for a specific promise or class transition
- fix missing assets first

Only add a minimal fallback transition when:

- core canvases or runtime nodes exist
- no critical 4xx/5xx resource failures remain
- the page is visually initialized behind the loader
- the fallback does not replace the original effect

If a loader is stuck, read `references/pitfalls.md` before patching it. The most common mistake is to hide the loader too early and accidentally mask the real missing runtime asset.

### 6. Browser Verification

Always test the replica in a real browser before reporting completion.

At minimum verify:

- page loads through `http://localhost:<port>/...`
- console errors are empty or explained
- failed network requests are empty or explained
- no critical 404/403/500 responses
- loader enters and exits
- expected canvas/Rive/WebGL nodes exist
- model files load
- texture/font/decoder files load
- animation is not static
- key scroll or pointer interactions respond

Do not stop at one screenshot. For animation-heavy pages, collect a small timeline from both official and local:

- same viewport, same browser type, fresh profile
- snapshots at stable timestamps such as 1s, 3s, 6s, and 10s after navigation
- no manual scroll for first-load comparison unless the official user flow includes it
- DOM state at each timestamp: `scrollY`, `scrollHeight`, `body` classes/attributes, central element from `elementFromPoint`, visible section names, canvas/video/image counts
- network state: 4xx/5xx, failed requests, dynamically imported chunks, JSON animation data, media files
- screenshots for visual review plus pixel diff for objective drift

Treat “console clean” as necessary but not sufficient. A page can have zero errors and still be in the wrong animation state.

Suggested acceptance thresholds for same-frame comparison:

- key runtime assets: no unexplained 4xx/5xx
- exceptions: none, except known browser media autoplay aborts that also occur on the official site
- structural state: same canvas/video/image counts and same dominant visible section
- scroll metrics: `scrollHeight` within a small tolerance unless responsive layout explains the difference
- stable-frame pixel diff: ideally below 1% sampled pixel ratio for a matched state; investigate anything above a few percent
- if early timeline frames differ but later stable frames converge, state which frame is considered the matched target

Useful checks:

- compare screenshots at different timestamps for frame movement
- count canvases and check dimensions
- inspect computed visibility of transition overlays
- record request URLs returning 4xx/5xx
- check whether old cache-bust versions are still loaded
- use a new entry filename when browser preview caching is stubborn

### 7. Fix Missing Resource Loops

When the browser shows logs like:

```text
fetch for ".../textures/.../file.ktx2" responded with 404
net::ERR_ABORTED ".../models/file.glb"
net::ERR_ABORTED ".../fonts/font-msdf.json"
```

Treat the first missing resource group as the root cause. Later `ERR_ABORTED` messages may be secondary failures after the runtime cancels asset loading.

Fix loop:

1. Copy the exact missing URL list from console/network.
2. Check whether local files exist at the requested paths.
3. Download or mirror the exact assets from the official asset base when allowed.
4. Preserve directory names and filenames exactly.
5. Include both fallback and primary formats when used by capability branches, such as `webp` and `ktx2`.
6. Include decoders required by the selected branch, such as Basis/KTX2 or Draco.
7. Refresh cache-bust query strings.
8. Retest in browser.

Do not claim success while any unexplained critical resource errors remain.

Also inspect dynamic resources that do not appear in the initial HTML:

- ES module chunks loaded through `import()`
- Lottie/bodymovin JSON files
- media files requested only when a carousel or scroll section activates
- route-specific images/videos under works/cases/projects paths
- WebGL/HDR/texture files loaded after capability detection
- fonts requested by CSS after first layout

If the local page changes state after serving from `/`, rerun resource capture because new chunks and media may only be requested in the correct route branch.

### 8. Compare Against The Official Site

For “1:1” work, compare the local page against the official page whenever possible.

Compare:

- initial loader appearance and exit timing
- first viewport composition
- typography and scale
- navigation placement
- model/canvas presence
- animation rhythm
- scroll transitions
- hover/pointer response
- mobile/desktop breakpoints if required

If exact matching cannot be achieved, state the specific remaining gap and whether it is due to missing assets, blocked runtime behavior, license/access limits, or a fallback implementation.

Comparison should use both automated evidence and human-readable artifacts:

- side-by-side screenshots from official and local at multiple timestamps/scroll points
- a short machine summary: console count, failed requests, 4xx count, canvas/video/image counts, `scrollHeight`, dominant visible elements
- pixel diff for matched frames when screenshots are available
- a written verdict that distinguishes “runtime clean” from “visually matched”

If the user only cares about the final result, keep the report internal and continue fixing until the dominant frames match. Share the comparison only when the user asks for evidence or when a blocker prevents full parity.

## Evidence Standard

Use evidence-backed statements:

- `SOURCE`: directly observed in source HTML, JS, CSS, network, or local browser run
- `PARTIAL`: observed but not fully localized or not fully understood
- `FALLBACK`: manually rebuilt because original runtime could not be replayed
- `UNKNOWN`: not yet confirmed

Do not use vague claims such as “basically identical” without browser evidence.

## User Communication

Be direct when quality is not yet sufficient. If the user says the result is unlike the source, stop defending the current build and inspect the browser/source gap.

Good response pattern:

- acknowledge the specific mismatch
- identify the likely technical cause
- inspect real browser logs/network
- fix root-cause resource/runtime issues
- retest before returning

Avoid:

- delivering a style-inspired page when the user requested source-site replication
- saying a model is loaded without verifying the actual GLB/GLTF request
- saying animations work without checking frame changes
- hiding a stuck loader before fixing missing assets
- ignoring selected console logs from the user

## Packaging

When the user asks for source code, package the H5 project as a zip.

Include:

- entry HTML
- `assets/`
- runtime scripts
- `README.md`

Exclude:

- `.git/`
- temporary test scripts
- screenshots used only for debugging
- browser cache files
- credentials or private tokens

## README Template

Use a concise README:

```markdown
# Site Replica

Private local reproduction for review and testing.

## Run locally

Serve this folder with a static HTTP server, then open:

http://localhost:PORT/<entry-file>.html

## Recommended entry

<entry-file>.html

## Notes

This project localizes runtime assets required for the reproduction. Keep private unless you have rights to redistribute the mirrored assets.
```

## Safety And Rights

If the replica includes official scripts, models, textures, fonts, or animation assets, recommend keeping the repository private unless the user has redistribution rights. Do not remove copyright, license, or attribution notices from source files.
