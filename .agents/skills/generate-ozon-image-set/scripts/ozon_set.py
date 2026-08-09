#!/usr/bin/env python3
"""Prepare and validate eight complete AI-generated Russian Ozon listing images."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover
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
SLIDE_TYPES = {
    "hero",
    "decision-overview",
    "white-background",
    "size-fit",
    "dimensions",
    "construction",
    "feature-proof",
    "benefits",
    "details",
    "materials",
    "angles",
    "usage",
    "scene",
    "care",
    "package",
    "configuration",
    "compatibility",
    "brand",
    "comparison",
}
LEGACY_OVERLAY_FIELDS = {
    "base_image",
    "product_layers",
    "detail_circles",
    "dimensions",
    "text_blocks",
    "logo",
    "rendered_file",
}
MANUAL_GATES = (
    "product_identity",
    "style_consistency",
    "russian_text_accuracy",
    "layout_integrity",
    "measurement_alignment",
    "platform_rules",
    "mobile_legibility",
    "information_density",
    "page_uniqueness",
    "color_variety",
)
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


def resolve_path(value: str, base: Path) -> str:
    path = Path(value)
    return str((base / path).resolve() if not path.is_absolute() else path.resolve())


def normalize_paths(manifest: dict[str, Any], base: Path) -> None:
    product = manifest.get("product", {})
    if isinstance(product, dict):
        source_images = product.get("source_images", [])
        if isinstance(source_images, list):
            product["source_images"] = [resolve_path(item, base) for item in source_images if nonempty(item)]
        brand = product.get("brand")
        if isinstance(brand, dict) and nonempty(brand.get("logo")):
            brand["logo"] = resolve_path(brand["logo"], base)
    for slide in manifest.get("slides", []):
        if isinstance(slide, dict) and nonempty(slide.get("final_image")):
            slide["final_image"] = resolve_path(slide["final_image"], base)


def shopper_texts(manifest: dict[str, Any]) -> Iterable[tuple[str, str]]:
    product = manifest.get("product", {})
    for key in ("name_ru", "color", "material", "quantity"):
        if nonempty(product.get(key)):
            yield f"product.{key}", product[key]
    for index, item in enumerate(product.get("package_contents", [])):
        if nonempty(item):
            yield f"product.package_contents[{index}]", item
    for index, item in enumerate(product.get("dimensions", [])):
        if isinstance(item, dict):
            for key in ("label", "value"):
                if nonempty(item.get(key)):
                    yield f"product.dimensions[{index}].{key}", item[key]
    for slide in manifest.get("slides", []):
        if not isinstance(slide, dict):
            continue
        prefix = f"slide[{slide.get('index', '?')}]"
        for key in ("title", "subtitle"):
            if nonempty(slide.get(key)):
                yield f"{prefix}.{key}", slide[key]
        for index, item in enumerate(slide.get("bullets", [])):
            if nonempty(item):
                yield f"{prefix}.bullets[{index}]", item
        for index, item in enumerate(slide.get("information_units", [])):
            if nonempty(item):
                yield f"{prefix}.information_units[{index}]", item


def validate_manifest(manifest: dict[str, Any], phase: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if manifest.get("schema_version") != 2:
        errors.append("schema_version must be 2 for complete-image generation")
    if not nonempty(manifest.get("sku")):
        errors.append("sku is required")
    if manifest.get("category") not in SUPPORTED_CATEGORIES:
        errors.append("category must be one of: " + ", ".join(sorted(SUPPORTED_CATEGORIES)))

    localization = manifest.get("localization_review")
    if not isinstance(localization, dict):
        errors.append("localization_review must record Russian copy review before and after generation")
        localization = {}
    if localization.get("locale") != "ru-RU":
        errors.append("localization_review.locale must be ru-RU")
    if localization.get("pre_generation_approved") is not True:
        errors.append("localization_review.pre_generation_approved must be true before image generation")
    pre_checks = localization.get("pre_generation_checks")
    required_pre_checks = (
        "natural_russian",
        "grammar_and_agreement",
        "ecommerce_fit",
        "fact_alignment",
        "claim_safety",
    )
    if not isinstance(pre_checks, dict):
        errors.append("localization_review.pre_generation_checks must be an object")
    else:
        for key in required_pre_checks:
            if pre_checks.get(key) is not True:
                errors.append(f"localization_review.pre_generation_checks.{key} must be true")

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
        errors.append("product.dimensions must contain at least one supplied measurement or footwear size mapping")
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
    if product.get("identity_strategy", "reference-guided") != "reference-guided":
        errors.append("product.identity_strategy must be reference-guided; post-generation source-pixel compositing is not allowed")

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
            errors.append(f"facts[{index}] needs value, source, and confirmed: true")

    strategy = manifest.get("set_strategy")
    if not isinstance(strategy, dict):
        errors.append("set_strategy must be an object that plans the set from buyer decisions")
        strategy = {}
    for key in ("audience", "typography", "visual_thesis"):
        if not nonempty(strategy.get(key)):
            errors.append(f"set_strategy.{key} is required")
    buyer_questions = strategy.get("buyer_questions", [])
    if not isinstance(buyer_questions, list) or len(buyer_questions) != 8 or not all(nonempty(item) for item in buyer_questions):
        errors.append("set_strategy.buyer_questions must contain exactly eight non-empty questions")
        buyer_questions = []
    elif len({re.sub(r"\s+", " ", item.strip()).casefold() for item in buyer_questions}) != 8:
        errors.append("set_strategy.buyer_questions must be unique")
    palette = strategy.get("palette", [])
    if not isinstance(palette, list) or not 3 <= len(palette) <= 5 or not all(nonempty(item) for item in palette):
        errors.append("set_strategy.palette must contain 3 to 5 non-empty colors")
    priority_fact_ids = strategy.get("priority_fact_ids", [])
    if not list_of_nonempty(priority_fact_ids):
        errors.append("set_strategy.priority_fact_ids must be a non-empty list")
        priority_fact_ids = []
    for fact_id in priority_fact_ids:
        if fact_id not in fact_ids:
            errors.append(f"set_strategy priority fact {fact_id!r} is absent from the confirmed fact ledger")

    slides = manifest.get("slides")
    if not isinstance(slides, list) or len(slides) != 8:
        errors.append("slides must contain exactly eight entries")
        slides = []
    indices = [slide.get("index") for slide in slides if isinstance(slide, dict)]
    if sorted(indices) != list(range(1, 9)):
        errors.append("slide indexes must be exactly 1 through 8")
    filenames: set[str] = set()
    slide_types: list[str] = []
    purposes: set[str] = set()
    slide_questions: set[str] = set()
    used_claims: set[str] = set()
    for slide in slides:
        if not isinstance(slide, dict):
            errors.append("each slide must be an object")
            continue
        index = slide.get("index", "?")
        slide_type = slide.get("type")
        slide_types.append(slide_type)
        if slide_type not in SLIDE_TYPES:
            errors.append(f"slide {index}: unsupported type {slide_type!r}")
        filename = slide.get("filename")
        if not nonempty(filename) or not re.match(r"^0[1-8]-[a-z0-9-]+\.png$", filename):
            errors.append(f"slide {index}: filename must look like 01-hero.png")
        elif filename in filenames:
            errors.append(f"slide {index}: duplicate filename {filename}")
        else:
            filenames.add(filename)
        for key in ("purpose", "buyer_question", "selection_reason", "layout", "generation_prompt"):
            if not nonempty(slide.get(key)):
                errors.append(f"slide {index}: {key} is required")
        for key in ("title", "subtitle", "bullets", "claims", "information_units", "final_image"):
            if key not in slide:
                errors.append(f"slide {index}: {key} key is required")
        purpose_key = re.sub(r"\s+", " ", str(slide.get("purpose", "")).strip()).casefold()
        if purpose_key:
            if purpose_key in purposes:
                errors.append(f"slide {index}: duplicate purpose; merge semantically repeated pages")
            purposes.add(purpose_key)
        question_key = re.sub(r"\s+", " ", str(slide.get("buyer_question", "")).strip()).casefold()
        if question_key:
            if question_key in slide_questions:
                errors.append(f"slide {index}: duplicate buyer_question; every page must answer a distinct question")
            slide_questions.add(question_key)
        information_units = slide.get("information_units")
        if not isinstance(information_units, list) or len(information_units) < 2 or not all(nonempty(item) for item in information_units):
            errors.append(f"slide {index}: information_units must contain at least two meaningful items")
        if not isinstance(slide.get("bullets"), list):
            errors.append(f"slide {index}: bullets must be a list")
        if not isinstance(slide.get("claims"), list):
            errors.append(f"slide {index}: claims must be a list")
        for claim in slide.get("claims", []):
            if claim not in fact_ids:
                errors.append(f"slide {index}: claim {claim!r} is absent from the confirmed fact ledger")
            else:
                used_claims.add(claim)
        present_legacy = sorted(LEGACY_OVERLAY_FIELDS.intersection(slide))
        if present_legacy:
            errors.append(f"slide {index}: legacy overlay fields are forbidden: {', '.join(present_legacy)}")
        if len(source_images) == 1 and slide.get("requires_new_angle") is True:
            errors.append(f"slide {index}: a new angle is forbidden with one source image")
        if slide_type == "comparison":
            sources = slide.get("comparison_sources")
            if not isinstance(sources, list) or len(sources) < 2 or not all(nonempty(item) for item in sources):
                errors.append(f"slide {index}: comparison requires at least two sourced sides")
        if phase == "validate":
            final_image = slide.get("final_image")
            if not nonempty(final_image) or not Path(final_image).is_file():
                errors.append(f"slide {index}: final_image is missing or not found; generate the complete page with AI")

    if slides and isinstance(slides[0], dict) and slides[0].get("type") != "hero":
        errors.append("slide 1 must be the hero; slides 2 through 8 are product-specific")
    for fact_id in priority_fact_ids:
        if fact_id not in used_claims:
            errors.append(f"priority fact {fact_id!r} is not covered by any slide")

    allowed_latin = {"Ozon"}
    for item in manifest.get("allowed_non_russian_terms", []):
        if nonempty(item):
            allowed_latin.add(item)
    if isinstance(brand, dict) and nonempty(brand.get("name")):
        allowed_latin.update(LATIN_TOKEN.findall(brand["name"]))
    if nonempty(product.get("model")):
        allowed_latin.update(LATIN_TOKEN.findall(product["model"]))
    allowed_latin_lower = {item.lower() for item in allowed_latin}
    for path, copy in shopper_texts(manifest):
        latin = LATIN_TOKEN.findall(copy)
        if not CYRILLIC.search(copy) and not all(token.lower() in allowed_latin_lower for token in latin):
            errors.append(f"{path}: shopper copy must be Russian")
        for token in latin:
            if token.lower() not in allowed_latin_lower:
                errors.append(f"{path}: unapproved Latin token {token!r}")
        for pattern in PROHIBITED_COPY:
            if pattern.search(copy):
                errors.append(f"{path}: prohibited promotional or contact copy {copy!r}")

    if phase == "validate":
        if localization.get("post_generation_approved") is not True:
            errors.append("localization_review.post_generation_approved must be true after full-resolution text review")
        slide_checks = localization.get("slide_checks")
        if not isinstance(slide_checks, list) or len(slide_checks) != 8:
            errors.append("localization_review.slide_checks must contain eight slide-by-slide transcription checks")
        else:
            checked_indices: list[int] = []
            for position, check in enumerate(slide_checks):
                if not isinstance(check, dict):
                    errors.append(f"localization_review.slide_checks[{position}] must be an object")
                    continue
                index = check.get("index")
                checked_indices.append(index)
                if check.get("status") != "pass":
                    errors.append(f"localization_review.slide_checks[{position}].status must be pass")
                expected = check.get("expected_text")
                observed = check.get("observed_text")
                if not isinstance(expected, list) or not all(nonempty(item) for item in expected):
                    errors.append(f"localization_review.slide_checks[{position}].expected_text must be a list of exact strings")
                if not isinstance(observed, list) or not all(nonempty(item) for item in observed):
                    errors.append(f"localization_review.slide_checks[{position}].observed_text must transcribe every visible string")
                if isinstance(expected, list) and isinstance(observed, list):
                    normalize = lambda values: [re.sub(r"\s+", " ", str(item).strip()) for item in values]
                    if normalize(expected) != normalize(observed):
                        errors.append(f"localization_review.slide_checks[{position}]: expected and observed text differ")
            if sorted(checked_indices) != list(range(1, 9)):
                errors.append("localization_review.slide_checks indexes must be exactly 1 through 8")
        manual = manifest.get("manual_qa")
        if not isinstance(manual, dict):
            errors.append("manual_qa must be an object")
        else:
            for key in MANUAL_GATES:
                if manual.get(key) is not True:
                    errors.append(f"manual_qa.{key} must be true after full-resolution review")
        platform = manifest.get("platform_check")
        if not isinstance(platform, dict):
            errors.append("platform_check must record the current official rule review or conservative fallback")
        else:
            for key in ("url", "checked_at", "category_decision", "status"):
                if not nonempty(platform.get(key)):
                    errors.append(f"platform_check.{key} is required")
            status = platform.get("status")
            if status not in {"verified", "conservative-fallback"}:
                errors.append("platform_check.status must be verified or conservative-fallback")
            if status == "conservative-fallback":
                if not nonempty(platform.get("retrieval_error")):
                    errors.append("platform_check.retrieval_error is required for conservative-fallback")
                warnings.append("official Ozon rules were not retrievable; conservative content rules were used and upload-time recheck remains mandatory")

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


def exact_copy_block(slide: dict[str, Any]) -> list[str]:
    if slide.get("text_allowed", True) is False:
        return ["Exact shopper-facing text: NONE. Keep this complete page text-free."]
    lines = ["Exact Russian copy to render verbatim in the complete image:"]
    lines.append(f"- Title: {slide.get('title') or '[none]'}")
    lines.append(f"- Subtitle: {slide.get('subtitle') or '[none]'}")
    bullets = slide.get("bullets", [])
    lines.append("- Bullets: " + (" | ".join(bullets) if bullets else "[none]"))
    return lines


def write_prompts(path: Path, manifest: dict[str, Any]) -> None:
    invariants = manifest.get("product", {}).get("identity_lock", [])
    strategy = manifest.get("set_strategy", {})
    lines = [
        "# Complete final-image generation prompts",
        "",
        "Generate each page as a finished 3:4 Ozon listing image in one AI image call.",
        "Do not generate a background template and do not plan any post-generation overlay.",
        "",
        f"Set visual thesis: {strategy.get('visual_thesis', '')}",
        "Palette: " + " | ".join(strategy.get("palette", [])),
        f"Typography: {strategy.get('typography', '')}",
        "",
        "Shared product identity lock:",
    ]
    lines.extend(f"- {item}" for item in invariants)
    lines.append("")
    for slide in sorted(manifest.get("slides", []), key=lambda item: item.get("index", 0)):
        lines.extend(
            [
                f"## {slide.get('index')}. {slide.get('type')}",
                "",
                f"Purpose: {slide.get('purpose', '')}",
                f"Buyer question: {slide.get('buyer_question', '')}",
                f"Selection reason: {slide.get('selection_reason', '')}",
                "Required information units: " + " | ".join(slide.get("information_units", [])),
                "",
                slide.get("generation_prompt", ""),
                "",
            ]
        )
        lines.extend(exact_copy_block(slide))
        lines.extend(
            [
                "",
                "Mandatory composition rules:",
                "- Complete final 1200 × 1600 artwork; no placeholders or blank cards.",
                "- Keep the product or truthful use demonstration visually dominant; never shrink it to create decorative whitespace.",
                "- Target 55–75% meaningful product area on a hero and 45–70% on a supporting page.",
                "- Keep low-detail dead background below roughly 20% of the canvas.",
                "- Make the title readable at search-thumbnail size and body copy readable on a phone.",
                "- Use 3–6 useful information units on a text hero and 4–7 on a supporting information page.",
                "- Keep text outside critical product features while using close, intentional visual grouping.",
                "- No full-width opaque or translucent banner over the product.",
                "- Detail modules must not cover the main product.",
                "- Dimension arrows must touch the true visible extrema of the measured axis.",
                "- Do not repeat the purpose, buyer question, or close-ups of another page.",
                "- No invented logo, watermark, claim, badge, part, angle, quantity, color, or product variation.",
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
    save_json(job_dir / "production-manifest.json", manifest)
    write_prompts(job_dir / "image-prompts.md", manifest)
    print(f"Prepared: {job_dir}")
    print_issues([], warnings)
    return 0


def create_contact_sheet(paths: list[Path], output: Path) -> None:
    cell_width, cell_height = 300, 420
    sheet = Image.new("RGB", (cell_width * 4, cell_height * 2), "#D9D9D9")
    draw = ImageDraw.Draw(sheet)
    font_path = Path(r"C:\Windows\Fonts\arial.ttf")
    font = ImageFont.truetype(str(font_path), 20) if font_path.is_file() else ImageFont.load_default()
    for index, source in enumerate(paths):
        image = Image.open(source).convert("RGB")
        thumb = ImageOps.fit(image, (280, 373), Image.Resampling.LANCZOS)
        x = (index % 4) * cell_width + 10
        y = (index // 4) * cell_height + 36
        sheet.paste(thumb, (x, y))
        draw.text((x, 8 + (index // 4) * cell_height), source.name, font=font, fill="black")
    sheet.save(output, format="JPEG", quality=90, optimize=True)


def command_validate(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    manifest = load_json(manifest_path)
    normalize_paths(manifest, manifest_path.parent)
    errors, warnings = validate_manifest(manifest, "validate")
    final_images: list[Path] = []
    for slide in sorted(manifest.get("slides", []), key=lambda item: item.get("index", 0)):
        value = slide.get("final_image")
        if not nonempty(value):
            continue
        path = Path(value)
        if not path.is_file():
            continue
        try:
            with Image.open(path) as image:
                if image.size != CANVAS:
                    errors.append(f"{path.name}: expected 1200x1600, got {image.width}x{image.height}")
                if image.mode not in {"RGB", "RGBA"}:
                    errors.append(f"{path.name}: expected RGB/RGBA, got {image.mode}")
        except OSError as exc:
            errors.append(f"{path.name}: cannot open image: {exc}")
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{path.name}: exceeds 10 MB")
        final_images.append(path)
    if len(final_images) != 8:
        errors.append(f"expected eight complete final images, found {len(final_images)}")

    contact_path = manifest_path.parent / "contact-sheet.jpg"
    if len(final_images) == 8:
        create_contact_sheet(final_images, contact_path)

    status = "PASS" if not errors else "FAIL"
    lines = [
        "# Ozon complete-image-set QA report",
        "",
        f"- Status: **{status}**",
        f"- Checked: {datetime.now().isoformat(timespec='seconds')}",
        f"- Manifest: `{manifest_path}`",
        f"- Complete final images found: {len(final_images)}/8",
        "- Expected canvas: 1200 × 1600 px, RGB/RGBA PNG, ≤10 MB",
        "- Image source: complete AI-generated compositions; no post-generation text or graphic overlay",
        "",
        "## Errors",
        "",
    ]
    lines.extend(f"- {item}" for item in errors) if errors else lines.append("- None")
    lines.extend(["", "## Warnings", ""])
    lines.extend(f"- {item}" for item in warnings) if warnings else lines.append("- None")
    manual = manifest.get("manual_qa", {})
    lines.extend(["", "## Required full-resolution review record", ""])
    lines.extend(f"- {key.replace('_', ' ').title()}: {manual.get(key) is True}" for key in MANUAL_GATES)
    lines.extend(
        [
            f"- Platform-check status: {manifest.get('platform_check', {}).get('status', 'missing')}",
            "",
            "Automated checks cannot prove text accuracy, layout integrity, measurement alignment, product identity, or CTR lift. Manual gates are mandatory.",
        ]
    )
    report_path = manifest_path.parent / "qa-report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"QA report: {report_path}")
    if len(final_images) == 8:
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
    prepare = subparsers.add_parser("prepare", help="validate a schema-v2 manifest and create a non-overwriting job directory")
    prepare.add_argument("--manifest", required=True, help="draft production-manifest JSON")
    prepare.add_argument("--workspace", default=".", help="project root that will receive output/ozon")
    prepare.set_defaults(handler=command_prepare)
    validate = subparsers.add_parser("validate", help="validate eight complete AI-generated final images")
    validate.add_argument("--manifest", required=True, help="production-manifest JSON with slide final_image paths")
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
