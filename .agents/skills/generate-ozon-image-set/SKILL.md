---
name: generate-ozon-image-set
description: Generate a coherent eight-image Russian-language Ozon product listing set from user-supplied product photos and verified product, selling-point, size, package, and optional brand or logo information. Use when Codex must create Ozon main images, white-background product images, lifestyle scenes, benefit infographics, dimension cards, detail cards, footwear cards, or a complete 8-image marketplace set for supported non-regulated physical goods while preserving product identity and preventing invented claims.
---

# Generate Ozon Image Set

Create exactly eight 3:4 Ozon listing images with one visual system, localized Russian copy, traceable facts, and strict product-identity control. Treat the user's photos and confirmed facts as the only source of truth.

## Required references

- Read [category-and-localization.md](references/category-and-localization.md) before planning any set.
- Read [reference-analysis.md](references/reference-analysis.md) when choosing visual hierarchy, layouts, badges, scene intensity, or information density. Do not copy a reference literally.

## Workflow

### 1. Inspect and gate inputs

Inspect every supplied image at high detail before drafting copy or generating images. Label each image as `primary reference`, `alternate view`, `detail reference`, `packaging reference`, or `logo`.

Require:

- supported category and product name;
- at least one sharp, unobstructed real product image;
- color/model/variant;
- exact material;
- exact quantity and package contents;
- exact dimensions needed for the dimensions card;
- verified selling points with a source for every claim.

Treat brand name, logo, preferred palette, and audience as optional. Pause and ask only for the smallest missing set when a required fact or necessary view is absent. Never fill gaps from visual guesswork, category norms, competitor listings, or generated content.

Reject unsupported regulated categories listed in the category reference. For footwear, apply its dedicated input gate.

### 2. Build the fact ledger and Russian copy

Create a draft `production-manifest.json` using the schema described below. Give every usable fact a stable `id`, `value`, non-empty `source`, and `confirmed: true`. Reference fact IDs from slide `claims`; never place an unreferenced factual assertion on a slide.

Write all added copy in localized Russian. Preserve real brand/model spelling and printed packaging text. Do not translate or redraw physical labels because that would change the product. Add brand/model tokens to `allowed_non_russian_terms` when they use Latin characters.

Resolve this skill's directory from the loaded `SKILL.md`. The commands below assume the current working directory is the project root. Run:

```powershell
python .agents/skills/generate-ozon-image-set/scripts/ozon_set.py prepare --manifest <draft-manifest.json> --workspace <current-project>
```

Use the printed job directory for all later work. `prepare` creates a non-overwriting `output/ozon/<sku>-<timestamp>/production-manifest.json` and an `image-prompts.md` file.

### 3. Lock the visual system and slide plan

Define one shared design system before generating bases:

- 3–5 color palette;
- regular and bold Cyrillic-capable fonts;
- title/body sizes and maximum line counts;
- badge, icon, corner-radius, shadow, and inset-detail treatment;
- one lighting direction, contrast level, material treatment, and scene mood.

Plan these six required slide types:

1. `hero`
2. `white-background`
3. `scene`
4. `benefits`
5. `dimensions`
6. `details`

Choose slides 7 and 8 adaptively from `package`, `usage`, `materials`, `scene`, `brand`, or `comparison`. Use `comparison` only when the user supplied both sides' images/data and sources. Keep `hero` factual and restrained; if current category rules disallow main-image text, set `text_allowed: false` and move its copy to another slide.

### 4. Generate text-free bases

Use the built-in `image_gen` tool by default. Make one distinct call per slide base; do not request eight different assets in one prompt. Inspect local source images first, then pass the same complete reference set to every identity-sensitive call.

For each prompt:

- set `Use case` to `product-mockup`, `photorealistic-natural`, or `ads-marketing` as appropriate;
- state that the output is a text-free 3:4 Ozon base;
- repeat product invariants from `product.identity_lock`;
- forbid any text, logo invention, watermark, badge, altered quantity, alternate color, new component, or new angle unsupported by the references;
- leave deliberate negative space for deterministic Russian copy;
- reuse the manifest palette, lighting, and material treatment.

Prefer exact source pixels, supplied transparent product images, and real detail crops. When a clean transparent product source is available, set `product.identity_strategy` to `source-pixel-composite`, place that same file in `product.source_images`, and add it to every slide through `product_layers`. Generate backgrounds without the product, then let the renderer composite the locked pixels. With one product view, preserve that angle across the set. Never invent a back, sole, internal structure, attachment, package item, or alternate model. For complex transparency, avoid a silent CLI/model fallback; use a complete text-free base or ask before any true-transparency fallback.

