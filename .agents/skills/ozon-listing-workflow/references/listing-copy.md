# Ozon listing copy rules

## Source hierarchy

Apply sources in this order: current Ozon category template/cabinet fields; current official Seller help; confirmed user product facts; Ozon query analytics or user query exports; current exact-category observations; conservative defaults below.

Never turn a remembered limit, third-party article, competitor pattern, or semantic guess into an Ozon requirement. Record exact official URLs and access date. The live category template overrides generic advice.

Official starting points:

- Image requirements: `https://docs.ozon.ru/global/products/upload/adding-content/image-requirements/`
- Ozon Seller query analytics: `https://seller.ozon.ru/media/news/novaya-analitika-po-zaprosam-tovarov/`

Locate current product-name, description, characteristic, and category-template rules at runtime because navigation and constraints may change.

## Russian marketplace reading habits

Write all shopper-facing copy as natural Russian marketplace communication for Russian Ozon shoppers. Do not translate Chinese wording sentence by sentence, imitate Chinese advertising rhythm, or expose seller-backend and production terminology to shoppers.

- Put the plain product identity and the most decision-relevant confirmed fact early; do not delay them behind atmosphere or slogans.
- Make text easy to scan on a phone: one dominant message per image, short meaningful headings, compact sentences, and predictable fact order.
- Prefer normal Russian ecommerce collocations and category vocabulary over transliteration, word-for-word calques, bureaucratic language, or keyword-shaped fragments.
- Use concrete nouns, verbs, quantities, materials, compatibility, configuration, and limitations. Remove filler such as “high quality,” “ideal choice,” “stylish solution,” “unique design,” or “must-have” unless a specific supported fact makes the statement meaningful.
- Avoid excessive imperatives, exclamation marks, rhetorical questions, first-person seller claims, and emotional pressure. Use a calm, factual, confident tone.
- Do not repeat the same noun or keyword merely to influence search. Russian case, number, word order, and agreement must sound natural in the sentence actually shown.
- Keep technical specifications in the vocabulary Russian shoppers expect for the category and explain an unfamiliar parameter only when it affects the decision.
- Separate audiences: shopper-facing titles, descriptions, and image text must support selection; seller-facing manifests, evidence notes, and QA records may use operational terminology but must never leak into the artwork.

During the editorial pass, read every Russian string as a complete shopper message rather than checking isolated words. Reject text that is grammatically possible but sounds translated, stiff, vague, overpromotional, or unlike a normal Russian Ozon listing.

## Keyword ledger

Build a new candidate ledger for each product before drafting a title. For each term record exact Russian wording, normalized shopper intent, layer, `observed-data` or `semantic-hypothesis`, source/date, supporting fact IDs, time sensitivity, destination, and inclusion/exclusion reason. Use these layers:

- `core-precise`: exact product type or strongest precise shopper phrase;
- `category-broad`: broader category wording that creates a genuinely different discovery path;
- two or three complementary `intent-group` values covering distinct needs such as product type, audience, season, use, construction, compatibility, or configuration;
- `long-tail`, `audience`, `season`, `material`, `structure-attribute`, `differentiating-benefit`, and `style-trend` candidates;
- `quantity` only when count changes the purchase decision;
- `brand` only when provided, evidenced, and not excluded.

Apply data priority in this order: Ozon query analytics/user keyword data; documented current same-category Ozon search observations; official category attributes and natural Russian shopper vocabulary; semantic candidates derived from confirmed facts. `observed-data` requires actual query data or a dated documented current search observation. `semantic-hypothesis` means only semantic relevance; it never means popular, frequent, trending, effective, or high-converting.

Deduplicate case, number, word-order, and weak-synonym variants. Exclude competitor brands, unrelated audiences, unsupported problems, and traffic bait such as “gift,” “premium,” or “best” unless true, allowed, and relevant.

## Title construction

