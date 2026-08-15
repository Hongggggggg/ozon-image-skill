# Agent-only Ozon listing QA

The Agent performs every validation decision. Do not use validation scripts, OCR scripts, image-difference scripts, automated scoring, or generated PASS flags. Directly inspect the evidence, copy, full-resolution images, and contact sheet. File metadata may be read directly, but it cannot replace visual and editorial judgment.

## 1. Evidence review

For every product, read every supplied row, document, label, package record, and product image. Record:

- exact SKU, product type, variant, material, quantity, package contents, sizes or dimensions;
- which visible construction details each source view actually supports;
- missing views that prohibit underside, interior, on-body, measurement, accessory, or package depictions;
- every user-provided reusable asset, its covered image type, source, reusable scope, and whether a rebuild was requested;
- contradictions and the conservative decision used.

Do not approve a listing while a variant-defining fact is ambiguous. A textual package-content fact supports copy, but an exact visual depiction of an included accessory still requires an image reference. Without it, use text-only package information or request a source image.

## 2. Copy review

Review title, description, tags, characteristics, and every image string as a Russian ecommerce editor and an Ozon category specialist.

Reject shopper-facing copy that is literal Chinese-to-Russian translation, seller-backend language, a keyword pile, bureaucratic Russian, empty promotional wording, or an unnatural collocation. Confirm that a Russian shopper can scan the product identity and decisive fact quickly and that each text block carries one clear message.

Review the selected title and at least two alternatives before consumer delivery. Require `title_keyword_ledger`, `title_candidates`, `title_phrase_roles`, `rejected_title_terms`, and `title_review`. Confirm:

- brand is included only with explicit trustworthy evidence and is not user-excluded; otherwise `brand.value` is `null` with an internal omission reason;
- no brand is invented from an image/file/folder name, store name, seller name, placeholder, or ambiguous mark;
- `excluded_visible_fields` overrides every populated table or evidence field/value across its recorded title, description, tags, and image scopes;
- the selected title and every alternative contain no SKU, `SKU`/`артикул` label, stock-keeping code, seller/internal article number, backend identifier, or bare value of any known SKU; this is unconditional and cannot be overridden by source data, public visibility, keyword coverage, or user authorization;
- the description contains no SKU, internal article number, backend identifier, known bare SKU value, or identifier/value excluded for that scope;
- any other model is included only when evidence establishes a public consumer-searchable model and the user allows it;
- the product-specific ledger separates precise core, broad category/discovery, two-to-three complementary intent groups, long-tail, audience, season, material, structure/attribute, differentiating benefit, style/trend, decision-relevant quantity, and eligible brand candidates;
- source priority is query analytics/user keyword data, then dated current Ozon observations, then official category attributes/natural Russian vocabulary, then fact-derived semantic hypotheses;
- the title contains one precise core term, one broad or alternate discovery path, one or two complementary long-tail intents, and two to four high-value attributes when category, evidence, and field budget allow;
- the title contains two or three semantically different search-intent groups when the category and evidence allow, rather than synonymous or reordered duplicates;
- each term is labeled `observed-data` or `semantic-hypothesis`, and the overall no-data plan is labeled `semantic-coverage`, without unsupported search-volume, popularity, trend, or conversion claims;
- factual attributes and restrained style/texture terms are supported, while premium/upgrade/professional/elegant claims and equivalents are omitted without direct evidence;
- 2026/new-release wording has confirmed launch evidence plus observed search or explicit positioning value and a time-sensitivity review;
- `лёгкая роскошь` is not used as a mechanical translation; any light-luxury direction is decomposed into supported natural design facts;
- comfort wording has last/lining/insole/sole/test or user-authorized support; winter/warmth wording matches its evidence strength; hidden-lift wording proves a real internal lift rather than an exposed platform, total increase, heel, sole, or shaft measurement; versatility wording is restrained, specific, and worth its title space;
- quantity appears only when pack, set, or accessory count changes the decision; default single-item or one-pair wording is omitted;
- the plain product type/core term and strongest precise intent are early, punctuation separates real semantic blocks, current Ozon field limits are verified or marked unknown, and no remembered Amazon length rule is used;
- each candidate records character count, repetition, Russian naturalness, coverage source, linked facts, internal search/discovery value, precision, purchase-decision value, and rejected terms/reasons;
- the selected title is neither under-expanded nor an overlong keyword chain.

