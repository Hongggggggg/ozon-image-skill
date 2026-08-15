# Ozon image-set design rules

Treat high-performing or competitor images as design hypotheses, never proof of causation or conversion lift without controlled data.

## Complete artwork

- Generate every page as one finished AI image; do not plan post-generation overlays.
- Reserve real negative space for copy and keep text outside the product silhouette.
- Keep the exact product dominant and recognizable at thumbnail size.
- Prefer one primary detail evidence mode. Place a detail enlargement beside the main product only under the locator-plus-inset exception below.
- Align dimension arrows to the sourced extrema and axis of the exact named quantity; never reuse a shaft, heel, sole, platform, foot, or package dimension as a proxy for another value.
- When evidence supplies a numeric option but not visible measurement endpoints, use text-only labels and keep the product silhouette and proportions unchanged.
- Regenerate complete pages with misspelled Russian, collisions, distortions, floating crops, or misleading measurements.

## Set-level design grammar

Define a reusable component grammar before prompting. Start with non-text visual components: whitespace, columns, rules, card shapes, color fields, annotation paths, product scale, crop, grouping, rhythm, and safe zones. Define their spacing, alignment, shape language, and hierarchy at set level.

Treat headline, eyebrow/model line, benefit subheadline, bullet, card label, neutral fact badge, chip, callout, footer, and progress mark as optional text components. Add one only after its exact string passes the visible-string role gate in [listing-copy.md](listing-copy.md). Do not add text merely to make the hierarchy look richer. An empty footer, non-text progress device, color block, rule, or spacing relationship may carry the visual system without consumer-visible wording.

Assign each slide a `layout_archetype`, `component_stack`, and `visual_rhythm_role`. Useful archetypes include `hero-stage`, `split-editorial`, `full-bleed-macro`, `single-detail-hero`, `annotated-path`, `structure-card`, `data-panel`, `scene-narrative`, and `catalog-grid`. Use at least four materially different archetypes across ten pages. Vary dense, open, detail, scene, and data pages intentionally; do not equate “one decision message” with “one large headline plus one product.”

The system must feel related without being templated: preserve component grammar and visual identity while changing spatial organization, evidence mode, and information density.

## Information structures and density

Express the claim ladder through composition, not a fixed text template. Useful structures include:

- headline plus benefit subheadline plus two-to-four proof callouts;
- headline plus two or three short selling-point or fact cards, with no subtitle when it would add no meaning;
- headline plus a short proof list or neutral fact cards;
- macro/detail visual with precise annotation lines and short labels;
- decision number or composition/parameter panel with one explanatory line;
- evidence-backed comparison block;
- scene plus one benefit line and a small set of use-context facts.

Use at least three materially different information structures across the ten-page set. Do not require every page to contain the same number of lines or components. A neutral number/composition badge may present a sourced fact, but never imitate an award, certification, discount, or unsupported performance badge.

Maintain clear hierarchy: Level 1 must scan first, optional Level 2 must add meaning rather than paraphrase, and Level 3 must visibly support the same selling point. Visual hierarchy does not require sentence hierarchy: product scale, spacing, grouping, cards, annotation paths, color fields, and type scale may separate levels while the copy remains short. For fashion, footwear, beauty, food, and similar visual categories, default to phrase-first microcopy: Level 2 targets two to six natural Russian words and Level 3 cards/callouts target one to four. Do not add a long subheadline merely to make the page appear layered.

Inspect phrase-first pages at mobile/contact-sheet size. The headline and two or three short terms should be scannable without reading a paragraph. Compress or remove abstract design commentary, obvious causal explanations, and translation-like phrasing. A sentence is acceptable only when the manifest uses `sentence-when-needed` or `instructional` and explains what necessary decision meaning would be lost by shortening it.

Avoid thin pages that use only a large headline and excessive empty area when distinct benefit/proof evidence is available. Also avoid dense pages with many small labels, repeated facts, or text too small for mobile viewing.

## Set planning

