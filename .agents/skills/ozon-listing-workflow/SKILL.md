---
name: ozon-listing-workflow
description: Create a complete Russian-language Ozon product listing from supplied evidence, including a carefully engineered product title, factual description, search tags/queries, selectable ten-image set, and QA artifacts. Use when Codex must prepare or refresh an Ozon card, turn a product folder into listing content, let a user choose image types, or reason about title elements such as product type, brand, model, audience, material, use, size, color, quantity, compatibility, selling points, and season without inventing facts or keyword demand.
---

# Ozon Listing Workflow

Act as a senior Ozon ecommerce operator, native-level Russian ecommerce editor, and ecommerce art director. Write consumer-facing text for the reading habits of Russian Ozon shoppers, not as a literal translation of Chinese source material or as seller-backend terminology. Understand how Russian shoppers scan listings and how copy, composition, hierarchy, and product proof support a purchase decision. Keep seller-facing manifests and QA notes operational and separate from shopper copy. Never let this expert role override evidence, current platform rules, or claim safety, and never promise ranking, CTR, or conversion gains.

Produce an evidence-backed Russian listing package: title, description, tags, ten final 3:4 images, manifest, prompts, and QA. Treat current Ozon rules and the selected category template as runtime dependencies.

## Required references

- Read [listing-copy.md](references/listing-copy.md) before researching queries or drafting text.
- Read [category-and-localization.md](references/category-and-localization.md) before selecting claims or category rules.
- Read [reference-analysis.md](references/reference-analysis.md) before designing the image set.
- Read [image-selection.md](references/image-selection.md) before asking for optional product information or selecting image types.
- Read [agent-qa.md](references/agent-qa.md) before approving copy or final images.

## 1. Inspect and gate evidence

Inspect every supplied image and document. Prompt the user with a concise list of information they may provide, explain that useful confirmed information may appear in the images, title, or description, and continue with the evidence available. Do not turn the prompt into a mandatory form. Evaluate exact product type/category, SKU/model, variant/color, material, quantity, package contents, dimensions or size data, selling points, audience, use context, and real product images for usefulness rather than displaying everything supplied. Follow [image-selection.md](references/image-selection.md).

Record any user instruction that forbids a field or exact value from consumer content in `excluded_visible_fields`, with field/value, scope, source, and reason. User exclusion overrides a populated product table, packaging, fact ledger, and all other evidence. Never write an excluded brand, model, SKU, internal number, or other field/value back into the title, description, tags, or images merely because it exists in source data. Apply exclusions to every requested consumer-content scope and keep the excluded value internal.

Inventory any user-provided reusable size chart, after-sales card, packaging card, care card, or other generic listing asset before selecting pages. Record it in `user_provided_reusable_assets`; unless the user explicitly requests a rebuild, add its covered type to `excluded_from_generation` and do not count it among the ten newly generated product-specific pages. Fill the freed slot with another truthful product-specific buyer question. A reusable asset may be delivered alongside the set without consuming a generation slot.

Request additional evidence only when a selected page or truthful product depiction cannot be produced without it. Require the relevant source view before showing an underside, interior, worn state, package item, measurement, or construction detail. Omit unsupported information rather than silently completing it.

Build a fact ledger with stable IDs, exact values, sources, and `confirmed: true`. Classify sources as user document, user statement, product photo, packaging, official manufacturer source, current Ozon rule, Ozon query analytics, or market hypothesis.

Never infer material, season, audience, performance, compatibility, origin, certification, included accessories, or dimensions from appearance or category convention. Omit unsupported language or request the missing fact.

## 2. Verify current Ozon requirements

Browse the current official Ozon Seller help, relevant category requirements/template, and image requirements immediately before drafting. Record official URLs, access date, category decision, current field limits, and retrieval failures in `platform_check`.

Use the live category template and Seller cabinet fields as the source of truth. If official pages cannot be retrieved, record `conservative-fallback`, avoid claiming upload readiness, and require an upload-time recheck. Never present remembered limits as current rules.

## 3. Build search intent honestly

Use keyword evidence in this order:

1. Ozon query analytics/export and user-supplied keyword/query data;
2. documented current Ozon searches and real exact-category result observations;
3. official category attributes and natural vocabulary Russian shoppers use for the category;
4. semantic candidates derived from confirmed product facts.

