# Runtime Acquisition Guide

Use this guide when a user asks for a 1:1 website replica, especially when the page contains loader animations, Canvas/WebGL, Rive/Lottie, 3D models, video, shader effects, GSAP/ScrollTrigger, or route-dependent front-end behavior.

## Objective

The objective is to make the original front-end runtime reach the same states locally. Do not start by recreating the look with hand-written CSS/JS. A good replica preserves the official runtime chain whenever possible:

- original HTML and DOM assumptions
- original CSS and module/script order
- original runtime scripts and chunks
- dynamic assets requested after navigation
- models, textures, fonts, decoders, workers, animation JSON, and media
- route, storage, cookie, viewport, and first-visit state

## Capture order

1. Fetch the initial HTML and record the final resolved URL.
2. Identify linked CSS, JS, preload/prefetch/modulepreload entries, inline boot config, and asset base paths.
3. Run the official site in a real browser with a fresh profile and capture the network graph.
4. Interact only as much as needed to trigger normal first-load behavior. For scroll-driven pages, capture at several scroll positions after the first-load state is correct.
5. Export or list all 4xx/5xx, dynamic `import()` chunks, JSON animation files, media, fonts, WebGL assets, and workers.
6. Mirror assets locally while preserving the official path shape.
7. Serve locally through HTTP and open the same effective route, usually `/` with `index.html`.

## Assets to look for

Initial HTML rarely contains all runtime assets. Inspect network and console after the page is actually running.

- JavaScript chunks: `.js`, modulepreload chunks, lazy imports.
- Styles: `.css`, fonts referenced by CSS.
- Animation: `.riv`, Lottie/bodymovin `.json`, sprite sheets.
- 3D: `.glb`, `.gltf`, `.bin`, Draco decoders.
- WebGL textures: `.ktx2`, `.basis`, `.webp`, `.png`, `.jpg`, `.hdr`, `.exr`.
- Text rendering: MSDF font `.json` and atlas images.
- Runtime helpers: `.wasm`, `.worker.js`, `basis_transcoder`, `draco_decoder`.
- Media: `.mp4`, `.webm`, `.mov`, poster images, route-triggered works/project videos.
- API-like static data: JSON files under `assets/json`, `data`, `works`, `projects`, or similar.

## Route and state matching

Many mismatches are caused by running the local copy from the wrong path. If the official page is `https://example.com/`, create `index.html` and test `http://localhost:<port>/`.

Compare official and local:

- `location.pathname`
- body/html classes and data attributes
- storage and cookies that influence first-visit or intro branches
- scroll restoration state
- viewport and device scale factor
- reduced-motion and autoplay-related settings
- visible central element from `document.elementFromPoint`
- `scrollHeight` after the page stabilizes

If there are no 4xx errors but the visual state is wrong, investigate route/state before rewriting visuals.

## User-browser variants

Some sites do not have a single canonical homepage. The page can change based on login status, experiment buckets, region, language, cookies, local storage, CMS settings, or the user's current browser profile. In those cases, a clean headless capture may produce a different valid online variant than the one the user sees.

When the user says the online page differs from the replica, inspect the user's actual Chrome page if available. Treat that browser state as the source of truth.

Record the following from the user's browser without storing private credentials:

- `location.href`, title, viewport, device pixel ratio, language, and user agent
- public runtime flags such as `window.__globalVars__`, build version, environment, login status, region code, and A/B version IDs
- rendered DOM or a sanitized DOM snapshot
- visible text for the first viewport and key sections
- image, video, canvas, and iframe counts
- loaded stylesheet, script, image, font, and media resource URLs
- `performance.getEntriesByType("resource")` for resources already used by the rendered page
- console and network failures

If the page is authenticated or personalized, prefer a rendered-DOM snapshot for local reproduction instead of replaying authenticated APIs. Remove scripts that would fetch private data again, replace cross-origin iframes with placeholders when they are not part of the target visual, and mirror only visual assets required to preserve the captured state.

Do not capture, commit, or package cookies, bearer tokens, CSRF tokens, account secrets, raw private API responses, or unnecessary personal data. If visible personal content is part of the screenshot-level target, tell the user that the local replica contains personalized visible information and should remain private.

## First-load animation capture

Use a fresh browser profile for first-load animation. Do not let a previous visit, local storage, or cached route state skip the intro unless the official comparison uses the same condition.

Capture the same timestamps on official and local, for example:

- 1 second after navigation
- 3 seconds after navigation
- 6 seconds after navigation
- 10 seconds after navigation

At each timestamp record:

- screenshot
- `scrollY`
- `scrollHeight`
- body/html classes
- central element and text
- canvas/video/image counts
- console exceptions
- failed requests and 4xx/5xx responses

## When to patch

Patch only what is required for local operation:

- asset path resolution
- base URL assumptions
- analytics or third-party calls that are not part of the visual runtime
- cache-busting during debugging
- narrow loader watchdogs only after the original visual runtime has initialized

Avoid replacing official animation systems with new handmade animations unless the fallback is explicitly disclosed.