Fail the entire title package if the selected title or either alternative contains any SKU representation, including a label plus value or the bare known value; do not repair it by relabeling the SKU as a model or keyword. Also fail for any other internal-number leak, unevidenced brand, violation of `excluded_visible_fields`, fewer than two intent groups when the category/evidence allow, unsupported trend/year/comfort/warmth/hidden-lift/versatility wording, keyword stuffing, synonym repetition, unsupported modifier, meaningless quantity, unnatural punctuation, or internal terminology in title or description. Fail under-expansion when evidence supports two or three complementary intents and several high-value attributes but the title contains only the product name plus one or two modifiers; rewrite with natural, relevant coverage. Preserve the opposite fail gate for an overlong keyword chain, redundant variants, or unnatural Russian.

Review a completed claim ladder for every non-hero page. Require `selling_point`, nullable `consumer_benefit`, `support_facts`, `evidence_ids`, `claim_strength`, `visible_copy_roles`, `microcopy_mode`, `microcopy_deletion_test`, and `omitted_claims_and_reasons`; require `information_layer_exception` when fewer than two levels are used. Confirm that important selling-point pages use three levels when adequate evidence exists, while sparse evidence never triggers invented copy.

Check every non-null Level 2 item against Level 1: it must add shopper value, a direct descriptor, or a restrained supported experience, not restate the headline. For `phrase-first`, target two to six natural Russian words for Level 2 and one to four for each Level 3 card/callout. Check every Level 3 point: it must support the same selling point, be distinct from the other points, link to evidence, and use a meaningful presentation role. Target two to four proof points only when that many truthful points exist. A headline plus two or three truthful short cards passes without a subtitle.

Apply the deletion test before generation and again to observed artwork. Fail or compress copy that sounds like analysis, design critique, empty styling rhetoric, obvious causal explanation, or literal translation; that does not change the purchase decision when removed; or that can preserve all supported meaning in a shorter phrase. Do not treat the examples as a fixed blacklist. A `sentence-when-needed` or `instructional` exception passes only when the manifest states the necessary meaning lost by compression.

Review `claim_strength` explicitly. Direct facts may be stated as facts; supported benefits must remain close to visible/material evidence; marketing claims need adequate test/performance evidence or explicit authorized marketing material. User-provided examples alone are not evidence. Fail unsupported comfort, health, warmth, fatigue, cushioning, rebound, slip-resistance, absolute, or efficacy language and literal Russian translations of Chinese ecommerce slang.

Review Level 4 offers only when the user supplied exact current terms, evidence includes validity/expiry, and current Ozon/category rules permit the offer on the page. Otherwise require `offer: null` and record the omission reason.

Run the visible-string role gate on every planned headline, eyebrow, model line, benefit subheadline, bullet, card label, badge, chip, callout, footer, progress mark, annotation label, and instruction. Approve a string only when it has exactly one role—`shopper-identity`, `decision-answer`, `sourced-fact`, or `necessary-instruction`—plus fact IDs when factual, concrete shopper value, and a justified `required` value. Put every rejected status/backend/filler candidate into `rejected_internal_strings` and keep it out of prompts.

Fail any internal evidence or workflow status in consumer copy, including equivalents of confirmed, verified, evidence, source, fact, QA, manifest, selection, automatic, SKU, or article. Explicit failures include an SKU/article label followed by `<KNOWN_SKU_VALUE>` or the known bare SKU value in the title or description. Treat `<KNOWN_SKU_VALUE>` as an internal documentation placeholder only; its literal appearance in consumer content also fails. A public model may appear on at most one identity page only when evidence and user permissions allow it; never use any model as a repeated model line, footer, watermark, or decoration. Any field or exact value excluded from images through `excluded_visible_fields` fails wherever it appears in image copy.