- Start from ten distinct buyer questions and confirmed facts.
- Preserve up to eight user-selected image types and automatically select the remaining types; follow [image-selection.md](image-selection.md).
- Make slide 1 a current-rule-compliant hero.
- Do not require scene, benefits, dimensions, details, materials, or white-background pages.
- Merge pages that reuse evidence or answer the same question.
- Let the hero summarize several priority facts. Make every page from 2 through 10 contribute different primary information.
- Repeat a hero fact later only when the later page adds deeper proof, measurement, configuration, limitation, or context. Do not repeat the same headline, decision message, claim cluster, or visual explanation.
- Treat a different angle, crop, background, scene, icon arrangement, or wording as repetition when the shopper learns the same thing.
- Use scenes only to prove fit, scale, handling, placement, use, or outcome.

Before generation, build an information-coverage matrix with one row per confirmed fact and one column per slide. Mark each use as `primary`, `supporting`, or `hero-summary`. Outside the hero, assign a fact as `primary` on only one page. Supporting repetition is allowed only when necessary for comprehension and must not dominate the page.

## Colorway concentration

- Select one evidence-linked primary colorway and at most one evidence-linked secondary colorway.
- Use the primary colorway on at least 70% of identity-sensitive pages unless the product's confirmed color choice is a central buyer question and the manifest records a different rationale.
- Restrict the secondary colorway to explicitly listed pages. Do not alternate primary and secondary colors page by page or use color changes as a substitute for layout rhythm.
- Create a colors/series page only for confirmed variants when the choice materially helps selection. Never derive a catalog color name from visual appearance alone.

## Detail evidence modes

Choose one primary evidence mode for each detail page:

- `full-bleed-macro`;
- `single-detail-hero`;
- `precise-annotation-path`;
- `structure-card`;
- `full-product-locator`.

Do not default to a full product plus circular or rectangular inset. A locator and inset may coexist only when the locator establishes position and the inset reveals a different layer or fact that is invisible or hard to distinguish at full-product scale. Record separate fact IDs and `combined_detail_rationale`. If both views prove the same seam, surface, control, material, or construction fact, keep only one.

## Purpose-to-headline separation

Treat angle, crop, layout, and page type as internal production metadata, not shopper copy. Build each page through four distinct fields:

1. `purpose`: what the production team must show;
2. `buyer_question`: what uncertainty the page resolves;
3. `decision_message`: the exact supported answer;
4. `title`: the natural Russian shopper-facing expression of that answer.

Example: `show side profile -> what silhouette and heel construction are visible? -> Mary Jane silhouette with low upper and wide heel -> СИЛУЭТ МЭРИ ДЖЕЙН / Низкий верх и широкий каблук`.

Example: `show material close-ups -> what parts use the confirmed material? -> upper, lining, and insole use sheepskin leather -> ВЕРХ, ПОДКЛАДКА И СТЕЛЬКА ИЗ ОВЕЧЬЕЙ КОЖИ`.

Do not let the visual composition generate the headline. `side view`, `detail`, `material`, `round toe`, and similar labels describe what is pictured, not why the page helps the shopper decide.

## Attention hypotheses

- Give the exact product or truthful bundle the largest visual mass.
- When hero text is allowed, use a plain Russian category headline, one meaningful numeric anchor, and one or two supported facts.
- Use strong contrast while preserving exact product color.
- Use context only when it clarifies use.
- Reduce uncertainty with sourced dimensions, quantity, capacity, package contents, material, compatibility, or configuration.

## Conservative design defaults

1. Product/bundle occupies roughly 55–75% of meaningful hero area and 45–70% on supporting pages.
2. Use 3–6 useful information units on a text hero and 4–7 on supporting pages.
3. Target headline height around 7–12% of canvas and body copy around 2.5–4%; verify on the contact sheet.
4. Keep dead background below roughly 20% unless the product remains dominant and the composition informative.
5. Use 3–5 coordinated colors: exact product color, neutral, category scene color, and at most two accents.
6. Use numbers only when sourced and decision-relevant.
7. Keep product identity, palette, typography, lighting, graphic language, Russian tone, spacing, and hierarchy unified across all ten pages while varying composition, crop, and scene intensity.
8. Ban badges, flags, medals, ratings, certifications, and comparisons unless evidenced and currently allowed.
