---
name: generate-ozon-image-set
description: Generate a product-specific eight-image Russian Ozon listing set as complete AI-generated final compositions from supplied product photos and verified facts. Use for supported non-regulated physical goods, including footwear and household goods, when Codex must plan the set from buyer decisions instead of a fixed slide template, create information-rich high-impact marketplace visuals, preserve exact product identity, and avoid post-generation text or graphic overlays.
---

# Generate Ozon Image Set

Create eight finished 3:4 Ozon images with accurate Russian copy, traceable facts, strong mobile readability, and strict product-identity control. Generate every page as one complete AI artwork. Never build a background and add text, cards, details, arrows, logos, or product cutouts afterward.

## Required references

- Read [category-and-localization.md](references/category-and-localization.md) before planning.
- Read [reference-analysis.md](references/reference-analysis.md) before choosing page roles, information density, hierarchy, colors, typography, details, dimensions, or scenes.

## Workflow

### 1. Inspect and gate inputs

Inspect every supplied image at high detail. Label it `primary reference`, `alternate view`, `detail reference`, `packaging reference`, `on-body reference`, or `logo`.

Require:

- supported category and exact product name;
- at least one sharp, unobstructed real product image;
- color/model/variant, material, quantity, package contents, and dimensions;
- sourced selling points and specifications;
- additional views for any interior, underside, worn, open, or detail evidence the set will show.

Treat brand, logo, palette, and audience as optional. Never fill factual gaps from appearance, category norms, competitors, or generated content. Apply the footwear adapter when relevant.

### 2. Build the fact ledger

Create a schema-version-2 manifest. Give every fact a stable `id`, `value`, source, and `confirmed: true`. Mark the facts that actually affect purchase in `set_strategy.priority_fact_ids`. Every priority fact must appear in at least one slide claim.

Write natural Russian shopper copy. Preserve supplied brand/model spelling and printed packaging text. Add permitted Latin brand/model tokens to `allowed_non_russian_terms`. Do not turn a visible feature into an unsupported performance claim.

Before `prepare`, freeze an exact Russian copy deck for all eight pages. Review every title, subtitle, bullet, label, number, and unit for:

- natural `ru-RU` wording rather than literal Chinese or English translation;
- grammar, case, number, gender, adjective/noun agreement, punctuation, decimal commas, and unit spacing;
- concise marketplace language that answers the buyer question without keyword stuffing;
- exact agreement with the confirmed fact ledger and package contents;
- absence of unsupported performance, season, origin, certification, ranking, promotion, or superlative claims.

Record the completed preflight in `localization_review`. Do not call image generation until `pre_generation_approved` and all five `pre_generation_checks` are `true`. Freeze the approved text verbatim; prompts may not improvise synonyms, extra benefits, or alternate numbers after approval.

Run `prepare`:

```powershell
<python-executable> .agents/skills/generate-ozon-image-set/scripts/ozon_set.py prepare --manifest <draft-manifest.json> --workspace <current-project>
```

Use the printed job directory for the production manifest and all images.

### 3. Plan from buyer decisions, not fixed page types

Write `set_strategy` before writing slides:

- `audience`: intended shopper;
- `buyer_questions`: the eight most useful questions this product can truthfully answer;
- `priority_fact_ids`: decision-relevant fact IDs that the set must cover;
- `palette`: 3–5 colors including the exact product color, a neutral, and one or two contrasting accents;
- `typography`: one legible Cyrillic type direction;
- `visual_thesis`: the set-wide visual and selling idea.

Make slide 1 a `hero`. Select slides 2–8 solely from product evidence and buyer questions. Allowed types include `decision-overview`, `white-background`, `size-fit`, `dimensions`, `construction`, `feature-proof`, `benefits`, `details`, `materials`, `angles`, `usage`, `scene`, `care`, `package`, `configuration`, `compatibility`, `brand`, and `comparison`.

Do not require a white-background, scene, benefits, dimensions, details, or materials page. Use one only when it resolves an important question better than another page.

For each slide, record:

- `purpose`: one unique sentence describing the page's job;
- `buyer_question`: one unique shopper question it answers;
- `selection_reason`: why this content deserves a full page;
- `information_units`: the meaningful items visible on the page, such as product name, quantity, number, specification, benefit, usage result, package item, or detail label.

Reject semantic duplicates. A materials page and a details page are duplicates when both merely show the same three surface close-ups. Merge them and use the freed page for another buyer question. Repetition is allowed only when the hero summarizes a fact that a later page proves in greater depth.

### 4. Design for mobile click and scan behavior

Use the high-click references as attention hypotheses, not proof of conversion.

For the hero:

- give the product or truthful bundle about 55–75% of meaningful visual area;
- use a large category/product headline when current rules permit it;
- use one large numeric anchor when quantity, capacity, size, or another sourced number matters;
- add one or two short supporting facts;
- use 3–6 information units total when text is allowed;
- keep uninformative empty background below roughly 20% of the canvas.

For information pages:

- keep the product or demonstrated use at about 45–70% of meaningful visual area;
- use 4–7 useful information units, without repeating another page;
- make the title readable in a search thumbnail and body copy readable on a phone;
- target title letter height around 7–12% of canvas height and body letter height around 2.5–4%;
- prefer one strong number, a short headline, and 2–4 supporting facts over many tiny badges;
- use compact high-contrast labels or badges only when they remain outside important product structure.

