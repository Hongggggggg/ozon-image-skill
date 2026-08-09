#!/usr/bin/env python3
"""Prepare, render, and validate an eight-image Russian Ozon product set."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover - exercised by runtime environment
    raise SystemExit("Pillow is required. Install it in the active Python environment: pip install pillow") from exc


CANVAS = (1200, 1600)
MAX_FILE_BYTES = 10 * 1024 * 1024
SUPPORTED_CATEGORIES = {
    "footwear",
    "home",
    "kitchen",
    "tools-garden",
    "electronics-accessories",
    "sports-outdoor",
    "pet-accessories",
}
REQUIRED_SLIDE_TYPES = {"hero", "white-background", "scene", "benefits", "dimensions", "details"}
ADAPTIVE_SLIDE_TYPES = {"package", "usage", "materials", "scene", "brand", "comparison"}
PROHIBITED_COPY = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"скидк",
        r"\bакци[яи]\b",
        r"хит\s+продаж",
        r"\bкупи(?:ть|те)?\b",
        r"\bзакаж(?:и|ите|ите сейчас)?\b",
        r"\b№\s*1\b",
        r"\bлучш(?:ий|ая|ее|ие)\b",
        r"\b(?:руб\.?|₽|доллар|\$|€)\b",
        r"https?://|www\.|@[A-Za-z0-9_]",
    )
]
HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
LATIN_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9._-]*")
CYRILLIC = re.compile(r"[А-Яа-яЁё]")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("Manifest root must be a JSON object")
    return value


def save_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    temporary.replace(path)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def list_of_nonempty(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty(item) for item in value)


def resolve_path(value: str | None, base: Path) -> str | None:
    if not value:
        return value
    path = Path(value)
    if not path.is_absolute():
        path = base / path
    return str(path.resolve())


def normalize_paths(manifest: dict[str, Any], base: Path) -> None:
    product = manifest.get("product", {})
    product["source_images"] = [resolve_path(item, base) for item in product.get("source_images", [])]
    brand = product.get("brand")
    if isinstance(brand, dict) and brand.get("logo"):
        brand["logo"] = resolve_path(brand["logo"], base)
    fonts = manifest.get("design", {}).get("fonts", {})
    if isinstance(fonts, dict):
        for key in ("regular", "bold"):
            if fonts.get(key):
                fonts[key] = resolve_path(fonts[key], base)
    for slide in manifest.get("slides", []):
        for key in ("base_image", "logo", "rendered_file"):
            if slide.get(key):
                slide[key] = resolve_path(slide[key], base)
        for layer in slide.get("product_layers", []):
            if isinstance(layer, dict) and layer.get("image"):
                layer["image"] = resolve_path(layer["image"], base)
        for detail in slide.get("detail_circles", []):
            if detail.get("image"):
                detail["image"] = resolve_path(detail["image"], base)


def shopper_texts(manifest: dict[str, Any]) -> Iterable[tuple[str, str]]:
    product = manifest.get("product", {})
    for key in ("name_ru", "color", "material", "quantity"):
        if nonempty(product.get(key)):
            yield f"product.{key}", product[key]
    for index, item in enumerate(product.get("package_contents", [])):
        yield f"product.package_contents[{index}]", item
    for index, item in enumerate(product.get("dimensions", [])):
        if isinstance(item, dict):
            for key in ("label", "value"):
                if nonempty(item.get(key)):
                    yield f"product.dimensions[{index}].{key}", item[key]
    for slide in manifest.get("slides", []):
        prefix = f"slides[{slide.get('index', '?')}]"
        for key in ("title", "subtitle"):
            if nonempty(slide.get(key)):
                yield f"{prefix}.{key}", slide[key]
        for index, item in enumerate(slide.get("bullets", [])):
            if nonempty(item):
                yield f"{prefix}.bullets[{index}]", item
        for index, item in enumerate(slide.get("dimensions", [])):
            if isinstance(item, dict):
                for key in ("label", "value"):
                    if nonempty(item.get(key)):
                        yield f"{prefix}.dimensions[{index}].{key}", item[key]
        for index, item in enumerate(slide.get("detail_circles", [])):
            if isinstance(item, dict) and nonempty(item.get("label")):
                yield f"{prefix}.detail_circles[{index}].label", item["label"]
        for index, item in enumerate(slide.get("text_blocks", [])):
            if isinstance(item, dict) and nonempty(item.get("text")):
                yield f"{prefix}.text_blocks[{index}].text", item["text"]


def validate_point(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(isinstance(item, (int, float)) and 0 <= item <= 1 for item in value)
    )


def validate_manifest(manifest: dict[str, Any], phase: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not nonempty(manifest.get("sku")):
        errors.append("sku is required")
    if manifest.get("category") not in SUPPORTED_CATEGORIES:
        errors.append("category must be one of: " + ", ".join(sorted(SUPPORTED_CATEGORIES)))

    product = manifest.get("product")
    if not isinstance(product, dict):
        errors.append("product must be an object")
        product = {}
    for key in ("name_source", "name_ru", "color", "material", "quantity"):
        if not nonempty(product.get(key)):
            errors.append(f"product.{key} is required")
    for key in ("package_contents", "source_images", "identity_lock"):
        if not list_of_nonempty(product.get(key)):
            errors.append(f"product.{key} must be a non-empty list of strings")
    dimensions = product.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions:
        errors.append("product.dimensions must contain at least one supplied measurement")
    else:
        for index, item in enumerate(dimensions):
            if not isinstance(item, dict) or not nonempty(item.get("label")) or not nonempty(item.get("value")):
                errors.append(f"product.dimensions[{index}] needs label and value")

    brand = product.get("brand", {})
    if brand is not None and not isinstance(brand, dict):
        errors.append("product.brand must be an object or omitted")
        brand = {}
    if isinstance(brand, dict) and brand.get("logo") and not nonempty(brand.get("name")):
        errors.append("a logo requires product.brand.name; do not invent an unnamed brand")

    source_images = product.get("source_images", []) if isinstance(product.get("source_images"), list) else []
    for item in source_images:
        if nonempty(item) and not Path(item).is_file():
            errors.append(f"source image not found: {item}")
    if isinstance(brand, dict) and nonempty(brand.get("logo")) and not Path(brand["logo"]).is_file():
        errors.append(f"brand logo not found: {brand['logo']}")
    identity_strategy = product.get("identity_strategy", "reference-guided")
    if identity_strategy not in {"reference-guided", "source-pixel-composite"}:
        errors.append("product.identity_strategy must be reference-guided or source-pixel-composite")

    facts = manifest.get("facts")
    fact_ids: set[str] = set()
    if not isinstance(facts, list) or not facts:
        errors.append("facts must be a non-empty fact ledger")
        facts = []
    for index, fact in enumerate(facts):
        if not isinstance(fact, dict):
            errors.append(f"facts[{index}] must be an object")
            continue
        fact_id = fact.get("id")
        if not nonempty(fact_id):
            errors.append(f"facts[{index}].id is required")
        elif fact_id in fact_ids:
            errors.append(f"duplicate fact id: {fact_id}")
        else:
            fact_ids.add(fact_id)
        if not nonempty(fact.get("value")) or not nonempty(fact.get("source")) or fact.get("confirmed") is not True:
            errors.append(f"facts[{index}] needs value, source, and confirmed=true")

    design = manifest.get("design")
    if not isinstance(design, dict):
        errors.append("design must be an object")
        design = {}
    palette = design.get("palette")
    if not isinstance(palette, dict):
        errors.append("design.palette must be an object")
        palette = {}
    for key in ("primary", "secondary", "accent", "text"):
        if not isinstance(palette.get(key), str) or not HEX_COLOR.match(palette.get(key, "")):
            errors.append(f"design.palette.{key} must be a six-digit hex color")

    slides = manifest.get("slides")
    if not isinstance(slides, list) or len(slides) != 8:
        errors.append("slides must contain exactly eight entries")
        slides = []
    indices = [slide.get("index") for slide in slides if isinstance(slide, dict)]
    if sorted(indices) != list(range(1, 9)):
        errors.append("slide indexes must be exactly 1 through 8")
    filenames: set[str] = set()
    slide_types: list[str] = []
    for slide in slides:
        if not isinstance(slide, dict):
            errors.append("each slide must be an object")
            continue
        index = slide.get("index", "?")
        slide_type = slide.get("type")
        slide_types.append(slide_type)
        if slide_type not in REQUIRED_SLIDE_TYPES | ADAPTIVE_SLIDE_TYPES:
            errors.append(f"slide {index}: unsupported type {slide_type!r}")
        filename = slide.get("filename")
        if not nonempty(filename) or not re.match(r"^0[1-8]-[a-z0-9-]+\.png$", filename):
            errors.append(f"slide {index}: filename must look like 01-hero.png")
        elif filename in filenames:
            errors.append(f"slide {index}: duplicate filename {filename}")
        else:
            filenames.add(filename)
        for key in ("layout", "generation_prompt"):
            if not nonempty(slide.get(key)):
                errors.append(f"slide {index}: {key} is required")
        for key in ("bullets", "claims"):
            if not isinstance(slide.get(key), list):
                errors.append(f"slide {index}: {key} must be a list")
        for claim in slide.get("claims", []):
            if claim not in fact_ids:
                errors.append(f"slide {index}: claim {claim!r} is absent from the confirmed fact ledger")
        if len(source_images) == 1 and slide.get("requires_new_angle") is True:
            errors.append(f"slide {index}: a new angle is forbidden with one source image")
        product_layers = slide.get("product_layers", [])
        if not isinstance(product_layers, list):
            errors.append(f"slide {index}: product_layers must be a list")
            product_layers = []
        if identity_strategy == "source-pixel-composite" and not product_layers:
            errors.append(f"slide {index}: source-pixel-composite requires at least one product layer")
        for layer_number, layer in enumerate(product_layers, start=1):
            if not isinstance(layer, dict):
                errors.append(f"slide {index}: product layer {layer_number} must be an object")
                continue
            layer_image = layer.get("image")
            if not nonempty(layer_image):
                errors.append(f"slide {index}: product layer {layer_number} needs image")
            elif not Path(layer_image).is_file():
                errors.append(f"slide {index}: product layer image not found: {layer_image}")
            elif identity_strategy == "source-pixel-composite":
                if str(Path(layer_image).resolve()) not in {str(Path(item).resolve()) for item in source_images if nonempty(item)}:
                    errors.append(f"slide {index}: locked product layer must come from product.source_images")
                else:
                    try:
                        with Image.open(layer_image) as layer_source:
                            if "A" not in layer_source.getbands() and "transparency" not in layer_source.info:
                                errors.append(f"slide {index}: locked product layer must have transparency")
                    except OSError:
                        errors.append(f"slide {index}: product layer image cannot be opened: {layer_image}")
            for coordinate in ("x", "y"):
                value = layer.get(coordinate)
                if not isinstance(value, (int, float)) or not 0 <= value <= 1:
                    errors.append(f"slide {index}: product layer {coordinate} must be between 0 and 1")
            width = layer.get("width")
            if not isinstance(width, (int, float)) or not 0 < width <= 1:
                errors.append(f"slide {index}: product layer width must be greater than 0 and at most 1")
            rotation = layer.get("rotation", 0)
            if not isinstance(rotation, (int, float)) or not -15 <= rotation <= 15:
                errors.append(f"slide {index}: product layer rotation must be between -15 and 15 degrees")
        if slide_type == "comparison":
            sources = slide.get("comparison_sources")
            if not isinstance(sources, list) or len(sources) < 2 or not all(nonempty(item) for item in sources):
                errors.append(f"slide {index}: comparison requires at least two sourced sides")
        if slide_type == "dimensions":
            annotations = slide.get("dimensions")
            if not isinstance(annotations, list) or not annotations:
                errors.append(f"slide {index}: dimension annotations are required")
            else:
                for annotation in annotations:
                    if not isinstance(annotation, dict) or not validate_point(annotation.get("from")) or not validate_point(annotation.get("to")):
                        errors.append(f"slide {index}: each dimension needs normalized from/to points")
        if slide_type == "details":
            circles = slide.get("detail_circles")
            if not isinstance(circles, list) or not circles:
                errors.append(f"slide {index}: details requires at least one real-image detail circle")
            else:
                for circle in circles:
                    if not isinstance(circle, dict) or not nonempty(circle.get("image")) or not validate_point(circle.get("center")):
                        errors.append(f"slide {index}: each detail circle needs image and normalized center")
        if phase in {"render", "validate"}:
            if not nonempty(slide.get("base_image")) or not Path(slide["base_image"]).is_file():
                errors.append(f"slide {index}: base_image is missing or not found")
        for circle in slide.get("detail_circles", []):
            if isinstance(circle, dict) and nonempty(circle.get("image")) and not Path(circle["image"]).is_file():
                errors.append(f"slide {index}: detail image not found: {circle['image']}")

    missing_types = REQUIRED_SLIDE_TYPES - set(slide_types)
    if missing_types:
        errors.append("required slide types missing: " + ", ".join(sorted(missing_types)))
    if len(slides) == 8 and any(item not in ADAPTIVE_SLIDE_TYPES for item in slide_types[6:8]):
        errors.append("slides 7 and 8 must use adaptive page types")

    allowed_latin = {"Ozon"}
    for item in manifest.get("allowed_non_russian_terms", []):
        if nonempty(item):
            allowed_latin.add(item)
    if isinstance(brand, dict) and nonempty(brand.get("name")):
        allowed_latin.update(LATIN_TOKEN.findall(brand["name"]))
    if nonempty(product.get("model")):
        allowed_latin.update(LATIN_TOKEN.findall(product["model"]))
    allowed_latin_lower = {item.lower() for item in allowed_latin}
    for path, text in shopper_texts(manifest):
        if not CYRILLIC.search(text) and not all(token.lower() in allowed_latin_lower for token in LATIN_TOKEN.findall(text)):
            errors.append(f"{path}: added shopper copy must be Russian")
        for token in LATIN_TOKEN.findall(text):
            if token.lower() not in allowed_latin_lower:
                errors.append(f"{path}: unapproved Latin token {token!r}")
        for pattern in PROHIBITED_COPY:
            if pattern.search(text):
                errors.append(f"{path}: prohibited promotional or contact copy {text!r}")

    if phase == "validate":
        manual = manifest.get("manual_qa")
        if not isinstance(manual, dict):
            errors.append("manual_qa must be an object")
        else:
            for key in ("product_identity", "style_consistency", "russian_proofread", "platform_rules"):
                if manual.get(key) is not True:
                    errors.append(f"manual_qa.{key} must be true after visual review")
        platform = manifest.get("platform_check")
        if not isinstance(platform, dict):
            errors.append("platform_check must record the current official rule review or conservative fallback")
        else:
            for key in ("url", "checked_at", "category_decision", "status"):
                if not nonempty(platform.get(key)):
                    errors.append(f"platform_check.{key} is required")
            platform_status = platform.get("status")
            if platform_status not in {"verified", "conservative-fallback"}:
                errors.append("platform_check.status must be verified or conservative-fallback")
            if platform_status == "conservative-fallback":
                if not nonempty(platform.get("retrieval_error")):
                    errors.append("platform_check.retrieval_error is required for conservative-fallback")
                hero = next((item for item in slides if item.get("type") == "hero"), {})
                if hero.get("text_allowed", True) is not False:
                    errors.append("conservative-fallback requires a text-free hero")
                warnings.append("official Ozon rules were not retrievable; a conservative text-free hero was used and upload-time recheck remains mandatory")

    return errors, warnings


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._").lower()
    return slug or "product"


def unique_directory(path: Path) -> Path:
    if not path.exists():
        return path
    number = 2
    while True:
        candidate = path.with_name(f"{path.name}-v{number}")
        if not candidate.exists():
            return candidate
        number += 1


def unique_file(path: Path) -> Path:
    if not path.exists():
        return path
    number = 2
    while True:
        candidate = path.with_name(f"{path.stem}-v{number}{path.suffix}")
        if not candidate.exists():
            return candidate
        number += 1


def write_prompts(path: Path, manifest: dict[str, Any]) -> None:
    invariants = manifest.get("product", {}).get("identity_lock", [])
    lines = ["# Text-free image-generation prompts", "", "Shared product identity lock:"]
    lines.extend(f"- {item}" for item in invariants)
    lines.append("")
    for slide in sorted(manifest.get("slides", []), key=lambda item: item.get("index", 0)):
        lines.extend(
            [
                f"## {slide.get('index')}. {slide.get('type')}",
                "",
                slide.get("generation_prompt", ""),
                "",
                "Mandatory: text-free base; no invented logo, watermark, badge, new part, new angle, quantity change, color change, or unsupported product variation.",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def command_prepare(args: argparse.Namespace) -> int:
    source = Path(args.manifest).resolve()
    manifest = load_json(source)
    normalize_paths(manifest, source.parent)
    errors, warnings = validate_manifest(manifest, "prepare")
    if errors:
        print_issues(errors, warnings)
        return 2
    workspace = Path(args.workspace).resolve()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    job_dir = unique_directory(workspace / "output" / "ozon" / f"{slugify(manifest['sku'])}-{stamp}")
    job_dir.mkdir(parents=True, exist_ok=False)
    output_manifest = job_dir / "production-manifest.json"
    save_json(output_manifest, manifest)
    write_prompts(job_dir / "image-prompts.md", manifest)
    print(f"Prepared: {job_dir}")
    if warnings:
        print_issues([], warnings)
    return 0


def color(value: str, fallback: str) -> str:
    return value if isinstance(value, str) and HEX_COLOR.match(value) else fallback


def font_candidates(explicit: str | None, bold: bool) -> list[Path]:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if bold:
        candidates.extend(
            [Path(r"C:\Windows\Fonts\arialbd.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")]
        )
    else:
        candidates.extend(
            [Path(r"C:\Windows\Fonts\arial.ttf"), Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")]
        )
    return candidates


def load_font(manifest: dict[str, Any], size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    fonts = manifest.get("design", {}).get("fonts", {})
    explicit = fonts.get("bold" if bold else "regular") if isinstance(fonts, dict) else None
    for candidate in font_candidates(explicit, bold):
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int, max_lines: int = 4) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if draw.textbbox((0, 0), trial, font=font)[2] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textbbox((0, 0), last + "…", font=font)[2] > max_width:
            last = last[:-1]
        lines[-1] = last.rstrip() + "…"
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
    width: int,
    max_lines: int = 4,
    spacing: int = 10,
    align: str = "left",
) -> int:
    lines = wrap_text(draw, text, font, width, max_lines)
    y = xy[1]
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = xy[0]
        if align == "center":
            x += max(0, (width - line_width) // 2)
        elif align == "right":
            x += max(0, width - line_width)
        draw.text((x, y), line, font=font, fill=fill)
        y += bbox[3] - bbox[1] + spacing
    return y


def add_overlay(image: Image.Image, box: tuple[int, int, int, int], fill: tuple[int, int, int, int], radius: int = 0) -> None:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    layer_draw = ImageDraw.Draw(layer)
    if radius:
        layer_draw.rounded_rectangle(box, radius=radius, fill=fill)
    else:
        layer_draw.rectangle(box, fill=fill)
    image.alpha_composite(layer)


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], fill: str, width: int = 6) -> None:
    draw.line((start, end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    for point, direction in ((start, angle), (end, angle + math.pi)):
        for delta in (-0.5, 0.5):
            tip = (
                int(point[0] + 24 * math.cos(direction + delta)),
                int(point[1] + 24 * math.sin(direction + delta)),
            )
            draw.line((point, tip), fill=fill, width=width)


def normalized_point(value: list[float]) -> tuple[int, int]:
    return int(value[0] * CANVAS[0]), int(value[1] * CANVAS[1])


def draw_logo(image: Image.Image, path_value: str | None) -> None:
    if not path_value:
        return
    logo_path = Path(path_value)
    if not logo_path.is_file():
        return
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((260, 120), Image.Resampling.LANCZOS)
    image.alpha_composite(logo, (CANVAS[0] - logo.width - 70, 55))


def draw_product_layers(image: Image.Image, slide: dict[str, Any]) -> None:
    """Composite unchanged transparent source pixels before deterministic annotations."""
    for item in slide.get("product_layers", []):
        source = Image.open(item["image"]).convert("RGBA")
        target_width = max(1, int(float(item["width"]) * CANVAS[0]))
        target_height = max(1, round(source.height * target_width / source.width))
        layer = source.resize((target_width, target_height), Image.Resampling.LANCZOS)
        rotation = float(item.get("rotation", 0))
        if rotation:
            layer = layer.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)
        center_x = int(float(item["x"]) * CANVAS[0])
        center_y = int(float(item["y"]) * CANVAS[1])
        position = (center_x - layer.width // 2, center_y - layer.height // 2)
        if item.get("shadow") is True:
            alpha = layer.getchannel("A")
            shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
            shadow.putalpha(alpha.filter(ImageFilter.GaussianBlur(radius=max(6, layer.width // 70))))
            dark = Image.new("RGBA", layer.size, (12, 23, 28, 85))
            dark.putalpha(shadow.getchannel("A").point(lambda value: value * 85 // 255))
            image.alpha_composite(dark, (position[0] + 18, position[1] + 24))
        image.alpha_composite(layer, position)


def draw_standard_copy(image: Image.Image, slide: dict[str, Any], manifest: dict[str, Any]) -> None:
    if slide.get("text_allowed", True) is False or slide.get("type") == "white-background":
        return
    draw = ImageDraw.Draw(image)
    palette = manifest.get("design", {}).get("palette", {})
    primary = color(palette.get("primary"), "#2A2240")
    secondary = color(palette.get("secondary"), "#F5F0E8")
    accent = color(palette.get("accent"), "#F2A33A")
    text_color = color(palette.get("text"), "#FFFFFF")
    slide_type = slide.get("type")
    title = slide.get("title", "")
    subtitle = slide.get("subtitle", "")
    bullets = slide.get("bullets", [])
    title_font = load_font(manifest, 86 if slide_type == "hero" else 68, bold=True)
    subtitle_font = load_font(manifest, 42, bold=True)
    body_font = load_font(manifest, 35, bold=False)

    if slide_type == "hero":
        add_overlay(image, (0, 0, CANVAS[0], 430), (12, 12, 18, 145))
        y = draw_wrapped(draw, (70, 55), title, title_font, text_color, 930, max_lines=3, spacing=6)
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            width = min(900, bbox[2] - bbox[0] + 56)
            add_overlay(image, (70, y + 18, 70 + width, y + 88), tuple(ImageColor_getrgb(accent)) + (235,), radius=20)
            draw.text((98, y + 29), subtitle, font=subtitle_font, fill=primary)
    elif slide_type in {"benefits", "package", "usage", "materials", "brand", "comparison"}:
        add_overlay(image, (45, 45, CANVAS[0] - 45, 270), (15, 15, 20, 165), radius=34)
        draw_wrapped(draw, (80, 72), title, title_font, text_color, 1040, max_lines=2)
        if subtitle:
            draw_wrapped(draw, (82, 205), subtitle, subtitle_font, accent, 1000, max_lines=1)
        if bullets:
            card_height = 105
            start_y = CANVAS[1] - 70 - card_height * len(bullets) - 18 * (len(bullets) - 1)
            for index, bullet in enumerate(bullets[:4]):
                top = start_y + index * (card_height + 18)
                add_overlay(image, (60, top, CANVAS[0] - 60, top + card_height), (255, 255, 255, 222), radius=28)
                draw.ellipse((86, top + 34, 118, top + 66), fill=accent)
                draw_wrapped(draw, (145, top + 25), bullet, body_font, primary, 930, max_lines=2, spacing=4)
    else:
        add_overlay(image, (45, 45, CANVAS[0] - 45, 250), (15, 15, 20, 160), radius=34)
        draw_wrapped(draw, (80, 72), title, title_font, text_color, 1040, max_lines=2)
        if subtitle:
            draw_wrapped(draw, (82, 188), subtitle, subtitle_font, accent, 1000, max_lines=1)

    draw_logo(image, slide.get("logo") or manifest.get("product", {}).get("brand", {}).get("logo"))


def ImageColor_getrgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]


def draw_dimensions(image: Image.Image, slide: dict[str, Any], manifest: dict[str, Any]) -> None:
    if slide.get("type") != "dimensions" or slide.get("text_allowed", True) is False:
        return
    draw = ImageDraw.Draw(image)
    palette = manifest.get("design", {}).get("palette", {})
    accent = color(palette.get("accent"), "#F2A33A")
    primary = color(palette.get("primary"), "#2A2240")
    font = load_font(manifest, 34, bold=True)
    for annotation in slide.get("dimensions", []):
        start = normalized_point(annotation["from"])
        end = normalized_point(annotation["to"])
        draw_arrow(draw, start, end, accent)
        label = " ".join(item for item in (annotation.get("label"), annotation.get("value")) if nonempty(item))
        point = normalized_point(annotation.get("text_at", [(annotation["from"][0] + annotation["to"][0]) / 2, (annotation["from"][1] + annotation["to"][1]) / 2]))
        bbox = draw.textbbox((0, 0), label, font=font)
        width = bbox[2] - bbox[0] + 34
        height = bbox[3] - bbox[1] + 24
        add_overlay(image, (point[0] - width // 2, point[1] - height // 2, point[0] + width // 2, point[1] + height // 2), (255, 255, 255, 232), radius=16)
        draw.text((point[0] - width // 2 + 17, point[1] - height // 2 + 9), label, font=font, fill=primary)


def draw_details(image: Image.Image, slide: dict[str, Any], manifest: dict[str, Any]) -> None:
    if slide.get("type") != "details" or slide.get("text_allowed", True) is False:
        return
    palette = manifest.get("design", {}).get("palette", {})
    accent = color(palette.get("accent"), "#F2A33A")
    primary = color(palette.get("primary"), "#2A2240")
    draw = ImageDraw.Draw(image)
    font = load_font(manifest, 30, bold=True)
    for item in slide.get("detail_circles", [])[:4]:
        radius = int(item.get("radius", 0.13) * CANVAS[0])
        center = normalized_point(item["center"])
        source_rgba = Image.open(item["image"]).convert("RGBA")
        source = Image.new("RGB", source_rgba.size, "white")
        source.paste(source_rgba, mask=source_rgba.getchannel("A"))
        crop_values = item.get("crop", [0, 0, 1, 1])
        crop = (
            int(crop_values[0] * source.width),
            int(crop_values[1] * source.height),
            int(crop_values[2] * source.width),
            int(crop_values[3] * source.height),
        )
        detail = ImageOps.fit(source.crop(crop), (radius * 2, radius * 2), Image.Resampling.LANCZOS)
        mask = Image.new("L", detail.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0, detail.width - 1, detail.height - 1), fill=255)
        image.paste(detail.convert("RGBA"), (center[0] - radius, center[1] - radius), mask)
        draw.ellipse((center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius), outline=accent, width=10)
        label = item.get("label", "")
        if label:
            bbox = draw.textbbox((0, 0), label, font=font)
            width = min(420, bbox[2] - bbox[0] + 28)
            top = center[1] + radius + 14
            add_overlay(image, (center[0] - width // 2, top, center[0] + width // 2, top + 58), (255, 255, 255, 232), radius=14)
            draw.text((center[0] - width // 2 + 14, top + 10), label, font=font, fill=primary)


def draw_text_blocks(image: Image.Image, slide: dict[str, Any], manifest: dict[str, Any]) -> None:
    if slide.get("text_allowed", True) is False:
        return
    draw = ImageDraw.Draw(image)
    for item in slide.get("text_blocks", []):
        x = int(item.get("x", 0.05) * CANVAS[0])
        y = int(item.get("y", 0.05) * CANVAS[1])
        width = int(item.get("width", 0.9) * CANVAS[0])
        font = load_font(manifest, int(item.get("font_size", 42)), bold=item.get("bold", False))
        fill = color(item.get("color"), "#FFFFFF")
        background = item.get("background")
        if isinstance(background, str) and HEX_COLOR.match(background):
            add_overlay(image, (x - 16, y - 12, x + width + 16, y + int(item.get("height", 0.08) * CANVAS[1])), tuple(ImageColor_getrgb(background)) + (220,), radius=int(item.get("radius", 18)))
        draw_wrapped(draw, (x, y), item["text"], font, fill, width, max_lines=int(item.get("max_lines", 3)), align=item.get("align", "left"))


def render_slide(slide: dict[str, Any], manifest: dict[str, Any], output_path: Path) -> None:
    base = Image.open(slide["base_image"]).convert("RGB")
    image = ImageOps.fit(base, CANVAS, Image.Resampling.LANCZOS, centering=(0.5, 0.5)).convert("RGBA")
    draw_product_layers(image, slide)
    draw_standard_copy(image, slide, manifest)
    draw_dimensions(image, slide, manifest)
    draw_details(image, slide, manifest)
    draw_text_blocks(image, slide, manifest)
    final = Image.new("RGB", CANVAS, "white")
    final.paste(image, mask=image.getchannel("A"))
    final.save(output_path, format="PNG", optimize=True)


def command_render(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    manifest = load_json(manifest_path)
    normalize_paths(manifest, manifest_path.parent)
    errors, warnings = validate_manifest(manifest, "render")
    if errors:
        print_issues(errors, warnings)
        return 2
    for slide in sorted(manifest["slides"], key=lambda item: item["index"]):
        output_path = unique_file(manifest_path.parent / slide["filename"])
        render_slide(slide, manifest, output_path)
        slide["rendered_file"] = str(output_path.resolve())
        print(f"Rendered: {output_path.name}")
    save_json(manifest_path, manifest)
    return 0


def create_contact_sheet(paths: list[Path], output: Path) -> None:
    cell_width, cell_height = 300, 420
    sheet = Image.new("RGB", (cell_width * 4, cell_height * 2), "#D9D9D9")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 20) if Path(r"C:\Windows\Fonts\arial.ttf").is_file() else ImageFont.load_default()
    for index, path in enumerate(paths):
        image = Image.open(path).convert("RGB")
        thumb = ImageOps.fit(image, (280, 373), Image.Resampling.LANCZOS)
        x = (index % 4) * cell_width + 10
        y = (index // 4) * cell_height + 36
        sheet.paste(thumb, (x, y))
        draw.text((x, 8 + (index // 4) * cell_height), path.name, font=font, fill="black")
    sheet.save(output, format="JPEG", quality=90, optimize=True)


def command_validate(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    manifest = load_json(manifest_path)
    normalize_paths(manifest, manifest_path.parent)
    errors, warnings = validate_manifest(manifest, "validate")
    rendered: list[Path] = []
    for slide in sorted(manifest.get("slides", []), key=lambda item: item.get("index", 0)):
        value = slide.get("rendered_file")
        if not nonempty(value):
            errors.append(f"slide {slide.get('index')}: rendered_file is missing; run render")
            continue
        path = Path(value)
        if not path.is_file():
            errors.append(f"slide {slide.get('index')}: rendered file not found: {path}")
            continue
        try:
            with Image.open(path) as image:
                if image.size != CANVAS:
                    errors.append(f"{path.name}: expected 1200x1600, got {image.width}x{image.height}")
                if image.mode not in {"RGB", "RGBA"}:
                    errors.append(f"{path.name}: expected RGB/RGBA, got {image.mode}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.name}: cannot open image: {exc}")
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{path.name}: exceeds 10 MB")
        rendered.append(path)
    if len(rendered) != 8:
        errors.append(f"expected eight rendered images, found {len(rendered)}")

    contact_path = manifest_path.parent / "contact-sheet.jpg"
    if len(rendered) == 8:
        create_contact_sheet(rendered, contact_path)

    status = "PASS" if not errors else "FAIL"
    lines = [
        "# Ozon image-set QA report",
        "",
        f"- Status: **{status}**",
        f"- Checked: {datetime.now().isoformat(timespec='seconds')}",
        f"- Manifest: `{manifest_path}`",
        f"- Rendered images found: {len(rendered)}/8",
        "- Expected canvas: 1200 × 1600 px, RGB/sRGB-oriented PNG, ≤10 MB",
        "- Copy source: deterministic manifest rendering; no model-rendered final Russian text",
        "",
        "## Errors",
        "",
    ]
    lines.extend(f"- {item}" for item in errors) if errors else lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in warnings) if warnings else lines.append("- None")
    lines.extend(
        [
            "",
            "## Required visual review record",
            "",
            f"- Product identity: {manifest.get('manual_qa', {}).get('product_identity') is True}",
            f"- Style consistency: {manifest.get('manual_qa', {}).get('style_consistency') is True}",
            f"- Russian proofreading: {manifest.get('manual_qa', {}).get('russian_proofread') is True}",
            f"- Platform-rule handling reviewed: {manifest.get('manual_qa', {}).get('platform_rules') is True}",
            f"- Platform-check status: {manifest.get('platform_check', {}).get('status', 'missing')}",
            "",
            "Automated checks cannot prove CTR lift or visually certify product identity. The manual gates above are mandatory.",
        ]
    )
    report_path = manifest_path.parent / "qa-report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"QA report: {report_path}")
    if len(rendered) == 8:
        print(f"Contact sheet: {contact_path}")
    print_issues(errors, warnings)
    return 0 if not errors else 2


def print_issues(errors: list[str], warnings: list[str]) -> None:
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)
    for item in warnings:
        print(f"WARNING: {item}", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare = subparsers.add_parser("prepare", help="validate a draft manifest and create a non-overwriting job directory")
    prepare.add_argument("--manifest", required=True, help="draft production-manifest JSON")
    prepare.add_argument("--workspace", default=".", help="project root that will receive output/ozon")
    prepare.set_defaults(handler=command_prepare)
    render = subparsers.add_parser("render", help="render deterministic copy and annotations onto eight text-free bases")
    render.add_argument("--manifest", required=True, help="prepared production-manifest JSON")
    render.set_defaults(handler=command_render)
    validate = subparsers.add_parser("validate", help="validate rendered files and write QA report/contact sheet")
    validate.add_argument("--manifest", required=True, help="rendered production-manifest JSON")
    validate.set_defaults(handler=command_validate)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