Copy selected generated bases into the job directory. Update each slide's `base_image` path and, if needed, `product_layers`, `detail_circles`, or `dimensions` annotations in the copied manifest. A product layer uses normalized center coordinates and width, for example `{"image":"product.png","x":0.5,"y":0.58,"width":0.72,"rotation":0,"shadow":true}`. Keep rotation within ±15°. Under `source-pixel-composite`, every layer image must be a transparent file listed in `product.source_images`.

### 5. Render deterministic Russian text

Render with:

```powershell
python .agents/skills/generate-ozon-image-set/scripts/ozon_set.py render --manifest <job-dir>/production-manifest.json
```

Use the script for all added titles, subtitles, bullets, badges, dimension arrows, real-image detail circles, and supplied logos. Never ask the image model to spell the final Russian text. The renderer writes `01-hero.png` through `08-*.png`, or versioned siblings on rerun, and records each path as `rendered_file`.

### 6. Validate and visually review

Open all eight full-resolution images and the contact sheet. Compare every slide against the source images for silhouette, proportions, color, material, seams, controls, accessories, branding, product count, package count, and visible text.

Set all `manual_qa` values to `true` only after completing those checks:

- `product_identity`
- `style_consistency`
- `russian_proofread`
- `platform_rules`

For `platform_rules`, first try to read the current official URL. Record `platform_check.status: verified` only when the official rule text was actually available. If the page remains unavailable after one retry, use `status: conservative-fallback`, record the concrete `retrieval_error`, force the hero to `text_allowed: false`, and state in `category_decision` that upload-time recheck is still mandatory. Set the manual gate to true only after reviewing that handling; never describe fallback status as official verification.

Then run:

```powershell
python .agents/skills/generate-ozon-image-set/scripts/ozon_set.py validate --manifest <job-dir>/production-manifest.json
```

Do not deliver while the report contains an error or an unchecked manual gate. A `conservative-fallback` warning may remain only when the official Ozon page was genuinely unreachable, the hero is text-free, and the handoff explicitly says the set still needs an upload-time rule recheck. If product drift occurs, regenerate that base with one targeted correction; if it persists, fall back to an exact supplied cutout/view and a simpler scene.

## Manifest contract

Use UTF-8 JSON with these top-level keys:

```json
{
  "schema_version": 1,
  "sku": "stable-sku-or-slug",
  "category": "home",
  "allowed_non_russian_terms": ["Brand", "Model-X"],
  "product": {
    "name_source": "source-language name",
    "name_ru": "Русское название",
    "color": "Белый",
    "model": "",
    "material": "Керамика",
    "quantity": "6 шт.",
    "package_contents": ["6 салатников"],
    "dimensions": [{"label": "Диаметр", "value": "14 см"}],
    "source_images": ["absolute-or-draft-relative-path"],
    "brand": {"name": "", "logo": null},
    "identity_lock": ["white ribbed ceramic bowls", "six-piece set"]
  },
  "facts": [
    {"id": "quantity", "value": "6 шт.", "source": "user brief", "confirmed": true}
  ],
  "design": {
    "palette": {"primary": "#33214B", "secondary": "#F4E9DC", "accent": "#E8A33A", "text": "#FFFFFF"},
    "fonts": {"regular": null, "bold": null}
  },
  "manual_qa": {
    "product_identity": false,
    "style_consistency": false,
    "russian_proofread": false,
    "platform_rules": false
  },
  "slides": []
}
```

Each slide must contain `index`, `type`, `filename`, `layout`, `title`, `subtitle`, `bullets`, `claims`, `generation_prompt`, and `base_image`. `base_image` may be empty during `prepare` but must point to a real text-free base before `render`. Optional keys are `logo`, `text_allowed`, `requires_new_angle`, `product_layers`, `dimensions`, `detail_circles`, `text_blocks`, and `comparison_sources`. Use `product.identity_strategy: source-pixel-composite` whenever every page can reuse an unchanged transparent source; otherwise use `reference-guided` and document the manual identity review.

Use normalized 0–1 coordinates for dimension points, detail-circle centers, and custom text blocks. Consult `python .agents/skills/generate-ozon-image-set/scripts/ozon_set.py --help` for command details.

## Delivery

Deliver exactly eight rendered PNG files plus:

- `production-manifest.json`
- `image-prompts.md`
- `qa-report.md`
- `contact-sheet.jpg`

Report the job directory, the built-in image-generation path used, and any intentionally omitted or simplified visual because the source evidence was insufficient. Never claim CTR or conversion improvement without actual experiment data.