Use richer but controlled color. Preserve the exact product color, then add category-relevant scene colors and a clear accent. Avoid an eight-page wash of the same cream background. Keep typography, product treatment, and accent logic consistent while varying composition and scene intensity.

### 5. Generate complete AI artworks

Use the built-in `image_gen` tool by default. Make one distinct call per page and pass the same complete identity-reference set to every identity-sensitive call.

Every prompt must include:

- `Asset type: complete final 3:4 Ozon listing image`;
- the page purpose, buyer question, and required information units;
- exact Russian title, subtitle, bullets, labels, and numbers verbatim;
- product invariants from `product.identity_lock`;
- target product-area, hierarchy, text-size, color, and empty-space guidance;
- explicit non-overlap zones;
- no watermark, invented logo, unsupported claim, altered quantity, alternate color, new component, or unsupported angle.

Treat the output as final artwork. A format-only resize is allowed; adding or replacing visible content after generation is not.

### 6. Apply page-specific truth rules

For every page:

- keep shopper text outside critical product features and maintain immediate legibility;
- allow small high-contrast text modules, but never place a large opaque or translucent panel over the product;
- do not shrink the product just to create decorative whitespace;
- do not use flags, medals, ratings, certifications, official-store claims, prices, discounts, or promotional urgency without explicit evidence and current permission.

For detail, material, and construction content:

- show only supplied visible evidence;
- keep enlargements outside the main product silhouette;
- combine related evidence on one page when it answers the same question;
- never create multiple pages that reuse the same close-ups with different headings.

For dimensions and footwear sizing:

- use a supported view;
- make arrow endpoints touch the true visible extrema;
- keep arrows parallel to the measured axis and labels outside the product;
- use a size table instead of meaningless arrows when the buyer needs a mapping rather than a physical product dimension.

For scenes and usage:

- include them only when the context explains fit, scale, handling, outcome, placement, or use;
- do not use decorative lifestyle imagery that answers no buyer question;
- do not imply an accessory, food, performance result, or use claim that is absent from supplied evidence.

### 7. Inspect and iterate

Open every image at full resolution and as a contact sheet. Check:

- exact product identity, count, color, proportions, construction, accessories, and packaging;
- exact Russian spelling, units, punctuation, and line breaks;
- title and body legibility at contact-sheet size;
- sufficient product scale and no excessive dead space;
- useful information density and a clear hierarchy;
- controlled color variety across the set;
- unique page purpose and buyer question;
- no repeated detail/material page;
- correct detail placement and measurement alignment.

Transcribe every visible string from every final page and compare it line by line with the frozen copy deck. Record all eight comparisons in `localization_review.slide_checks`, including `expected_text`, `observed_text`, and `status`. Check meaning as well as spelling: the sentence must be natural Russian, factually correct, appropriate for ecommerce, and unambiguous in context.

Treat any misspelling, malformed Cyrillic, missing or duplicated word, wrong number or unit, unnatural phrase, untranslated fragment, added claim, or visible text absent from the approved deck as a page-generation failure. Regenerate or AI-edit the complete page and repeat the transcription. Never repair text with a post-generation overlay. Set `post_generation_approved: true` only when all eight transcription records pass exactly.

Regenerate or AI-edit a failing complete page. Never repair it with PIL, canvas, SVG, or another text/graphic overlay renderer.

### 8. Validate

Set manual gates to `true` only after review:

- `product_identity`
- `style_consistency`
- `russian_text_accuracy`
- `layout_integrity`
- `measurement_alignment`
- `platform_rules`
- `mobile_legibility`
- `information_density`
- `page_uniqueness`
- `color_variety`

Then run:

```powershell
<python-executable> .agents/skills/generate-ozon-image-set/scripts/ozon_set.py validate --manifest <job-dir>/production-manifest.json
```

Do not deliver with an error or unchecked gate. Record unavailable platform rules honestly and require an upload-time recheck; do not claim verification or CTR improvement without evidence.

## Manifest contract

Use UTF-8 JSON with `schema_version: 2`. Include `set_strategy`. Each slide must contain `index`, `type`, `filename`, `purpose`, `buyer_question`, `selection_reason`, `information_units`, `layout`, `title`, `subtitle`, `bullets`, `claims`, `generation_prompt`, and `final_image`.

Include this mandatory localization record:

```json
{
  "localization_review": {
    "locale": "ru-RU",
    "pre_generation_approved": true,
    "pre_generation_checks": {
      "natural_russian": true,
      "grammar_and_agreement": true,
      "ecommerce_fit": true,
      "fact_alignment": true,
      "claim_safety": true
    },
    "post_generation_approved": false,
    "slide_checks": []
  }
}
```

After generation, change `post_generation_approved` to `true` only after adding eight `slide_checks`. Each check must contain `index`, `status: "pass"`, and exact `expected_text` and `observed_text` lists. The observed list must transcribe every visible string, including AI-added text; the two lists must match after whitespace normalization.

Do not use legacy overlay fields: `base_image`, `product_layers`, `detail_circles`, `dimensions`, `text_blocks`, slide-level `logo`, or `rendered_file`.

Use `text_allowed: false` only when current rules require a text-free hero. Use `requires_new_angle: true` only when sources support the view. Use `comparison_sources` for sourced comparisons.

## Delivery

Deliver eight complete final PNG files plus `production-manifest.json`, `image-prompts.md`, `qa-report.md`, and `contact-sheet.jpg`. Report the job directory, generation path, upload-time rule warning, and any omitted page caused by insufficient evidence.
