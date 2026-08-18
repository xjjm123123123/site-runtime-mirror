# Replica Pitfalls

These pitfalls come from real official-site replica attempts. Use them as a diagnostic guide when a replica “almost works” but the final result is not actually identical.

## Mistaking style recreation for runtime replay

Symptom:

- The page looks inspired by the official site, but the user says the animations are invented.
- Loading screen, scroll motion, WebGL/Rive/Lottie, or model behavior feels different.

Wrong response:

- Add custom CSS animations to approximate the source.
- Manually rebuild the page from screenshots.
- Say the result is “close enough” because the static composition is similar.

Correct response:

- Return to the official runtime chain.
- Identify the original scripts, chunks, animation files, models, textures, fonts, and decoders.
- Preserve the official animation system whenever possible.
- Clearly label any manually rebuilt fallback.

Why it matters:

The user is asking for the official site's behavior, not a new site in the same visual style. Runtime replay is the only reliable path for complex animation parity.

## Hiding a stuck loader too early

Symptom:

- The page stays on a loading screen.
- A forced class/style change reveals content underneath.

Wrong response:

- Immediately hide the loader with CSS or JavaScript.
- Add a timeout that always removes the transition layer.

Correct response:

- Inspect console and network first.
- Identify the first failed resource group.
- Check whether the loader waits for model/texture/font/WASM/Rive/Lottie promises.
- Fix missing assets before adding any watchdog.
- Add a narrow fallback only after the real visual runtime has initialized and no critical resource errors remain.

Why it matters:

The loader is often correctly waiting for missing runtime assets. Hiding it can make the page appear “loaded” while WebGL, model, font, or animation systems are still broken.

## Capturing only fallback texture formats

Symptom:

- Browser reports missing `.ktx2`, `.basis`, `.hdr`, model, or MSDF font files.
- There are multiple `ERR_ABORTED` logs after the first few 404s.

Wrong response:

- Assume existing `.webp` or `.png` files are enough.
- Chase every aborted file as an independent problem.

Correct response:

- Determine which capability branch the browser selected.
- Mirror both primary and fallback formats when the source runtime supports them.
- Include required decoders such as `basis_transcoder.js`, `basis_transcoder.wasm`, Draco wrappers, and WASM files.
- Treat later `ERR_ABORTED` messages as possible secondary failures after the first missing group.

Why it matters:

Modern WebGL runtimes choose asset branches based on browser capabilities. A local copy can have images but still fail because the browser requested compressed textures.

## Declaring success from a clean console

Symptom:

- Console errors and 4xx responses are zero.
- The screenshot still does not match the official site.
- Scroll height, visible section, or animation phase differs.

Wrong response:

- Say the replica is correct because there are no errors.
- Start manually changing layout or style.

Correct response:

- Compare runtime state, not only logs.
- Check `location.pathname`, body/html classes, storage, cookies, history state, viewport, scroll restoration, and first-visit branches.
- Compare `scrollY`, `scrollHeight`, central visible element, canvas/video/image counts, and timeline progress.

Why it matters:

A site can run without throwing and still be in the wrong route, state branch, or timeline phase.

## Testing from a named HTML file instead of root

Symptom:

- Local preview uses `/site-replay.html`.
- Official site is served from `/`.
- Visual state, scroll height, or first section differs.

Wrong response:

- Keep debugging styles and resources while serving from the wrong path.

Correct response:

- Create `index.html`.
- Serve locally from `http://localhost:<port>/`.
- Retest the resource graph and runtime state from the root path.

Why it matters:

Route-aware front-end code often branches on `location.pathname`, base URL, router state, or scroll restoration. The same script can behave differently from `/` and `/some-file.html`.

## Missing dynamic resources not visible in HTML

Symptom:

- Initial HTML and static assets appear mirrored.
- Scrolling or waiting triggers missing videos, Lottie JSON, chunks, or data files.
- Layout height differs from the official page.

Wrong response:

- Stop after mirroring the initial HTML asset list.

Correct response:

- Capture the official page in a running browser.
- Watch dynamic imports and delayed requests.
- Trigger normal first-load and scroll states.
- Mirror route-triggered media, JSON, chunks, and project/works assets.

Why it matters:

Many modern sites lazy-load the assets that actually control layout height and animation stages.

## Relying on one screenshot

Symptom:

- One frame looks similar, but entry animation or scroll behavior is wrong.
- User says screenshots are not enough to prove the motion.

Wrong response:

- Compare only one still image.

Correct response:

- Capture a timeline from official and local, such as `1s`, `3s`, `6s`, `10s`.
- Record DOM state and network state at each timestamp.
- Use pixel diff only for matched frames.
- If early frames differ but stable frames converge, explicitly state which stage matches and continue fixing if full entry parity is required.

## Capturing the wrong online variant

Symptom:

- The local replica is faithful to one online version, but the user says their browser shows a different page.
- The source site changes between anonymous and logged-in states.
- Page height, visible modules, navigation buttons, or recommendations differ even though assets and console errors look clean.

Wrong response:

- Continue tuning layout against the anonymous headless capture.
- Assume the user's browser must be stale or wrong.
- Ignore login status, A/B version IDs, cookies, localStorage, viewport, language, or region.

Correct response:

- Inspect the user's actual Chrome browser when the user asks for that version.
- Compare runtime flags such as login status, region, build version, and experiment IDs.
- Capture the rendered DOM, visible text, image list, resource entries, and viewport from the user's browser.
- For authenticated pages, prefer a sanitized rendered-DOM snapshot over replaying private APIs locally.
- Tell the user if the replica contains visible personalized content and should remain private.

Why it matters:

Many official sites are CMS-driven, A/B-tested, and personalized. A clean anonymous runtime capture can be technically correct but still not match the specific page variant the user wants.

Why it matters:

Screenshots verify a frame. They do not prove animation timing, state transitions, or asset-driven runtime behavior.

## Reusing a dirty browser profile

Symptom:

- Official and local first-load states differ between runs.
- Loader or intro sometimes appears and sometimes does not.

Wrong response:

- Assume the result is random or only a cache issue.

Correct response:

- Use a fresh profile for first-load animation tests.
- Test storage/cookie states deliberately.
- Clear or compare `localStorage`, `sessionStorage`, and cookies.

Why it matters:

Many sites store “visited” or intro-complete flags. A dirty profile can skip or alter the exact animation the user wants replicated.

## Over-packaging debug artifacts

Symptom:

- The H5 source package includes temporary scripts, screenshots, comparison folders, browser profiles, caches, or raw debug outputs.

Wrong response:

- Zip the whole workspace.

Correct response:

- Package only entry HTML, localized runtime assets, source scripts/styles, supporting assets, and README.
- Exclude `.git`, temporary capture scripts, debug screenshots, browser caches, credentials, and unrelated files.
- Keep comparison evidence separately unless the user asks for it.

Why it matters:

The user wants usable H5 source, not the agent's scratch workspace.

## Saying “official assets” without proving paths

Symptom:

- The response claims real official assets are used.
- Browser logs or package contents do not prove the exact runtime paths.

Wrong response:

- Rely on assumptions or filenames that only look plausible.

Correct response:

- Tie claims to observed source HTML, network requests, local files, and browser verification.
- Keep an asset manifest.
- Confirm that local URLs return successfully at the same paths the runtime requests.

Why it matters:

Faithful replication depends on exact path and runtime behavior, not on asset names alone.