Use the live Ozon category formula and current field maximum when available. Otherwise build a natural Russian sequence from `[brand when evidenced and allowed] + precise core term + broad/different discovery path + one or two complementary long-tail intents + two to four high-value supported attributes/selling points + restrained evidence-consistent trend/style term when justified + decision-relevant quantity`. Keep the product type and strongest precise intent early. Optimize jointly for accurate identification, relevant search coverage, filter/category matching, Russian readability, and purchase judgment—not the shortest possible title and not maximum keyword density.

### Brand and identifier gate

Treat `brand` as nullable. Include it only when user data, a product table, or trustworthy product evidence explicitly establishes it and `excluded_visible_fields` allows it. A clearly legible authentic brand label may be evidence; a guessed mark, image/file/folder name, store name, or seller name is not. Never invent a brand, use a placeholder brand, or convert a store name into a brand. When brand is absent, conflicting, uncertain, or user-excluded, record `brand.value: null` and an internal omission status such as `品牌未提供—已省略`; never show that explanation to shoppers.

Never put an SKU in any selected or alternative title. This ban includes `SKU`/`артикул` labels, stock-keeping codes, seller/internal article numbers, backend identifiers, and the bare value of any known SKU. It is unconditional: source availability, public visibility, keyword/search data, field length, user authorization, or a desire for broader coverage cannot permit it. Keep SKU only in internal evidence and operational records; reject it before title drafting and verify all three title candidates. Apply the same ban to the description. Default every model to omitted. Include another model only when evidence establishes it as a public consumer-facing model, there is evidence that shoppers use it for product identification/search, and it is not excluded. A genuine public model is not automatically an SKU, but any value used internally as the SKU remains forbidden in the title. User instructions in `excluded_visible_fields` override all source fields and exact values for their recorded scopes; do not restore excluded content merely because it exists in the table.

### Search-intent groups

Choose terms independently for the current product; never fill a fixed title template. When category language and evidence allow, cover two or three semantically complementary groups:

1. `core-keyword-precise`: the exact product type or precise shopper phrase;
2. `core-keyword-broad`: a broader category phrase that adds a different discovery path;
3. `core-keyword-long-tail`: a high-relevance phrase for audience, season, use, construction, compatibility, or configuration.

Do not count synonyms, inflections, reordered words, singular/plural variants, or near-identical category names as separate groups. Select one precise core term, one broad or alternate discovery path, one or two complementary long-tail intents, and two to four high-value attributes when truthful and useful. Every group needs a distinct intent in `title_phrase_roles`. If query analytics or documented search observation supports a phrase, use `coverage_basis: observed-data`; otherwise use `semantic-hypothesis` and label the overall plan `semantic-coverage`. Never call semantic coverage high-volume, popular, trending, hot, or conversion-driving.

### Attributes, style, and quantity

| Element | Include when | Exclude when |
| --- | --- | --- |
| Audience | Explicit positioning or category attribute supports it | Appearance alone suggests gender, age, or profession |
| Material | Supplied and decision-relevant | Guessed from texture |
| Feature/construction | Specific, provable, and useful | Vague, subjective, or redundant |
| Use/compatibility | Exact supported task, model, or standard | Based on “universal” assumptions |
| Size/capacity/color | Variant-defining or category-relevant | Confusable, unsupported, or user-excluded |
| Season | Season attribute and construction evidence agree | Added for traffic or appearance alone |
| Style/texture | Restrained and consistent with direct evidence, e.g. `замшевой фактуры` without claiming suede material | Subjective aspiration or material inference |
| Quantity | Pack, set, or included accessory count changes the decision | Default single item, one pair, or count added to fill a formula |

Treat waterproof, warm, orthopedic, non-slip, hypoallergenic, eco, safe, professional, premium, upgrade, elegant, original, `профессиональный`, `премиальный`, `улучшенный`, `элегантный`, and equivalents as evidence-sensitive marketing claims. Prefer factual modifiers such as `женские`, `зимние`, `с меховой отделкой`, or `замшевой фактуры` only when their exact meaning is supported.