For each image page, write:

- internal purpose;
- buyer question;
- supported decision message;
- shopper-facing headline;
- why the headline helps a purchase decision;
- fact IDs supporting every claim.

When auxiliary copy exists, also record `auxiliary_copy_rationale`. Apply the removal test: if deleting an eyebrow, model line, subtitle, card label, chip, footer, or progress text does not reduce product identification, decision value, factual understanding, or necessary instruction, delete it.

Fail a headline when it is only a camera angle, section label, layout instruction, or bare attribute. Examples that fail as complete titles include `ВИД СБОКУ`, `ДЕТАЛИ`, `МАТЕРИАЛЫ`, `КРУПНЫЙ ПЛАН`, `КРУГЛЫЙ НОСОК`, `ОВЕЧЬЯ КОЖА`, and `ШЕРСТЬ`.

Do not repair a weak headline with an unsupported outcome. `комфортный`, `мягкий`, `тёплый`, `устойчивый`, `прочный`, `нескользящий`, and similar words require direct evidence. When no outcome is supported, write a fuller factual decision statement.

## 3. Pre-generation page review

Before generating any image, inspect the ten-page copy deck as a set:

- every page answers a distinct, useful buyer question;
- slides 2–10 each introduce different primary information;
- the information-coverage matrix assigns every non-hero primary fact to only one page;
- `user_provided_reusable_assets` and `excluded_from_generation` are complete; no excluded type consumes one of the ten new-generation slots unless `rebuild_requested` is true;
- zero to eight normalized user-selected types are present as mandatory plan items;
- automatic selections fill the remaining slots to exactly ten and record a purchase-decision reason;
- no page exists only to reach ten images;
- titles are decision messages, not labels;
- every planned visible string appears in `visible_strings` and passes exactly one allowed role;
- every non-hero page has a completed claim ladder, uses at least two truthful levels by default, or records a valid `information_layer_exception` when no distinct second layer exists;
- important selling-point pages use a distinct benefit/descriptor and relevant proof points when evidence supports them, or use a headline plus two or three short truthful cards without forcing a subtitle;
- every page records `microcopy_mode`; phrase-first Level 2 and Level 3 cards meet the target lengths or document why a longer mode is necessary;
- every non-null Level 2 and every short card passes `microcopy_deletion_test`, adds distinct purchase meaning, and scans quickly at mobile size;
- every benefit and support point has linked evidence, a valid claim strength, and a visible-copy role; internal claim-ladder field names are absent from frozen consumer copy;
- any Level 4 offer has supplied current terms, validity evidence, and a recorded platform-rule pass;
- `rejected_internal_strings` contains every considered evidence/status, production/navigation filler, or seller-backend string and none of those strings appears in the frozen deck;
- every title/description/image field or exact value in `excluded_visible_fields` is absent from its recorded consumer-content scope even when source data contains it;
- brand is absent from consumer content when `brand.value` is null or status is omitted, and any included brand has explicit linked evidence;
- generic eyebrows such as `МАТЕРИАЛЫ`, `ДЕТАЛЬ`, `ФАКТУРА`, `КОНСТРУКЦИЯ`, `СЕЗОН`, `ВНЕШНИЙ ВИД`, or `СИЛУЭТ` are absent unless a page-specific `auxiliary_copy_rationale` passes the removal test;
- an eligible public model appears on no more than one identity page, never with an SKU/article label or as footer decoration; excluded models appear nowhere;
- `auxiliary_copy_rationale` is populated only on pages that actually contain necessary auxiliary text;
- repeated facts occur only as a justified hero-summary/deeper-proof relationship or as minor context;
- no two supporting pages teach the same fact through different angles, crops, scenes, wording, or layouts;
- one confirmed primary colorway and no more than one confirmed secondary colorway are recorded; visible photo color is not used as an unsourced catalog name;
- the secondary colorway appears only on explicitly allowed pages, and a series/colors page exists only for a confirmed, decision-relevant color choice;
- the reusable component grammar, at least four planned layout archetypes, component stack, and visual-rhythm role are recorded for every slide;
- every detail page selects one primary evidence mode, and every locator-plus-inset combination has separate fact IDs and a rationale for the additional hard-to-see information;
- every number, material, season, audience, compatibility, package item, and benefit links to a confirmed fact;
- exact Russian grammar, agreement, punctuation, units, and line breaks are approved;
- no page requests an unsupported angle, interior, outsole, use scene, accessory appearance, or measurement graphic;
- every number is bound to its exact sourced quantity; height increase, shaft height, heel height, sole thickness, platform height, foot length, and package dimensions are never treated as interchangeable;
- measurement arrows have sourced physical endpoints; when the endpoints or mechanism are not visible in the evidence, the page uses text-only numeric choices and does not change product proportions to simulate the value;
- the hero follows verified current rules or uses the conservative text-free fallback when official rules are unavailable.

