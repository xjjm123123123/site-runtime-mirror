# Verification Checklist

Use this checklist before claiming that a local replica matches the official site.

## Required evidence

- The local page is served through HTTP, not opened through `file://`.
- If the official page is `/`, the local page is tested from `/` with `index.html`.
- Console exceptions are empty or individually explained.
- Failed requests are empty or individually explained.
- No unexplained 4xx/5xx responses remain for visual/runtime assets.
- Dynamic chunks, animation JSON, media, fonts, decoders, workers, models, and textures are mirrored.
- Loader enters and exits through the original runtime path, or any fallback is explicitly documented.
- Expected Canvas/WebGL/Rive/Lottie/video elements exist and have plausible dimensions.
- The page is not static: two or more frames show expected motion or runtime state changes.

## Timeline comparison

For animation-heavy pages, compare official and local at several timestamps under the same viewport and fresh-profile conditions.

Recommended timestamps:

- `1s`
- `3s`
- `6s`
- `10s`

Record at each timestamp:

- screenshot path
- `scrollY`
- `scrollHeight`
- `document.body.className`
- `document.documentElement.className`
- visible section or central element
- counts of `canvas`, `video`, and `img`
- failed network requests
- bad HTTP responses
- console exceptions

## Stable-frame acceptance

Use screenshots as evidence, not as the only proof. A single screenshot can match while motion is wrong.

For the stable matched frame:

- sampled pixel diff should ideally be below 1%
- dominant visible element should match
- scroll height should be within a small tolerance
- first viewport composition should match
- animation should continue or settle in the same way

If early frames differ but stable frames converge, state the matched timestamp and continue investigating if the user specifically requires the full entry animation.

## Common failure patterns

### Clean console but wrong visual

Likely causes:

- local page is served from a named file instead of `/`
- route/state branch differs
- first-visit storage/cookie differs
- scroll restoration or history state differs
- intro timeline progress differs
- browser profile is dirty

### Loader stuck

Likely causes:

- missing model, texture, font, decoder, or animation file
- wrong capability branch, such as `ktx2` requested but only `webp` mirrored
- rejected promise in original loader
- aborted resource group after first missing file

Fix missing assets before hiding the loader.

### Scroll positions mismatch

Likely causes:

- missing route-triggered media that changes layout height
- missing pinned spacer from GSAP/ScrollTrigger
- wrong viewport/device scale
- script initialized before fonts/media loaded
- route branch mismatch

## Reporting

When the user only wants the final result, keep detailed comparison artifacts internal and continue fixing. Share evidence when:

- the user asks for a comparison
- a blocker prevents full parity
- a fallback was used
- the result is ready and the user needs confidence that runtime parity was checked