### Product-specific candidate gates

Treat “2026 new,” “light luxury,” “comfortable,” “warm,” “hidden height increase,” and “versatile” as candidate directions supplied for evaluation, not a reusable word pack:

- **2026/new:** use a current-year/new-release expression only when evidence confirms a 2026 launch and the term has observed search value or explicit current positioning value. Record the date sensitivity and remove or revalidate it when stale.
- **Light luxury:** do not translate it mechanically as `лёгкая роскошь`. Decompose the actual design into natural supported Russian details such as `лаконичный дизайн`, `металлический декор`, `кристаллы`, or `лаковая фактура`. `Элегантный`, `премиальный`, and similar value judgments still require evidence and must earn their character cost.
- **Comfort:** use comfort wording only when the last, lining, insole, sole construction, tests, or explicit user-authorized selling material supports it. When evidence is weaker, name the concrete structure instead of claiming comfort.
- **Warmth:** when season and construction are confirmed, prefer precise levels such as `зимние`, `утеплённые`, or `с меховой подкладкой`. Temperature ratings, severe-cold suitability, heat retention, or equivalent strong results require adequate tests.
- **Hidden height increase:** use `со скрытым подъёмом` or `со скрытой танкеткой` only for a real internal hidden lift/wedge. Never substitute an exposed thick platform, outsole thickness, heel height, total height increase, or shaft height.
- **Versatility:** prefer restrained, specific Russian such as `на каждый день`, `для повседневных образов`, or `для базового гардероба` when use evidence/positioning supports it and it adds a worthwhile discovery path. Reject absolute match-all claims and omit the phrase when it adds little beyond stronger attributes.

These examples define evaluation logic, not mandatory vocabulary. A different product must produce a different ledger and may reject every example direction.

### Punctuation, budget, and output

Use commas, a short dash, or a semicolon to separate real semantic blocks when this improves Russian readability. Do not copy Amazon's 200-character convention. Retrieve the current Ozon/category limit at runtime; if unavailable, record `unknown — recheck at upload` and optimize for natural coverage without inventing a maximum.

Draft at least one selected title and two alternatives. Score each for product identity, live category formula, two-to-three distinct intent groups where allowed, core-term frontloading, evidence support, variant clarity, natural Russian, punctuation, character budget, repetition, relevant search/discovery value, precision, purchase-decision value, and absence of internal/excluded fields. Record `title_keyword_ledger`, `title_candidates`, `title_phrase_roles`, `rejected_title_terms`, and `title_review`. Show only the selected title to the consumer unless the user requests comparison; keep alternatives and analysis in the manifest/QA.

Reject unsupported candidates regardless of score. Avoid all-caps, emoji, repeated punctuation, seller names, prices, discounts, calls to action, ratings, rankings, competitor names, keyword chains, and synonym repetition. Also reject under-expansion: when the ledger contains two or three truthful complementary intents and several high-value attributes but the title uses only the product name plus one or two modifiers, rewrite it with broader relevant coverage. Anti-stuffing is not a reason to discard useful supported search paths.

## Description

Use short connected paragraphs. Include only relevant sections: allowed shopper identity and main supported benefit; intended use/audience; construction/material; dimensions/fit/capacity/compatibility; package contents; care, setup, or limitations.

Do not include an SKU, internal article number, backend identifier, known bare SKU value, or any field/value listed in `excluded_visible_fields` for the description scope. Apply the same public-model evidence gate used for the title. Do not duplicate the characteristic table or upgrade a characteristic into an unsupported performance result. Keep allowed identity terms near the beginning naturally. Exclude links, contacts, social handles, price/promotion/delivery claims, unsupported warranty, competitor comparisons, rankings, review claims, urgency, and unsupported health or safety outcomes.

## Selling-point claim ladder

Plan image copy as an evidence ladder, not as extra words around a large title:

1. **Hook / selling point:** one clear, scannable decision message.
2. **Benefit / descriptor:** an optional short shopper descriptor or restrained experience phrase; it does not need to explain why or form a complete sentence.
3. **Proof:** two to four distinct evidence-linked attributes, ingredients/materials, structures, parameters, use contexts, detail annotations, or supported comparison points; cards and callouts should normally be phrases.
4. **Offer:** optional and only when the user explicitly supplies current terms, evidence confirms validity/expiry, and current Ozon/category rules allow it on that page.

Default non-hero pages to at least two truthful levels; give important selling-point pages three when evidence supports them. A headline plus two or three short selling-point/fact cards is a valid gradient; visual hierarchy is not sentence hierarchy. Do not force a subtitle, benefit, or two-to-four proof points. When Level 1 already communicates the complete answer and no distinct benefit/proof exists, set `consumer_benefit: null`, record `information_layer_exception` and the omitted claim reason rather than paraphrasing or inventing.

### Phrase-first microcopy

Set `microcopy_mode: phrase-first` by default for fashion, footwear, beauty, food, and other visually led products. In natural Russian, target two to six words for Level 2 and one to four words for Level 3 card/callout copy. Prefer noun phrases, adjective phrases, direct attribute phrases, and brief evidence-supported experience phrases. Use `sentence-when-needed` only when a complete sentence carries necessary choice, limitation, compatibility, or use meaning that a shorter phrase would lose; use `instructional` only for necessary instructions.

`consumer_benefit` is optional. It may be a short descriptor such as `Мягкий короткий ворс`, `Объёмный силуэт`, or `Мягкое ощущение`; it is not required to answer “why” in sentence form. Set it to `null` when it adds no meaning beyond the headline. Never convert a headline into a longer causal sentence merely to fill Level 2.

Apply an abstract-explanation deletion test to every subtitle and short card. Delete or compress it when it:

- comments on styling, visual design, or the copy itself instead of naming an attribute, use, choice, or supported experience;
- narrates an obvious causal relationship without adding a purchase-relevant fact;
- uses vague destinations such as “for the winter wardrobe” or claims to “highlight the model's lines” without resolving a buyer question;
- sounds like a literal translation or formal copy analysis rather than language a Russian shopper scans naturally;
- can be removed without changing the shopper's decision, or can be shortened without losing supported meaning.

This is a tone-and-value test, not a fixed banned-word list. A phrase may be valid in another context only when it adds concrete, evidenced decision value. Record the result in `microcopy_deletion_test` as `keep`, `compress`, or `delete`.

Map each candidate through `feature -> benefit -> experience` and label claim strength:

- `fact`: directly verifiable attributes such as artificial short-pile lining, thick rubber sole, round toe, mid-calf shaft, gentle ruching, or side buckle when supported;
- `supported-benefit`: a restrained implication tightly connected to evidence, such as a soft wrapping feel, soft-touch surface, or a round-toe silhouette with more visual toe room;
- `marketing-claim`: strong comfort, performance, health, or experiential wording allowed only with adequate wearing tests, material/structure proof, performance evidence, or explicit authorized marketing material.

Do not upgrade `fact` to `supported-benefit` merely to make copy warmer. Do not upgrade either to `marketing-claim` because the user supplied an example phrase. Prohibit cloud-walking effects, cotton-like footfeel, maximum comfort, all-day fatigue relief, heat retention, rebound cushioning, slip resistance, therapeutic/health effects, absolutes, and similar outcomes without the required evidence.

Localize the meaning for Russian shoppers; never translate Chinese internet slang word for word. When evidence supports only a neutral benefit, downgrade slang or hyperbole to natural restrained Russian. Record the removed strong phrase in `omitted_claims_and_reasons`.

Footwear examples, not reusable templates:

- Weak: `МЯГКОСТЬ` as an isolated large headline.
- Abstract/translated: `Выразительный силуэт для зимнего гардероба`; compress to `Зимний образ` only when it adds supported decision value, otherwise omit.
- Explanatory: `Складки формируют объёмный силуэт`; compress to `Объёмный силуэт` when the visible construction supports it.
- Lining, only when supported: `Мягкий короткий ворс`; add `Комфортное ощущение` only when material/structure evidence or explicit user authorization supports that experience.
- Forbidden without testing: `ЭФФЕКТ ХОЖДЕНИЯ ПО ОБЛАКУ`, `МАКСИМАЛЬНЫЙ КОМФОРТ`, `НОГИ НЕ УСТАЮТ ВЕСЬ ДЕНЬ`.

Do not copy the better example into another product. Rebuild every ladder from that product's own evidence and Russian category vocabulary.

## Visible-string role gate

Before freezing any image copy, enumerate every exact string that could appear in the artwork: headline, eyebrow, model line, benefit subheadline, bullet, card label, badge, chip, callout, footer, progress mark, annotation label, and instruction. Do not review only the headline.

Assign each approved string exactly one role:

- `shopper-identity`: natural product identity, plus brand or public model only after evidence and `excluded_visible_fields` gates pass;
- `decision-answer`: the supported answer to the page's buyer question;
- `sourced-fact`: a concrete material, quantity, dimension, compatibility, construction, package, care, or limitation fact;
- `necessary-instruction`: a short instruction required to use, choose, measure, or interpret the product correctly.

For every string record exact text, role, fact IDs when factual, shopper value, and `required`. If a string cannot fit one role, or removing it leaves purchase understanding unchanged, reject it. Store rejected candidates in `rejected_internal_strings`; do not send them to image generation.

Reject internal evidence/status, production/navigation filler, seller-backend terms, and their Russian, English, Chinese, or other-language equivalents. Forbidden examples include `confirmed`, `verified`, `evidence`, `source`, `fact`, `QA`, `manifest`, `selection`, `automatic`, `SKU`, `ПОДТВЕРЖДЕНО`, `ПРОВЕРЕНО`, `ИСТОЧНИК`, `ФАКТ`, `МАНИФЕСТ`, `ВЫБРАНО`, `АВТОМАТИЧЕСКИ`, `АРТИКУЛ`, `已确认`, `已验证`, `证据`, `来源`, `事实`, `质检`, `清单`, `自动`, and `货号` when used as internal labels. Never show evidence summaries such as `ТРИ ПОДТВЕРЖДЁННЫХ МАТЕРИАЛА`.

Treat a permitted public model differently from an SKU label, but default models to omitted. Never show an SKU label, internal article label, or known bare SKU value in the title or description. The notation `<KNOWN_SKU_VALUE>` is an internal rule-document placeholder, not approved visible copy. A public model may appear on at most one shopper-identity image only when explicit evidence supports consumer use and the user has not excluded it. When `excluded_visible_fields` contains a brand, model, SKU, internal identifier, or exact value for images, omit it entirely from artwork, footer, progress device, watermark, and model line.

Default generic eyebrow and section labels to absent. `МАТЕРИАЛЫ`, `ДЕТАЛЬ`, `ФАКТУРА`, `КОНСТРУКЦИЯ`, `СЕЗОН`, `ВНЕШНИЙ ВИД`, `СИЛУЭТ`, and equivalents fail when they merely expose the page type. They do not count as hierarchy or decision information. Allow one only when it is natural Russian shopper navigation, accompanies a complete decision-useful message, and `auxiliary_copy_rationale` explains why its removal would reduce understanding. If the page works equally well without it, delete it.

Visual hierarchy does not require extra words. Prefer whitespace, columns, rules, card shapes, color fields, annotation paths, product scale, crop, grouping, and rhythm before adding an eyebrow, chip, footer, or progress text.

## Image headline engineering

Keep internal planning language out of every shopper-visible string. After the visible-string role gate, derive the headline in this order:

`purpose -> buyer question -> confirmed decision message -> shopper headline`

- `purpose` describes the production job and may mention angle, crop, scene, detail, or layout.
- `buyer_question` describes the uncertainty to resolve.
- `decision_message` states the supported answer the shopper should retain.
- `shopper headline` expresses that answer naturally and specifically.

Reject titles that only name production sections or camera treatments: `ВИД СБОКУ`, `ВИД СВЕРХУ`, `ДЕТАЛИ`, `КРУПНЫЙ ПЛАН`, `МАТЕРИАЛЫ`, `ХАРАКТЕРИСТИКИ`, `ФОТО ТОВАРА`, and equivalents.

Reject bare-attribute titles such as `КРУГЛЫЙ НОСОК`, `ОВЕЧЬЯ КОЖА`, `ШЕРСТЬ`, `РЕЗИНОВАЯ ПОДОШВА`, or `ЧЁРНЫЙ ЦВЕТ` when they merely repeat one characteristic. Convert them into a complete decision message using only confirmed facts:

| Weak title | Better supported pattern |
| --- | --- |
| `ВИД СБОКУ` | `СИЛУЭТ МЭРИ ДЖЕЙН` + a factual construction subtitle |
| `КРУГЛЫЙ НОСОК` | `КРУГЛЫЙ НОСОК И НИЗКИЙ ВЫРЕЗ` |
| `ОВЕЧЬЯ КОЖА` | `ВЕРХ, ПОДКЛАДКА И СТЕЛЬКА ИЗ ОВЕЧЬЕЙ КОЖИ` |
| `ШЕРСТЬ` | `ШЕРСТЯНАЯ ПОДКЛАДКА ПО ВСЕЙ ВНУТРЕННЕЙ ЧАСТИ` only when that coverage is sourced |

Do not manufacture a benefit to improve a weak fact. Words such as `комфортный`, `тёплый`, `устойчивый`, `мягкий`, `прочный`, or `безопасный` require direct support. When no outcome is sourced, make the construction, choice, quantity, compatibility, limitation, or configuration more complete instead.

Headline gate for every slide:

1. The title is not the `purpose` or a translation of it.
2. The title answers the buyer question with a supported decision message.
3. The title is more informative than a section label or one isolated attribute.
4. Every implied outcome is sourced.
5. Title, subtitle, and visual proof describe the same fact and variant.
6. A shopper can understand why the page matters without seeing the internal page type.

## Numeric and measurement semantics

Before freezing any numeric image copy, write the fact as `value + unit + measured quantity + evidence source`. Do not shorten away the measured quantity when that would make the value ambiguous. Overall height increase is not shaft height, heel height, sole thickness, or platform height; foot length is not insole length unless the source explicitly equates them; package dimensions are not product dimensions.

The headline, labels, arrows, and product proportions must all express the same measured quantity. If the source confirms a numeric option but does not show where or how it is measured, present the option as a factual text choice without measurement arrows or geometry changes. A correct number with the wrong visual referent is a factual failure, not a styling issue.

## Tags and field mapping

“Search tags” are a structured delivery artifact, not a promise that every category exposes a field called tags. Map filter terms to Ozon characteristics first; use a dedicated keyword field only when the current template exposes it; retain other useful terms in `listing-content.json`. Keep the set compact. Every term needs source, evidence label, intent, fact IDs, and destination.

## Final audit

Confirm that title, description, tags, attributes, images, selected variant, quantity, package contents, measurements, allowed brand, and any eligible public model refer to the same product. Confirm that `excluded_visible_fields` is respected everywhere, brand is omitted when null or unconfirmed, title intent groups are complementary, quantity is decision-relevant or omitted, every modifier has evidence, observed/semantic-coverage labels do not overstate demand, Russian grammar and units are correct, shopper-facing text passes the Russian marketplace reading-habit review, and field lengths match current recorded constraints.