Record the approval rationale. Do not proceed because the deck merely looks plausible.

## 4. Full-resolution image review

Open every generated page at full resolution. For each page, record:

1. every visible string exactly as seen, including small eyebrow, chip, footer, progress, and model-line text;
2. comparison with the frozen `visible_strings` array, its allowed role, and its shopper value;
3. product identity: silhouette, color, finish, parts, fasteners, seams, decoration, quantity, and proportions;
4. whether the visual proves the recorded decision message;
5. whether the observed headline, benefit line, and proof points match the frozen claim ladder, add distinct meaning, and remain readable on a phone without covering critical product features;
6. whether phrase-first Level 2 copy remains a natural two-to-six-word phrase and each Level 3 card/callout remains a one-to-four-word phrase, or whether a justified longer mode preserves necessary meaning;
7. whether any unsupported object, package, accessory, badge, claim, logo, number, variation, measurement endpoint, or changed proportion appeared;
8. whether the page duplicates another page or repeats a full-product-plus-inset treatment without new evidence;
9. whether the observed colorway, layout archetype, component stack, detail-evidence mode, and hierarchy match the manifest;
10. pass or fail, with a concrete reason.

One malformed character, extra word, unregistered auxiliary string, visible internal claim-ladder field name, disallowed role, internal status/backend term, changed number, unsupported strong claim, number attached to the wrong physical quantity, altered product part, misleading accessory, unsupported scene, or repeated primary information fails the whole page. Regenerate or AI-edit the complete page, then repeat the full review.

## 5. Contact-sheet review

Inspect all ten pages together and record:

- consistent product identity and selected variant;
- coherent palette, lighting, typography, and visual hierarchy;
- meaningful page-to-page variety without decorative filler;
- buyer-question coverage and logical order;
- different primary information on slides 2–10, with repetition limited to justified hero summary and later proof;
- absence of generic headings and repeated isolated attributes;
- hero strength and thumbnail recognizability;
- balanced information density and mobile readability.

Also record these set-level counts and distributions:

- `layout_archetype_distribution` and the longest consecutive run of the same archetype;
- component hierarchy usage, including pages with only a large headline and product;
- `primary_colorway_page_count`, `secondary_colorway_page_count`, and total identity-sensitive pages;
- full-product-plus-inset page count and whether each inset proves a distinct hard-to-see fact;
- reusable assets excluded from generation and the product-specific pages used as replacements.
- generic eyebrow text and repeat count across pages;
- model identifier count, location, and whether any instance acts as footer or decoration;
- pages whose hierarchy uses non-text components instead of unnecessary labels.
- `information_level_distribution`, `information_structure_distribution`, and pages using a documented layer exception;
- important selling-point pages with only an isolated headline despite available benefit/proof evidence;
- pages where subheadlines paraphrase headlines, proof points repeat or drift from the selling point, or text density harms mobile reading.
- `microcopy_mode_distribution`, phrase-first subtitles over six words, phrase-first cards/callouts over four words, full-sentence short-card count, and pages that fail quick mobile scanning;
- pages containing abstract explanatory tone, translation-like Russian, or a causal sentence created only to populate Level 2.

