"""Cheap local visual probes for labelled-diagram assessment rows."""

from __future__ import annotations

from collections import Counter
from io import BytesIO

from PIL import Image

from tutorbench_lab.media import load_image
from tutorbench_lab.schemas import ImageRef


def build_visual_probe(ref: ImageRef) -> str | None:
    """Detect simple horizontal marker rows and summarize endpoint colors.

    This is intentionally a lightweight hint, not a replacement for VLM
    perception. It helps the audit stage notice whether a marker endpoint sits
    in interior fill, on a thick border, or on a colored organelle.
    """

    encoded = load_image(ref)
    if encoded is None:
        return None
    image = Image.open(BytesIO(encoded.data)).convert("RGB")
    width, height = image.size
    pixels = image.load()

    max_y = min(height, int(height * 0.62))
    row_threshold = max(50, int(width * 0.04))
    rows = []
    min_y = max(100, int(height * 0.10))
    for y in range(min_y, max_y):
        dark_count = sum(1 for x in range(width) if _is_dark(pixels[x, y]))
        if dark_count >= row_threshold:
            rows.append((y, dark_count))
    clusters = _cluster_rows(rows)
    marker_rows = []
    for cluster in clusters:
        y = max(cluster, key=lambda item: item[1])[0]
        segments = _dark_segments(pixels, width, y)
        if len(segments) < 1:
            continue
        min_x = min(start for start, _ in segments)
        max_x = max(end for _, end in segments)
        if max_x - min_x < width * 0.05:
            continue
        endpoints = []
        for label, x in [("left", min_x), ("right", max_x)]:
            endpoints.append(
                f"{label} endpoint x={x}: {_summarize_endpoint(pixels, width, height, x, y)}"
            )
        marker_rows.append(f"- y={y}: " + "; ".join(endpoints))

    if len(marker_rows) < 3:
        return None
    return (
        "Local visual probe for horizontal marker lines. Use as a concrete "
        "endpoint-color hint; the image still controls final judgment.\n"
        + "\n".join(marker_rows[:12])
    )


def _cluster_rows(rows: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    clusters: list[list[tuple[int, int]]] = []
    for y, count in rows:
        if not clusters or y > clusters[-1][-1][0] + 1:
            clusters.append([])
        clusters[-1].append((y, count))
    return clusters


def _dark_segments(pixels, width: int, y: int) -> list[tuple[int, int]]:
    xs = [x for x in range(width) if _is_dark(pixels[x, y])]
    if not xs:
        return []
    segments = []
    start = prev = xs[0]
    for x in xs[1:]:
        if x == prev + 1:
            prev = x
            continue
        if prev - start >= 10:
            segments.append((start, prev))
        start = prev = x
    if prev - start >= 10:
        segments.append((start, prev))
    return segments


def _summarize_endpoint(pixels, width: int, height: int, x: int, y: int) -> str:
    offsets = [
        (-12, 0),
        (12, 0),
        (0, -12),
        (0, 12),
        (-16, -16),
        (-16, 16),
        (16, -16),
        (16, 16),
        (-24, 0),
        (24, 0),
        (0, -24),
        (0, 24),
    ]
    classes = []
    colors = []
    for dx, dy in offsets:
        xx = x + dx
        yy = y + dy
        if xx < 0 or yy < 0 or xx >= width or yy >= height:
            continue
        rgb = pixels[xx, yy]
        if _is_dark(rgb):
            continue
        classes.append(_classify_color(rgb))
        colors.append(f"rgb{tuple(rgb)}")
    if not classes:
        return "surroundings mostly dark line/marker pixels"
    counts = Counter(classes)
    top = ", ".join(f"{name} x{count}" for name, count in counts.most_common(3))
    sample = ", ".join(colors[:4])
    return f"surroundings {top}; sample colors {sample}"


def _is_dark(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    return r < 80 and g < 80 and b < 100


def _classify_color(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    if r > 248 and g > 248 and b > 248:
        return "white page/outside"
    if r > 220 and g > 235 and b > 235:
        return "light cyan interior fill/cytoplasm"
    if r > 190 and g > 150 and b < 110:
        return "yellow/gold thick border/cell wall"
    if g > 175 and r < 160 and b < 180:
        return "green oval/chloroplast"
    if r < 100 and 95 < g < 165 and 95 < b < 165:
        return "dark teal oval/nucleus"
    if r > 170 and b > 140 and g < 180:
        return "pink oval/mitochondrion"
    if r > 180 and g > 200 and 170 < b < 220:
        return "pale large oval/vacuole"
    if r < 80 and g > 120 and b > 130:
        return "blue/teal outline or membrane"
    return "other colored region"