Separate `observed` queries from `hypothesis` terms. Never call a term popular, high-frequency, seasonal, trending, or conversion-driving without data. Exclude competitor brands, irrelevant traffic terms, unsupported benefits, mistranslations, and redundant word-order variants.

Create a product-specific candidate keyword ledger before drafting titles. Classify every candidate as `core-precise`, `category-broad`, one of two or three complementary `intent-group` values, `long-tail`, `audience`, `season`, `material`, `structure-attribute`, `differentiating-benefit`, `style-trend`, `quantity`, or `brand`. Record exact Russian wording, normalized intent, source/date, `observed-data|semantic-hypothesis`, linked fact IDs, time sensitivity, priority rationale, destination, and inclusion/rejection decision. Brand is eligible only when supplied and not excluded; quantity is eligible only when decision-relevant. Prefer complete Ozon characteristics over repeated synonyms in prose.

## 4. Engineer the title

Optimize the title jointly for accurate identification, relevant search coverage, filter/category matching, Russian readability, and purchase judgment. Do not treat either an extremely short conservative fact title or a maximal keyword chain as the goal. Follow the live category formula and field limit. Otherwise build a natural Russian title from `[brand only when evidenced and allowed] + precise core product term + broader/different discovery path + one or two complementary long-tail intents + two to four high-value supported attributes/selling points + restrained evidence-consistent style/trend term when justified + decision-relevant quantity`. Keep the product type and strongest precise intent early. Use commas, a short dash, or a semicolon only when they improve separation; never import a remembered Amazon 200-character formula.

Treat brand as nullable and conditional. Include it only when user data, a product table, or trustworthy product evidence explicitly establishes the brand and `excluded_visible_fields` does not prohibit it. Do not invent a brand, use a placeholder, infer one from a folder/image filename, convert a store or seller name into a brand, or guess from ambiguous visual marks. When absent, conflicting, uncertain, or excluded, use `brand: null` internally and record the omission reason; never expose that reason to shoppers.

Treat model as default-omit. Include a model only when evidence establishes it as a public consumer-facing model that shoppers genuinely search for, and it is not excluded. Apply an unconditional title SKU ban: no selected title or alternative may contain an SKU, stock-keeping code, seller/internal article number, backend identifier, its known bare value, or labels such as `SKU`/`артикул`. Source availability, public visibility, keyword coverage, and user authorization do not create an exception. Keep SKU only in internal evidence/operations fields. Apply the same prohibition to the description. A user exclusion always wins even when a table contains brand or model values.

Choose terms per product, never by copying a category template. When evidence and category language allow, cover one precise core term, one broader term or genuinely different discovery path, one or two complementary long-tail intents, and two to four high-value attributes/selling points. Organize these into two or three distinct search-intent groups such as product type, audience/season/use, or structure/compatibility/configuration. Do not count reordered words, inflections, or synonymous duplicates as separate groups. Without query/search data, label every proposed discovery term `semantic-hypothesis` and the plan `semantic-coverage`; never claim high volume, popularity, trend, hot-keyword status, or conversion value.

Use functional, feature, attribute, and restrained style terms only when evidenced. Treat user suggestions such as “2026 new,” “light luxury,” “comfortable,” “warm,” “hidden height increase,” and “versatile” as candidates, never mandatory tokens. Apply the product-specific gates in [listing-copy.md](references/listing-copy.md): verify current-year launch and search/positioning value; replace literal `лёгкая роскошь` with concrete natural design facts; support comfort with last/lining/insole/sole facts or user-authorized material; distinguish winter/insulated/fur-lined facts from tested temperature or heat-retention claims; use `со скрытым подъёмом` or `со скрытой танкеткой` only for a real internal hidden lift and never for an exposed platform, total height increase, or heel height; and prefer restrained everyday-use wording over universal match-all claims. `Премиальный`, `элегантный`, and equivalents still require direct support. A photo may support a visible texture/style description but not an unsourced material claim.

Add a quantity phrase only when pack count, set count, or included accessory count changes the purchase decision. Do not spend title characters on default single-item or one-pair wording. Draft at least one selected title and two alternatives from the ledger. For each candidate, record phrase-role breakdown, coverage source, linked evidence, character count, repetition, Russian naturalness, search/discovery value, precision, purchase-decision value, and rejected terms with reasons. Show only the selected title in consumer delivery unless the user requests comparison; keep alternatives and analysis internal.

Treat season and selling-point words as claims. Add `зимние`, `демисезонные`, `летние`, or similar terms only when source evidence, construction/material facts, and the category attribute support them. Prefer precise facts such as `съёмная стелька` over vague praise such as `удобные`.