Fail the contact sheet and rework affected pages when any condition occurs:

1. an excluded reusable asset is regenerated or consumes one of the ten new product-specific slots without an explicit rebuild request;
2. fewer than four materially different layout archetypes appear across the ten pages;
3. three or more consecutive supporting pages use the same dominant archetype, or three or more consecutive pages reduce to only a large headline plus one product without a meaningful supporting component;
4. the declared component grammar is absent in practice, hierarchy is unclear, or component placement changes arbitrarily rather than forming a coherent system;
5. the primary colorway appears on less than 70% of identity-sensitive pages without a documented color-choice rationale, the secondary colorway appears outside allowed pages, or colors alternate mechanically;
6. a colors/series page uses unconfirmed color names or exists without a meaningful color-choice question;
7. more than two supporting pages use the full-product-plus-inset archetype, or any inset repeats the same evidence without revealing a distinct hard-to-see layer or fact;
8. a detail page lacks a recorded primary evidence mode or uses locator plus inset without separate fact IDs and `combined_detail_rationale`;
9. any visible auxiliary string is missing from the role gate, has an internal/status/backend role, or lacks concrete shopper value;
10. any consumer-visible string contains evidence state, QA/manifest/selection language, SKU/article labels, or production/navigation filler;
11. a generic eyebrow is reused on multiple pages, or any generic eyebrow remains when its removal leaves the purchasing information unchanged;
12. a model identifier appears on more than one identity page, carries an SKU/article label, violates `excluded_visible_fields`, or is used as footer, watermark, progress, or decorative repetition;
13. text labels were added only to simulate hierarchy even though whitespace, grouping, rules, cards, color fields, annotation paths, scale, or rhythm could carry the design without them;
14. an important selling-point page contains only an isolated large headline even though distinct benefit or proof evidence is available;
15. a subheadline merely rewrites or repeats the headline instead of adding shopper benefit or meaning;
16. a support point is unrelated to the selling point, duplicates another support point, or was invented to reach two-to-four items;
17. consumer artwork displays internal fields such as `selling_point`, `consumer_benefit`, `support_facts`, `evidence_ids`, `claim_strength`, `visible_copy_roles`, or `omitted_claims_and_reasons`;
18. strong comfort, performance, health, warmth, efficacy, absolute, cushioning, rebound, fatigue-relief, or slip-resistance language lacks the required evidence or authorization;
19. Russian copy directly imitates or literally translates Chinese internet/ecommerce slang instead of omitting or localizing it to an evidence-supported neutral expression;
20. fewer than three materially different information structures appear across the set, text is too sparse despite available proof, or small-copy density makes mobile reading impractical.
21. a phrase-first subtitle exceeds the necessary two-to-six-word target without a justified mode change, or any subtitle is longer than needed to preserve its decision value;
22. auxiliary copy uses abstract rhetoric, design commentary, or translation-like Russian that does not help the shopper choose;
23. Level 2 repeats Level 1, or a causal/explanatory sentence was invented only to satisfy the information gradient instead of using `null` or short proof cards;
24. a phrase-first Level 3 card/callout becomes a full sentence or exceeds the one-to-four-word target without necessary meaning and a recorded exception;
25. the headline, short descriptors, and fact cards cannot be scanned quickly at mobile/contact-sheet size;
26. experience wording such as `Комфортное ощущение` lacks material/structure evidence or explicit user authorization, or stronger comfort/fatigue/cloud claims lack the existing required tests and evidence.

## 6. Platform and delivery review

Record official URLs checked, access date, category decision, and retrieval failures. If current rules cannot be retrieved, mark `conservative-fallback`, use a text-free hero, avoid asserting field limits, and require a Seller-cabinet recheck before upload.

Before delivery, confirm by direct inspection that the folder contains the exact reviewed images and copy files. Write `qa-report.md` in the Agent's own words with per-slide findings and unresolved evidence gaps. Never state that a script validated the package.
