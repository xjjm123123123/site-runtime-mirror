# Official Site Replica Skill

`official-site-replica` is a TRAE Skill for faithful website reproduction. It is designed for cases where a user wants a website, homepage, landing page, or H5 experience to match the source site as closely as possible, especially when the original site contains complex runtime behavior such as loaders, Canvas/WebGL, Rive, Lottie, 3D models, videos, lazy-loaded chunks, custom fonts, route-sensitive state, or scroll-driven animation.

The core idea is simple: do not recreate the look from screenshots first. Capture and replay the original front-end runtime whenever possible, then verify the local result in a real browser.

## What it does

- Captures the source site's real HTML, CSS, JavaScript, chunks, preload entries, runtime config, and dynamic network graph.
- Mirrors visual/runtime assets locally, including images, fonts, videos, animation JSON, models, textures, decoders, workers, WASM files, and route-triggered resources.
- Preserves the official route and browser state assumptions, especially when the source page is served from `/`.
- Separates visual/runtime dependencies from analytics, tracking, chat widgets, and other non-visual noise.
- Verifies the local replica with browser evidence instead of relying on a single screenshot.
- Supports user-browser captures for logged-in, personalized, A/B-tested, or CMS-variant pages.

## When to use it

Use this Skill when the user asks for:

- `1:1` website or homepage reproduction
- faithful official-site cloning
- preserving official loading animation or scroll animation
- reproducing Canvas, WebGL, Rive, Lottie, or 3D model behavior
- debugging why a local replica does not match the source site
- comparing official and local timeline states
- capturing the exact page variant the user sees in their own Chrome browser

Do not use it for ordinary static landing pages, generic redesigns, or “inspired by” visual concepts where a new implementation is acceptable.

## Package contents

```text
official-site-replica/
  SKILL.md
  README.md
  references/
    runtime-acquisition.md
    verification-checklist.md
    pitfalls.md
  scripts/
    timeline_compare.py
    asset_manifest_template.json
  evals/
    evals.json
```

## Workflow summary

1. Fetch and inspect the official HTML.
2. Run the official page in a browser and capture the real network graph.
3. Identify the rendering surface: DOM, Canvas, WebGL, Rive, Lottie, video, or hybrid.
4. Mirror runtime and visual assets locally while preserving path assumptions.
5. Serve the replica through HTTP, preferably from `/` with `index.html` when the source page is also `/`.
6. Compare official and local states at multiple timestamps, not just one screenshot.
7. Fix missing resources and state mismatches before reporting completion.

## Logged-in and A/B variants

Some sites serve different pages depending on login status, cookies, localStorage, region, viewport, browser profile, or experiment bucket. For those cases, an anonymous headless capture may not match what the user sees.

When the user asks to match the page in their Chrome browser:

- use the external Chrome browser as the source of truth;
- capture `window.__globalVars__`, experiment IDs, viewport, rendered DOM, loaded images, stylesheets, resource entries, and visible text;
- avoid capturing or publishing secrets, cookies, tokens, or private data that is not needed for visual reproduction;
- prefer a sanitized rendered-DOM snapshot when live authenticated APIs cannot or should not be replayed locally.

## Verification expectations

At minimum, verify:

- no unexplained local 404/5xx responses;
- no runtime exceptions;
- expected visual assets load;
- expected canvas/video/image counts match or have an explained difference;
- `scrollHeight`, visible section, and key text match the target state;
- timeline frames match for animation-heavy pages.

For personalized snapshot replicas, also verify that the local page keeps the captured state without calling authenticated APIs again.

## Packaging

The distributable package can be provided as:

- `official-site-replica.skill` for direct Skill installation;
- `official-site-replica-skill-source.zip` for full source review, including `evals/`;
- `official-site-replica-package-manifest.json` for package integrity and file listing.

## Safety

Mirrored official assets may be copyrighted or license-restricted. Keep generated replicas private unless the user has permission to redistribute the source site's scripts, fonts, images, videos, models, and animation files.

Do not store credentials, cookies, private tokens, or user-sensitive data in the Skill itself. The Skill should contain reusable workflow instructions only.