Avoid keyword chains, repeated synonyms, promotional wording, subjective superlatives, competitor brands, all-caps, prices, discounts, seller names, and unsupported audience expansion. Do not misuse anti-stuffing rules to produce an under-covered title: when confirmed evidence supports two or three complementary intents and several high-value attributes, a title containing only the product name plus one or two modifiers fails and must be expanded naturally. Record every chosen title element with role, linked facts, source, and inclusion reason. Ensure title, category, characteristics, images, and package count describe the same variant.

## 5. Write the description and tags

Write connected Russian prose for a shopper. Apply the Russian marketplace reading-habit rules in [listing-copy.md](references/listing-copy.md): front-load identity and decisive facts, keep one clear message per text block, use natural Russian collocations and scan-friendly sentences, and remove literal Chinese syntax or inflated promotional phrasing. Never include an SKU, internal article number, backend identifier, known bare SKU value, or any field/value blocked by `excluded_visible_fields`. Include a public model only when the same evidence, consumer-search, and exclusion gates used for the title pass. Then cover relevant use, construction/material, fit or dimensions, package contents, care/compatibility, and limitations. Do not turn a characteristic into an unsupported result or repeat the title as a keyword block.

Generate a compact prioritized tag/query set. Every term needs intent, source, `observed` or `hypothesis`, linked facts, and destination. If the current category has no tag field, keep the set as a research artifact and map appropriate terms to characteristics or natural prose; never invent an upload field.

Complete the Russian editorial and factual gates in `listing.copy_review`.

## 6. Plan and generate the image set

Offer the image-type choices in [image-selection.md](references/image-selection.md) as plain text. A user may select zero to eight types. Treat every user-selected type as mandatory and highest priority, subject only to evidence, platform safety, and reusable-asset exclusion. If a selected type is already covered by a confirmed reusable asset, exclude it from new generation unless the user explicitly requests a rebuild, preserve the user's intent through the reusable asset, and replace its generation slot with a product-specific page. Always deliver ten newly generated product-specific pages: preserve the remaining selected types and automatically choose the rest, leaving at least two pages for evidence-led automatic selection. When no selected type is excluded, three selections require seven automatic pages and eight selections require two; otherwise compute `automatic_count = 10 - selected_types_still_requiring_generation`. Never ask the user to fill all ten slots.

Write `set_strategy`: audience, ten distinct buyer questions, selected and automatic image types, reusable-asset exclusions, selection reasons, priority fact IDs, an information-coverage matrix, claim-ladder coverage, information-structure distribution, `microcopy_default`, colorway strategy, palette, typography, lighting, contrast, framing, spacing, safe zones, product scale, reusable component grammar, layout-archetype distribution, visual rhythm, and visual thesis. Keep product identity, palette, typography, graphic language, Russian tone, and information hierarchy unified across all ten pages while varying crop, scene intensity, composition, information structure, and decision job. Default fashion, footwear, beauty, food, and similar visual categories to `phrase-first` microcopy.

For a multi-color product, select exactly one `primary_colorway` and at most one `secondary_colorway`, each linked to confirmed variant evidence. Build identity-sensitive pages around the primary colorway; do not rotate colors page by page or assign one color per page. Show the secondary colorway only on recorded pages where it resolves a real choice. Create a series/colors page only when confirmed color choice is itself an important buyer question. A color visible in a photo does not establish its catalog color name.

Define a set-level component grammar before generation. Build hierarchy first with non-text visual components such as whitespace, columns, rules, card shapes, color fields, annotation paths, product scale, cropping, grouping, and rhythm. Treat eyebrow/model line, headline, benefit subheadline, bullet, card label, neutral fact badge, chip, callout, footer, and progress mark as optional text components, never as required decoration. Select only components with shopper value. Assign every slide a `layout_archetype`, `component_stack`, and `visual_rhythm_role`; use at least four materially different layout archetypes across the ten pages and do not reduce the system to a large headline plus one product on page after page.

Make slide 1 a current-rule-compliant hero that may summarize several priority facts. Make slides 2–10 introduce different primary information from one another; a changed crop, scene, title, or layout does not make repeated information unique. Choose slides 2–10 only from evidence and buyer questions; do not force a universal page template.

