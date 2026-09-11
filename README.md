# Site Runtime Mirror

`Site Runtime Mirror` is a TRAE Skill for rebuilding complex websites by carrying over the original front-end runtime instead of drawing a lookalike from screenshots.

It is meant for the awkward cases: pages with loaders, GSAP timelines, WebGL canvases, Rive files, Lottie JSON, 3D models, custom fonts, lazy chunks, route-dependent state, or scroll-linked animation. The job is to make the original code path run locally and then prove it with browser evidence.

## Why this exists

Most website “replicas” fail in the same way: they copy the visible frame but lose the behavior that made the site feel alive. This Skill keeps the work anchored to the source runtime: the real HTML, scripts, styles, assets, route assumptions, and browser state that produced the target page.

Use it when visual similarity is not enough and the replica needs to preserve the source site's motion system, loading sequence, interaction model, and rendered state.

## What it helps with

- Capturing the page's real runtime graph: HTML, CSS, JavaScript, chunks, preload entries, inline config, and dynamic requests.
- Mirroring visual assets locally: images, fonts, videos, animation files, models, textures, decoders, workers, WASM, and route-triggered resources.
- Replaying source behavior through HTTP instead of relying on `file://`, which breaks many modern front-end runtimes.
- Separating visual dependencies from analytics, tracking, chat widgets, and other non-essential noise.
- Comparing official and local pages with runtime evidence: console/network state, canvas/video/image counts, scroll states, and timeline snapshots.
- Capturing the exact variant a user sees in their own browser when login state, cookies, CMS content, region, or A/B buckets matter.

## When to use it

Use this Skill for requests such as:

- “1:1 复刻这个官网”
- “动效要和原站一样，不要自己重做”
- “把这个 WebGL / Rive / Lottie 页面本地化”
- “这个复刻版和官网不一致，继续修到一致”
- “用我 Chrome 里看到的登录态页面做准”
- “把官网源码打包成可运行 H5 项目”

Do not use it for generic landing pages, mood-board-inspired designs, or new visual concepts where a fresh implementation is acceptable.

## Package layout

```text
.trae/skills/official-site-replica/
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

The installed folder still uses the historical slug `official-site-replica` for compatibility. The public-facing name is now `Site Runtime Mirror`.

## Typical workflow

1. Inspect the official HTML and identify the runtime entry points.
2. Capture the page in a browser to see the real network graph, dynamic chunks, animation files, media, and runtime state.
3. Identify what actually renders the target effect: DOM, Canvas, WebGL, Rive, Lottie, video, or a mix of several layers.
4. Mirror the required assets locally while preserving path and route assumptions.
5. Serve the result over HTTP, preferably from `/` with `index.html` when the source page also runs from `/`.
6. Compare official and local states at multiple moments instead of trusting one screenshot.
7. Fix unexplained missing resources, console errors, stuck loaders, and state mismatches before calling the replica finished.

## Logged-in variants

Some sites change by login state, cookies, localStorage, region, viewport, browser profile, or experiment bucket. In those cases, an anonymous headless capture may not match the page the user is actually judging.

When the user's Chrome view is the target, treat that browser session as the source of truth. Capture only the visual/runtime inputs needed for reproduction, such as rendered DOM, loaded resources, viewport, visible text, and safe runtime config. Do not store credentials, cookies, private tokens, or unrelated personal data.

## Verification bar

A replica is not done just because the page opens. At minimum, check:

- no unexplained local `404`, `403`, or `5xx` responses;
- no unhandled runtime exceptions;
- expected canvas, video, image, model, font, and animation assets are present;
- key DOM state, route, viewport, scroll position, and visible text match the target state;
- animation-heavy pages are compared across several timeline frames;
- authenticated or personalized snapshots remain stable without calling private live APIs again.

## Distributables

- `dist/official-site-replica.skill`: installable Skill package, kept under the original slug for compatibility.
- `dist/official-site-replica-skill-source.zip`: source package, including evals.
- `manifest/official-site-replica-package-manifest.json`: package inventory and checksums.

## Notes on usage

Mirrored website assets may be copyrighted or license-restricted. Keep replicas private unless the user has permission to redistribute the source site's scripts, fonts, images, videos, models, and animation files.

This Skill is a workflow guide, not a bundle of third-party site assets. The repository stores reusable instructions, verification scripts, and checklists only.
