#!/usr/bin/env python3
"""
Compare an official animated site against a local replay at multiple timestamps.

Dependencies:
  python -m pip install playwright pillow --break-system-packages
  python -m playwright install chromium

Example:
  python scripts/timeline_compare.py \
    --official https://example.com/ \
    --local http://localhost:8123/ \
    --out comparison
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any


def parse_timestamps(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def parse_viewport(value: str) -> tuple[int, int]:
    width, height = value.lower().split("x", 1)
    return int(width), int(height)


def sampled_pixel_diff(path_a: Path, path_b: Path, step: int = 2, threshold: int = 10) -> dict[str, Any]:
    try:
        from PIL import Image, ImageChops, ImageStat
    except Exception as exc:
        return {"available": False, "error": f"Pillow unavailable: {exc}"}

    image_a = Image.open(path_a).convert("RGB")
    image_b = Image.open(path_b).convert("RGB")

    if image_a.size != image_b.size:
        return {
            "available": True,
            "same_size": False,
            "official_size": image_a.size,
            "local_size": image_b.size,
        }

    diff = ImageChops.difference(image_a, image_b)
    stat = ImageStat.Stat(diff)
    mean = sum(stat.mean) / 3

    pixels = diff.load()
    width, height = diff.size
    sampled = 0
    changed = 0
    for y in range(0, height, step):
        for x in range(0, width, step):
            sampled += 1
            if max(pixels[x, y]) > threshold:
                changed += 1

    return {
        "available": True,
        "same_size": True,
        "mean_channel_diff": round(mean, 4),
        "sampled_pixels": sampled,
        "changed_pixels": changed,
        "sample_diff_ratio": round(changed / sampled, 6) if sampled else None,
        "threshold": threshold,
        "sample_step": step,
    }


def collect_page(label: str, url: str, out_dir: Path, timestamps: list[float], viewport: tuple[int, int]) -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise SystemExit(
            "Playwright is required. Install with:\n"
            "python -m pip install playwright --break-system-packages\n"
            "python -m playwright install chromium\n"
            f"Original error: {exc}"
        )

    result: dict[str, Any] = {
        "label": label,
        "url": url,
        "states": [],
        "console": [],
        "exceptions": [],
        "failed": [],
        "bad_responses": [],
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--ignore-gpu-blocklist"])
        context = browser.new_context(
            viewport={"width": viewport[0], "height": viewport[1]},
            device_scale_factor=1,
            reduced_motion="no-preference",
        )
        page = context.new_page()

        page.on("console", lambda msg: result["console"].append({"type": msg.type, "text": msg.text}))
        page.on("pageerror", lambda exc: result["exceptions"].append(str(exc)))
        page.on("requestfailed", lambda req: result["failed"].append({"url": req.url, "failure": str(req.failure)}))

        def handle_response(response: Any) -> None:
            status = response.status
            if status >= 400:
                result["bad_responses"].append({"status": status, "url": response.url})

        page.on("response", handle_response)

        start = time.monotonic()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        for ts in timestamps:
            delay = ts - (time.monotonic() - start)
            if delay > 0:
                page.wait_for_timeout(int(delay * 1000))

            state = page.evaluate(
                """
                () => {
                  const sample = (x, y) => {
                    const e = document.elementFromPoint(x, y);
                    if (!e) return null;
                    const r = e.getBoundingClientRect();
                    const cs = getComputedStyle(e);
                    return {
                      tag: e.tagName,
                      id: e.id || "",
                      className: String(e.className || ""),
                      text: (e.innerText || e.textContent || "").slice(0, 120),
                      x: Math.round(r.x),
                      y: Math.round(r.y),
                      width: Math.round(r.width),
                      height: Math.round(r.height),
                      opacity: cs.opacity,
                      visibility: cs.visibility
                    };
                  };
                  const visibleHeadings = [...document.querySelectorAll("h1,h2,h3,p,a,button")]
                    .map(e => {
                      const r = e.getBoundingClientRect();
                      const cs = getComputedStyle(e);
                      return {
                        tag: e.tagName,
                        className: String(e.className || ""),
                        text: (e.innerText || e.textContent || "").trim().slice(0, 100),
                        x: Math.round(r.x),
                        y: Math.round(r.y),
                        width: Math.round(r.width),
                        height: Math.round(r.height),
                        opacity: cs.opacity,
                        visibility: cs.visibility
                      };
                    })
                    .filter(e => e.text && e.width > 0 && e.height > 0 && e.y > -200 && e.y < innerHeight + 200)
                    .slice(0, 30);
                  return {
                    href: location.href,
                    pathname: location.pathname,
                    performanceNow: Math.round(performance.now()),
                    scrollX,
                    scrollY,
                    innerWidth,
                    innerHeight,
                    scrollHeight: document.documentElement.scrollHeight,
                    bodyClass: document.body.className,
                    htmlClass: document.documentElement.className,
                    canvasCount: document.querySelectorAll("canvas").length,
                    videoCount: document.querySelectorAll("video").length,
                    imageCount: document.querySelectorAll("img").length,
                    center: sample(Math.floor(innerWidth / 2), Math.floor(innerHeight / 2)),
                    points: [
                      sample(Math.floor(innerWidth / 2), 120),
                      sample(Math.floor(innerWidth / 2), Math.floor(innerHeight / 2)),
                      sample(Math.floor(innerWidth / 2), innerHeight - 120)
                    ],
                    visibleText: visibleHeadings
                  };
                }
                """
            )

            shot_name = f"{label}_{str(ts).replace('.', '_')}s.png"
            shot_path = out_dir / shot_name
            page.screenshot(path=str(shot_path), full_page=False)
            state["screenshot"] = shot_name
            state["timestamp_seconds"] = ts
            result["states"].append(state)

        context.close()
        browser.close()

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--official", required=True, help="Official site URL")
    parser.add_argument("--local", required=True, help="Local replay URL")
    parser.add_argument("--out", required=True, help="Output directory")
    parser.add_argument("--timestamps", default="1,3,6,10", help="Comma-separated seconds after navigation")
    parser.add_argument("--viewport", default="1440x1200", help="Viewport, for example 1440x1200")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamps = parse_timestamps(args.timestamps)
    viewport = parse_viewport(args.viewport)

    official = collect_page("official", args.official, out_dir, timestamps, viewport)
    local = collect_page("local", args.local, out_dir, timestamps, viewport)

    diffs = []
    for official_state, local_state in zip(official["states"], local["states"]):
        official_path = out_dir / official_state["screenshot"]
        local_path = out_dir / local_state["screenshot"]
        diffs.append(
            {
                "timestamp_seconds": official_state["timestamp_seconds"],
                "official_screenshot": official_state["screenshot"],
                "local_screenshot": local_state["screenshot"],
                "pixel_diff": sampled_pixel_diff(official_path, local_path),
                "official_center": official_state.get("center"),
                "local_center": local_state.get("center"),
                "official_scroll_height": official_state.get("scrollHeight"),
                "local_scroll_height": local_state.get("scrollHeight"),
            }
        )

    report = {
        "official": official,
        "local": local,
        "diffs": diffs,
        "summary": {
            "official_console_count": len(official["console"]),
            "local_console_count": len(local["console"]),
            "official_exception_count": len(official["exceptions"]),
            "local_exception_count": len(local["exceptions"]),
            "official_failed_count": len(official["failed"]),
            "local_failed_count": len(local["failed"]),
            "official_bad_response_count": len(official["bad_responses"]),
            "local_bad_response_count": len(local["bad_responses"]),
        },
    }

    (out_dir / "timeline_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Report written to: {out_dir / 'timeline_report.json'}")


if __name__ == "__main__":
    main()