Give each slide a unique purpose, question, primary decision message, image type, selection source (`user|automatic`), and selection reason. Assign `primary_fact_ids` and `supporting_fact_ids`. Outside the hero, do not reuse the same fact as the primary message of another page. A hero fact may appear once later only when the later page adds deeper proof, measurement, configuration, limitation, or context; do not repeat the same wording or visual claim. Merge pages that still communicate the same information. If ten truthful questions are unavailable, request the evidence needed for an impossible user-selected type or use another supported exact-product view for an automatic slot; never invent decorative claims.

Complete a claim ladder before writing prompts for every non-hero page:

1. Level 1 `selling_point`: one clear, scannable hook or decision answer;
2. Level 2 `consumer_benefit`: an optional short shopper descriptor or restrained experience phrase, not a mandatory explanatory sentence;
3. Level 3 `support_facts`: two to four distinct evidence-linked facts, parameters, components, use contexts, annotations, or comparisons that prove the selling point; when rendered as cards or callouts, keep them phrase-like;
4. Level 4 `offer`: optional promotional information only when the user explicitly supplied it, it remains current, evidence records its terms/expiry, and current Ozon/category rules permit it on that page.

Default each non-hero page to at least two truthful information levels; important selling-point pages should use three when evidence supports them. A valid gradient may be a headline plus two or three short fact/selling-point cards; visual hierarchy does not require a long subtitle or complete sentences. Do not force extra layers, two-to-four bullets, or an offer. If the headline already communicates the complete supported answer and no separate benefit/proof exists, set `consumer_benefit` to `null`, keep the page lean, and record `information_layer_exception` plus `omitted_claims_and_reasons` instead of paraphrasing or inventing copy.

Assign every page a `microcopy_mode`. For `phrase-first`, use natural Russian noun, adjective, attribute, or short experience phrases: target two to six words for Level 2 and one to four words for Level 3 cards/callouts. Use `sentence-when-needed` only when a complete sentence adds necessary decision information that cannot be preserved in a shorter phrase; use `instructional` only for necessary use, choice, measurement, or safety instructions. Before freezing copy, apply the abstract-explanation deletion test in [listing-copy.md](references/listing-copy.md): delete or compress language that sounds like copy analysis, design commentary, translationese, unsupported causal explanation, or abstract styling rhetoric. `consumer_benefit` may be `null`; never lengthen a headline paraphrase merely to populate Level 2.

Map `feature -> benefit -> experience` with explicit claim strength, but do not turn the mapping into a visible causal sentence. Use `fact` for directly verifiable construction or attributes, `supported-benefit` for a restrained shopper benefit tightly linked to evidence, and `marketing-claim` only for user-authorized marketing material or adequate testing/performance evidence. Facts such as artificial short-pile lining, thick rubber sole, round toe, mid-calf shaft, gentle ruching, or side buckle may be stated when supported. Neutral short phrases such as `Мягкий короткий ворс`, `Объёмный силуэт`, or `Мягкое ощущение` require close evidence and restrained wording; experience wording such as `Комфортное ощущение` additionally requires material/structure support or explicit user authorization. Do not claim cloud-like cushioning, cotton-soft footfeel, maximum comfort, all-day fatigue relief, heat retention, rebound cushioning, slip resistance, health effects, or similar strong outcomes without the required test, construction/material evidence, or explicit authorized marketing source. A user example is not product evidence.

For every detail page, choose one primary evidence mode: `full-bleed-macro`, `single-detail-hero`, `precise-annotation-path`, `structure-card`, or `full-product-locator`. Do not default to a whole product plus circular or rectangular inset. Allow a locator plus inset only when the inset proves a different layer or fact that is invisible or hard to distinguish in the locator, and record `combined_detail_rationale` plus separate fact IDs. If both views prove the same evidence, remove one.

Keep four planning fields separate for every page: internal `purpose`, `buyer_question`, supported `decision_message`, and shopper-facing `title`. Never copy or translate an internal label into the title. Reject production labels such as `ВИД СБОКУ`, `ДЕТАЛИ`, `МАТЕРИАЛЫ`, `КРУПНЫЙ ПЛАН`, or `ХАРАКТЕРИСТИКИ`. Also reject a bare attribute as the whole title, such as `КРУГЛЫЙ НОСОК`, `ОВЕЧЬЯ КОЖА`, or `ШЕРСТЬ`, unless it is part of a complete, decision-useful statement. Prefer a supported relationship, configuration, comparison, quantified choice, material construction, use constraint, or package fact. If no benefit is sourced, state the factual construction completely; never invent comfort, warmth, durability, safety, or performance to make a headline sound stronger.

