# Category, localization, and compliance rules

## Supported v1 categories

- Footwear
- Home organization, home textiles, and household goods
- Kitchenware and dining products
- Hand tools, power-tool accessories, garden tools, and ordinary automotive accessories
- Consumer-electronics accessories without medical or safety claims
- Sports and outdoor goods
- Pet accessories without health or veterinary claims

Reject or route to a future category-specific workflow:

- clothing other than footwear;
- food, beverages, alcohol, tobacco, or vaping products;
- supplements, medicines, medical devices, diagnostic products, or therapeutic goods;
- hazardous chemicals, pesticides, or controlled products;
- adult products, digital goods, and services;
- any product whose required claim or sale depends on evidence the user cannot provide.

## Common input gate

Require exact product name, category, variant/color, material, quantity, package contents, dimensions, source images, and sourced selling points. A user statement is an acceptable source record; visual inference is not.

If only one product image is supplied:

- preserve its visible angle;
- do not create rear, underside, inside, exploded, open/closed, or worn variants not shown;
- allow simpler background changes, scale-preserving placement, close crops of visible details, and text layouts;
- request more images when a required slide cannot be truthful.

## Footwear adapter

Require:

- pair count and exact colorway/model;
- at least a clear lateral or three-quarter view;
- user-supplied size system and size chart or foot-length mapping;
- construction/material claims supplied by the user;
- sole/outsole/tread photos before showing or describing them;
- on-foot source material before generating an on-foot scene that must preserve exact fit and silhouette.

Do not convert CN/EU/RU sizes from memory. Do not infer waterproofing, warmth, arch support, orthopedic value, slip resistance, natural leather, or season rating from appearance. If a chart is absent, pause before making the dimension/size card.

## Product-specific eight-slide policy

Require slide 1 to be a current-rule-compliant hero. Do not impose a universal sequence on slides 2–8. Rank the buyer questions that can be answered from supplied evidence, then give each remaining page one distinct decision job.

Possible pages include exact-product overview, size/fit, dimensions, construction, feature proof, materials, real details, alternate angles, usage, context, care, package contents, configuration, compatibility, supplied brand story, and sourced comparison. None is mandatory merely because it is common in marketplace templates.

Give every page a unique purpose, buyer question, and selection reason. Merge pages that use the same evidence or answer the same question. In particular, do not create separate material and detail pages when both repeat the same surface, seam, control, or outsole close-ups.

Cover every priority fact at least once. Repeat a fact only when the hero summarizes it and a later page provides deeper proof. If the product lacks eight truthful and useful questions, request more evidence or use a distinct supported exact-product angle; never add decorative scenes or duplicate details only to fill the set.

## Russian localization

All added shopper-facing text must be Russian except real brand names, model identifiers, and legally printed packaging text.

Use a two-pass localization gate:

1. **Pre-generation editorial pass:** approve the exact eight-page copy deck before prompting. Check natural Russian usage, grammar and agreement, ecommerce clarity, fact alignment, and claim safety. Freeze the approved strings.
2. **Post-generation visual pass:** at full resolution, transcribe every visible string on each page and compare it with the approved deck. Check not only spelling but also meaning, naturalness, factual accuracy, line-break ambiguity, numbers, and units. Extra AI-generated text is a failure even when it is grammatically correct.

Do not accept a page because its headline is readable while a smaller label is wrong. One malformed character, invented word, missing qualifier, altered number, duplicated phrase, untranslated fragment, or unnatural marketplace expression requires complete-page regeneration or AI editing followed by a new transcription pass.

Use:

- `6 шт.` for quantity;
- `50 × 70 см` for dimensions;
- `350 мл`, `2 л`, `670 г`, `1,5 кг` for metric values;
- decimal comma, multiplication sign `×`, and a space between number and unit;
- concise noun phrases and natural benefit statements rather than literal Chinese calques;
- sentence case for body copy and restrained uppercase for short headlines only.

Avoid:

- unnatural keyword piles;
- unsupported superlatives such as `лучший`, `№ 1`, or `премиальный`;
- vague promises such as `идеальный для всех`;
- unverified `официальный`, `японские технологии`, `100%`, `гарантия`, or origin claims;
- prices, discounts, coupon language, urgency, ratings, review counts, contact details, URLs, QR codes, social handles, and calls to action;
- Russian-looking transliterations when a normal Russian marketplace term exists.

Proofread case agreement, singular/plural, adjective/noun agreement, unit abbreviations, punctuation, and line breaks. Keep a headline under roughly 35 characters where possible and a benefit under roughly 55 characters.

## Product and brand truth

- Use the supplied logo file as-is; do not redraw, simplify, translate, or invent a logo.
- If brand information is absent, keep the design unbranded.
- Preserve product packaging and physical labels exactly, even when they are not Russian.
- Keep color, finish, part count, fasteners, controls, seams, outsole, accessories, and proportions invariant across all slides.
- Do not show an accessory, battery, gift, box, attachment, food, or consumable as included unless package contents confirm it.

## Ozon rule checkpoint

Official image requirements can change. Before finalizing a set, open the current Ozon Seller category rules and the official image-requirements page:

`https://docs.ozon.ru/global/products/upload/adding-content/image-requirements/`

Treat the following as conservative production defaults, not a substitute for runtime verification:

- 3:4 portrait canvas at 1200 × 1600 px;
- RGB/sRGB PNG output and file size at or below 10 MB;
- product clearly visible and not misleadingly scaled;
- no price, discount, delivery promise, marketplace UI, contact information, rating, review count, or promotional CTA;
- no third-party trademark, certification, flag, medal, or official-store claim without evidence and current permission;
- main-image text only when the current category rule permits it; otherwise use a clean hero and move copy to a later slide.

Record the official URL checked, check date, category, and any category-specific decision in the manifest or QA notes.

If the official page remains unreachable after one retry, do not claim it was verified. Record `platform_check.status` as `conservative-fallback`, include the retrieval error, apply every conservative default above, and flag an upload-time recheck as mandatory. Use a text-free hero only when available evidence indicates that the category requires it; otherwise limit hero copy to the sourced product/category name and decision facts, without promotions, marketplace UI, badges, or unsupported claims. Use `verified` only when the official rule text was actually available.
