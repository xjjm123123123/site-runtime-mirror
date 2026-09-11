# Site Runtime Mirror

`Site Runtime Mirror` is a TRAE Skill for rebuilding complex websites by carrying over the original front-end runtime instead of drawing a lookalike from screenshots.

Use it for pages where the hard part is not layout, but behavior: loaders, GSAP timelines, WebGL canvases, Rive files, Lottie JSON, 3D models, custom fonts, lazy chunks, route-dependent state, or scroll-linked animation.

## What it preserves

- Real HTML, CSS, JavaScript, chunks, preload entries, inline config, and dynamic requests.
- Runtime assets such as images, fonts, videos, animation files, models, textures, decoders, workers, and WASM.
- Route assumptions, browser state, scroll positions, and first-visit or logged-in variants when they affect the visual result.
- The original motion path wherever technically possible, instead of replacing it with handmade CSS or a screenshot-based imitation.

## When to use it

Use this Skill when the user asks for:

- `1:1` website or homepage reproduction;
- preserving source-site loading, scroll, WebGL, Rive, Lottie, or 3D behavior;
- debugging why a local replica differs from the official page;
- matching the exact page variant visible in the user's own Chrome browser;
- packaging a local H5 version that can be served and verified.

Do not use it for generic landing pages, redesigns, mood boards, or “inspired by” pages where a new implementation is acceptable.

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

The folder keeps the original slug `official-site-replica` for compatibility. The public name is `Site Runtime Mirror`.

## Workflow summary

1. Inspect the official HTML and runtime entry points.
2. Capture the real browser network graph, including dynamic chunks and animation assets.
3. Identify what renders the target effect: DOM, Canvas, WebGL, Rive, Lottie, video, or a hybrid stack.
4. Mirror required assets locally while preserving route and path assumptions.
5. Serve the local version over HTTP and test the same effective route as the source site.
6. Compare official and local runtime states across multiple frames.
7. Fix missing resources, console errors, stuck loaders, and state mismatches before reporting completion.

## Logged-in variants

Some sites vary by login state, cookies, localStorage, region, viewport, browser profile, or experiment bucket. When the user's Chrome view is the target, use that browser session as the source of truth and capture only the visual/runtime inputs required for reproduction.

Do not store credentials, cookies, private tokens, or unrelated personal data in the Skill or generated package.

## Verification expectations

At minimum, verify:

- no unexplained local `404`, `403`, or `5xx` responses;
- no unhandled runtime exceptions;
- expected canvas, video, image, model, font, and animation assets are present;
- key DOM state, route, viewport, scroll position, and visible text match the target state;
- animation-heavy pages are compared across several timeline frames.

## Safety

Mirrored official assets may be copyrighted or license-restricted. Keep replicas private unless the user has permission to redistribute the source site's scripts, fonts, images, videos, models, and animation files.