Record `decision_message`, `headline_kind`, and `shopper_headline_rationale` for every slide. Run the headline gate in [listing-copy.md](references/listing-copy.md) before freezing Russian image copy. A text-free hero may leave the title empty, but must still record why text is omitted.

Before freezing copy, run the visible-string role gate in [listing-copy.md](references/listing-copy.md). Enumerate every consumer-visible string planned for the image—headline, eyebrow, benefit subheadline, bullet, card label, badge, chip, callout, footer, progress mark, annotation, and model line. Assign exactly one allowed role: `shopper-identity`, `decision-answer`, `sourced-fact`, or `necessary-instruction`; record fact IDs, shopper value, and whether the string is required. Reject internal evidence/status, production/navigation filler, seller-backend terms, and any auxiliary string that can be removed without reducing purchase understanding.

Never expose `confirmed`, `verified`, `evidence`, `source`, `fact`, `QA`, `manifest`, `selection`, `automatic`, `SKU`, or equivalent Russian, Chinese, or other-language status/backend wording. Reject internal-status strings and any `SKU <KNOWN_SKU_VALUE>` construction. Here `<KNOWN_SKU_VALUE>` is an internal documentation placeholder only and must never be rendered literally in consumer copy. A public consumer-searchable model may appear on at most one identity page only when evidence supports it and `excluded_visible_fields` allows it; never repeat any model as footer decoration. If user exclusions include a model, identifier, or exact value for a consumer-content scope, omit it throughout that scope.

Default generic eyebrow labels to absent. Do not show `МАТЕРИАЛЫ`, `ДЕТАЛЬ`, `ФАКТУРА`, `КОНСТРУКЦИЯ`, `СЕЗОН`, `ВНЕШНИЙ ВИД`, `СИЛУЭТ`, or equivalents when they merely name a page type. Allow one only when Russian shoppers genuinely need that navigation, it works with a complete decision-useful statement, and `auxiliary_copy_rationale` explains why removing it would reduce understanding.

Freeze exact Russian image copy and approve localization before generation. Author the manifest and prompt deck directly from the evidence ledger. Do not use a validator, linter, OCR script, image-comparison script, or other automated pass/fail mechanism for copy or image QA. The Agent must make and document every approval decision itself using [agent-qa.md](references/agent-qa.md).

Bind every number to the exact physical quantity named by the evidence before designing a measurement visual. Treat overall height increase, shaft height, heel height, sole thickness, platform height, foot length, and package dimensions as different facts even when they share a unit. Measurement arrows may touch only the sourced start and end points of that exact quantity. If the measured construction or endpoints are not visible in the supplied evidence, show the confirmed numeric choice as text without arrows, changed proportions, or a silhouette that implies another measurement.

Use `image_gen` by default, one complete final consumer-facing artwork per call, with the same user-supplied product references for identity-sensitive pages. Real product references are evidence, not permission to redesign the product. Do not generate a background and later add product cutouts, text, cards, arrows, logos, or other overlays with scripts, canvas tools, or conventional image editing. Regenerate or AI-edit the complete page for identity or text failures. A mechanically arranged contact sheet is an internal QA artifact, not a consumer-facing listing image, and must not alter any source page.

## 7. Inspect, validate, and deliver

Inspect every image full-size and as a ten-page contact sheet. Transcribe every visible string and compare it with frozen copy. Review product identity, Russian accuracy, claim-ladder alignment, benefit/proof relevance, claim strength, mobile legibility, information density, page uniqueness, measurement alignment and semantic target, platform rules, style consistency, listing-copy consistency, shopper-headline quality, layout-archetype distribution, information-structure distribution, component hierarchy, colorway concentration, repeated inset count, and visual rhythm. Apply the explicit fail conditions in [agent-qa.md](references/agent-qa.md). Fail any page whose title merely names the camera angle, page section, or isolated attribute instead of communicating the recorded decision message. Also fail a page when a correct number is attached to the wrong physical feature, such as depicting height increase as shaft height.

The Agent must write a slide-by-slide QA record with the observed visible strings, product-identity evidence, headline decision value, claim links, layout findings, and pass/fail reason. A boolean without review notes is not evidence. Rework every failed page and inspect it again. Do not deliver with unresolved failures.

Deliver `listing-content.json`, `listing-content.md`, ten newly generated product-specific PNGs, `production-manifest.json`, `image-prompts.md`, `qa-report.md`, and `contact-sheet.jpg`; list reusable assets separately without regenerating or counting them among the ten. These files are authored from the reviewed evidence; no script-generated PASS is allowed. Report rule status, evidence gaps, hypothesis-only tags, user-selected types, automatic selections, reusable-asset exclusions, and omitted unsupported content. Never promise ranking, CTR, or conversion improvement.

## Manifest additions

Use UTF-8 JSON with `schema_version: 12`. Retain the product, facts, localization, strategy, slides, platform-check, and agent-QA structures. Add:

```json
{
  "excluded_visible_fields": [{
    "field": "brand|model|sku|internal-number|other",
    "value": "optional exact value to exclude; internal only",
    "scope": ["title", "description", "images", "tags"],
    "source": "explicit user instruction",
    "reason": "why this field must remain internal"
  }],
  "listing": {
    "title_keyword_ledger": [{
      "term": "exact Russian candidate",
      "layer": "core-precise|category-broad|intent-group|long-tail|audience|season|material|structure-attribute|differentiating-benefit|style-trend|quantity|brand",
      "normalized_intent": "distinct discovery or decision job",
      "source": "query analytics, user data, dated Ozon observation, official category vocabulary, or confirmed fact",
      "coverage_basis": "observed-data|semantic-hypothesis",
      "fact_ids": ["fact-id"],
      "time_sensitive": false,
      "decision": "include-title|include-description|include-attribute|include-tags|reject",
      "reason": "priority or rejection reason"
    }],
    "brand": {
      "value": null,
      "fact_ids": [],
      "status": "included|omitted-not-provided|omitted-conflict|omitted-unconfirmed|omitted-user-excluded",
      "reason": "internal reason such as 品牌未提供—已省略; never consumer-visible"
    },
    "title": "Approved Russian title",
    "alternative_titles": ["Alternative 1", "Alternative 2"],
    "title_candidates": [{
      "text": "selected or alternative Russian title",
      "status": "selected|alternative",
      "character_count": 0,
      "intent_groups": ["distinct intent group"],
      "high_value_terms": ["supported attribute or selling point"],
      "coverage_sources": ["observed-data|semantic-hypothesis"],
      "fact_ids": ["fact-id"],
      "repetition_review": "none or explained",
      "russian_naturalness": "pass with rationale",
      "search_discovery_value": "internal evidence-based assessment without demand claims",
      "precision_review": "why traffic remains product-relevant",
      "purchase_decision_value": "what useful choice information is present"
    }],
    "title_phrase_roles": [{
      "text": "exact title phrase or punctuation",
      "role": "brand|core-keyword-precise|core-keyword-broad|core-keyword-long-tail|attribute-feature|style-modifier|quantity|punctuation",
      "intent": "distinct shopper search or reading job",
      "coverage_basis": "observed-data|semantic-hypothesis",
      "fact_ids": ["fact-id"],
      "reason": "why included"
    }],
    "rejected_title_terms": [{
      "text": "unused candidate phrase",
      "reason": "user-excluded|unsupported|duplicate-synonym|no-distinct-intent|subjective-marketing|low-decision-value|meaningless-quantity|character-budget|internal-field"
    }],
    "title_review": {
      "character_count": 0,
      "field_limit_status": "verified|unknown-recheck-required",
      "alternatives_count": 2,
      "candidate_count": 3,
      "intent_group_count": 2,
      "core_term_frontloaded": true,
      "semantic_groups_complementary": true,
      "precise_core_term_count": 1,
      "broad_or_alternate_discovery_path_count": 1,
      "complementary_long_tail_count": 1,
      "high_value_attribute_count": 2,
      "coverage_sufficient_for_available_evidence": true,
      "not_underexpanded": true,
      "deduplicated": true,
      "readable_russian": true,
      "punctuation_natural": true,
      "quantity_decision_relevant_or_omitted": true,
      "all_title_candidates_no_sku": true,
      "no_sku_internal_or_excluded_fields": true
    },
    "description": "Approved Russian description",
    "description_fact_ids": ["fact-id"],
    "search_tags": [{
      "term": "Russian query",
      "intent": "shopper intent",
      "evidence": "observed|hypothesis",
      "source": "source reference",
      "fact_ids": ["fact-id"],
      "destination": "title|description|attribute|search_tags"
    }],
    "seasonality": {
      "applied": false,
      "terms": [],
      "fact_ids": [],
      "rationale": "why season language is supported or omitted"
    },
    "copy_review": {
      "category_formula_checked": true,
      "field_limits_status": "verified|unknown-recheck-required",
      "all_claims_sourced": true,
      "no_keyword_stuffing": true,
      "russian_editorial_pass": true,
      "brand_evidence_policy_pass": true,
      "excluded_visible_fields_respected": true,
      "title_intent_coverage_pass": true,
      "title_keyword_ledger_pass": true,
      "title_underexpansion_gate_pass": true,
      "title_candidate_comparison_pass": true,
      "title_modifier_evidence_pass": true,
      "title_quantity_policy_pass": true,
      "title_and_description_identifier_leakage_pass": true,
      "unconditional_title_sku_ban_pass": true,
      "claim_ladder_pass": true,
      "strong_claim_evidence_pass": true,
      "offer_policy_pass": true,
      "information_structure_and_density_pass": true,
      "microcopy_mode_pass": true,
      "abstract_explanation_deletion_pass": true,
      "mobile_microcopy_scan_pass": true,
      "all_visible_strings_role_gated": true,
      "no_internal_status_strings": true,
      "model_identifier_policy_pass": true,
      "variant_consistency": true
    }
  }
}
```

Also record `platform_check.urls` and `platform_check.field_limits`. Use exact `title_max`, `description_max`, and source only when retrieved from the current official category template or Seller cabinet; otherwise store unknown values with the retrieval failure and mandatory upload-time recheck. Every factual modifier and tag must reference confirmed facts. An included brand or public model must link to explicit evidence and must not appear in `excluded_visible_fields`; an omitted brand may use an empty fact list with its internal omission status. `hypothesis` means semantic relevance, never proven demand.

Record the selection and design strategy with evidence-bearing structures:

```json
{
  "user_provided_reusable_assets": [{
    "asset_id": "asset-id",
    "type": "size-chart|after-sales|package|care|other",
    "source": "path or user reference",
    "scope": "why it is reusable",
    "rebuild_requested": false
  }],
  "excluded_from_generation": [{
    "image_type": "covered image type",
    "asset_id": "asset-id",
    "reason": "existing reusable asset covers this need"
  }],
  "set_strategy": {
    "microcopy_default": "phrase-first|sentence-when-needed|instructional",
    "primary_colorway": {"variant": "confirmed variant or source identity", "fact_ids": ["fact-id"]},
    "secondary_colorway": {"variant": "optional confirmed variant", "fact_ids": ["fact-id"], "allowed_slide_ids": ["slide-id"], "rationale": "decision value"},
    "color_series_page": {"included": false, "rationale": "confirmed color choice is or is not decision-relevant"},
    "component_grammar": {
      "visual_components": ["whitespace", "columns", "rules", "card-shapes", "color-fields", "annotation-paths", "product-scale", "crop", "grouping", "rhythm", "safe-zones"],
      "optional_text_components": ["headline", "eyebrow", "model-line", "subheadline", "bullet", "card-label", "badge", "chip", "callout", "footer", "progress-mark"],
      "text_policy": "include only when a visible string passes the role gate"
    },
    "layout_archetype_target": {"minimum_distinct": 4, "rhythm_rationale": "planned page-to-page variation"},
    "information_structure_target": {"minimum_distinct": 3, "rationale": "vary hierarchy and proof expression without repeating selling points"}
  },
  "rejected_internal_strings": [{
    "text": "candidate string rejected before generation",
    "reason": "internal-status|production-filler|navigation-filler|seller-backend|no-shopper-value",
    "disposition": "omit or replace with shopper-facing decision information"
  }]
}
```

Every slide must also include:

```json
{
  "image_type": "hero|core-benefit|usage-scene|multi-angle|atmosphere|detail|brand-story|size-capacity-size-chart|comparison|specification|process|package-accessories|series|composition|after-sales|usage-advice|other",
  "selection_source": "user|automatic",
  "selection_reason": "why this page was selected and why the information is useful",
  "primary_fact_ids": ["fact shown primarily on this page"],
  "supporting_fact_ids": ["facts used only as context"],
  "novel_information": "what this page tells the shopper that slides 2–10 do not repeat",
  "colorway_role": "primary|secondary|series|not-applicable",
  "layout_archetype": "hero-stage|split-editorial|full-bleed-macro|single-detail-hero|annotated-path|structure-card|data-panel|scene-narrative|catalog-grid|other",
  "component_stack": ["components used in hierarchy order"],
  "visual_rhythm_role": "open|dense|detail|scene|data|transition|close",
  "microcopy_mode": "phrase-first|sentence-when-needed|instructional",
  "detail_evidence_mode": "full-bleed-macro|single-detail-hero|precise-annotation-path|structure-card|full-product-locator|not-detail",
  "combined_detail_rationale": "required only when locator and inset prove different information",
  "selling_point": "Level 1 shopper hook or decision answer",
  "consumer_benefit": "Level 2 natural Russian phrase of 2-6 words, a necessary sentence in a justified non-phrase mode, or null",
  "support_facts": [{
    "text": "Level 3 evidence-linked support point; prefer 1-4 words for a card/callout in phrase-first mode",
    "evidence_ids": ["fact-id"],
    "claim_strength": "fact|supported-benefit|marketing-claim",
    "visible_copy_role": "bullet|badge|callout|annotation"
  }],
  "evidence_ids": ["all evidence supporting the page claim ladder"],
  "claim_strength": "fact|supported-benefit|marketing-claim",
  "visible_copy_roles": {
    "headline": "exact visible headline",
    "subheadline": "exact visible benefit line or null",
    "bullet": ["exact visible support point"],
    "badge": ["exact neutral factual badge text"],
    "callout": ["exact visible annotation or callout"]
  },
  "offer": null,
  "information_levels_used": [1, 2, 3],
  "information_layer_exception": null,
  "microcopy_deletion_test": {
    "adds_distinct_purchase_meaning": true,
    "shorter_phrase_preserves_meaning": false,
    "abstract_explanatory_tone": false,
    "translationese": false,
    "mobile_scan_pass": true,
    "decision": "keep|compress|delete"
  },
  "omitted_claims_and_reasons": [{"claim": "candidate claim", "reason": "unsupported|too-strong|duplicate|irrelevant|platform-disallowed|expired-offer"}],
  "visible_strings": [{
    "text": "exact frozen consumer-visible string",
    "role": "shopper-identity|decision-answer|sourced-fact|necessary-instruction",
    "fact_ids": ["fact-id when factual"],
    "shopper_value": "why this exact string helps the purchase decision",
    "required": true
  }],
  "auxiliary_copy_rationale": null,
  "purpose": "internal production job",
  "buyer_question": "shopper uncertainty",
  "decision_message": "complete answer supported by confirmed facts",
  "headline_kind": "identity|choice|configuration|construction|quantified-spec|use|package|compatibility|care|limitation|comparison|brand|text-free",
  "shopper_headline_rationale": "why the title helps a purchase decision without adding an unsupported outcome",
  "title": "shopper-facing Russian headline"
}
```

Set `auxiliary_copy_rationale` to a concrete explanation only when an eyebrow, model line, subheadline, bullet, card label, badge, chip, callout, footer, or progress string is present and necessary; otherwise keep it `null`.

Treat `selling_point`, `consumer_benefit`, `support_facts`, `evidence_ids`, `claim_strength`, `visible_copy_roles`, `information_levels_used`, `information_layer_exception`, `microcopy_mode`, `microcopy_deletion_test`, and `omitted_claims_and_reasons` as internal planning fields; never render their field names in consumer artwork. Target two to four distinct `support_facts` when Level 3 is used, but allow fewer with a truthful exception instead of filling the list. Count Russian words by natural space-separated lexical units for the phrase targets; punctuation does not justify extra words. A justified `sentence-when-needed` or `instructional` page may exceed the phrase target, but must record why compression would lose necessary decision meaning. When Level 4 is allowed, replace `offer: null` with an object containing exact text, evidence IDs, validity/expiry, and the current platform-rule decision.

Add `set_strategy.user_selected_types` with zero to eight normalized values, remove types covered by `excluded_from_generation` from the new-generation count, and add `set_strategy.automatic_types` with the product-specific values needed to reach ten newly generated pages. Add `localization_review.pre_generation_checks.shopper_headline_quality: true`, `visible_string_role_gate: true`, and `claim_ladder: true` only after the Agent records why each gate passes. Add `agent_qa.slide_reviews` with ten evidence-bearing review objects and a set-level contact-sheet review containing the required distributions, counts, and fail decisions. Do not use unexplained `manual_qa: true` flags as a substitute for written review.
