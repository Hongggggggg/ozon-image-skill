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

Prompt the user for any product information they have and any fields they explicitly do not want shown. Explain that confirmed, decision-relevant, non-excluded information may appear in the images, title, or description. Useful inputs include exact product name, category, variant/color, material, quantity, package contents, dimensions, source images, sourced selling points, intended audience, and truthful use context. This is an optional intake prompt, not a mandatory form. A user statement is an acceptable source record; visual inference is not.

Continue with the evidence available and omit low-value or unsupported information. Request a missing fact or source view only when it is needed to create a user-selected page or to depict the exact product truthfully. Follow [image-selection.md](image-selection.md) for selection and intake rules.

If only one product image is supplied:

- preserve its visible angle;
- do not create rear, underside, inside, exploded, open/closed, or worn variants not shown;
- allow simpler background changes, scale-preserving placement, close crops of visible details, and text layouts;
- request more images when a required slide cannot be truthful.

## Footwear adapter

Request the following when relevant to a selected page or listing claim:

- pair count and exact colorway/model;
- at least a clear lateral or three-quarter view;
- user-supplied size system and size chart or foot-length mapping;
- construction/material claims supplied by the user;
- sole/outsole/tread photos before showing or describing them;
- on-foot source material before generating an on-foot scene that must preserve exact fit and silhouette.

Do not convert CN/EU/RU sizes from memory. Do not infer waterproofing, warmth, arch support, orthopedic value, slip resistance, natural leather, or season rating from appearance. If a chart is absent, pause the dimension/size page rather than the whole workflow.

## Product-specific ten-slide policy

Require slide 1 to be a current-rule-compliant hero. Accept up to eight user-selected image types as mandatory plan items and automatically select enough additional types to reach ten, leaving at least two automatic choices. Do not impose a universal sequence on slides 2–10. Rank the buyer questions that can be answered from supplied evidence, then give each page one distinct decision job.

Possible pages include exact-product overview, size/fit, dimensions, construction, feature proof, materials, real details, alternate angles, usage, context, care, package contents, configuration, compatibility, supplied brand story, and sourced comparison. None is mandatory merely because it is common in marketplace templates.

Give every page a unique purpose, buyer question, primary fact set, and selection reason. The hero may summarize several priority facts, but slides 2–10 must each introduce different primary information. Merge pages that use the same evidence or answer the same question. A new angle, crop, background, headline, or composition is not a new information job. In particular, do not create separate material and detail pages when both repeat the same surface, seam, control, or outsole close-ups.

Cover every priority fact at least once. Repeat a fact only when the hero summarizes it and a later page provides deeper proof. If the product lacks ten truthful and useful questions, request evidence only for an impossible user-selected page; for automatic slots, use distinct supported exact-product views or other decision-relevant facts. Never add unsupported decorative scenes or duplicate details only to fill the set.

## Russian localization

All added shopper-facing text must be Russian except an evidence-backed brand or public model that passes `excluded_visible_fields`, plus legally printed packaging text that the user has not asked to exclude from the image scope. Apply every field and exact-value exclusion to its recorded scope even when the value is visible in source data.

Write for Russian Ozon shoppers: lead with the product and the fact that helps them choose, use natural Russian ecommerce phrasing, and keep the tone concise, factual, and confident. Do not carry Chinese sentence order, slogan density, seller-backend labels, or literal calques into the title, description, or image copy. Follow the full reading-habit gate in [listing-copy.md](listing-copy.md).

Localize claim strength, not just vocabulary. Do not translate Chinese ecommerce slang such as cloud-walking, cotton-like footfeel, “踩屎感,” or “全天不累” literally into Russian. When adequate tests or authorized marketing evidence are absent, omit the phrase or reduce it to a neutral `supported-benefit` that the visible/material evidence actually supports. Never let a catchy Chinese example become evidence for the product.

Use a two-pass localization gate:

1. **Pre-generation editorial pass:** approve the exact ten-page copy deck before prompting. Run the visible-string role gate on headlines and every auxiliary string, then check Russian marketplace reading habits, natural usage, grammar and agreement, ecommerce clarity, fact alignment, claim safety, and shopper-headline quality. Freeze only approved strings. A grammatically correct string still fails when it exposes internal status, seller/backend terminology, production navigation, a removable generic eyebrow, a camera angle, section name, or bare attribute.
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
- unsupported experiential or performance claims such as `эффект хождения по облаку`, `максимальный комфорт`, `ноги не устают весь день`, heat-retention, rebound, cushioning, or slip-resistance promises;
- unverified `официальный`, `японские технологии`, `100%`, `гарантия`, or origin claims;
- prices, discounts, coupon language, or urgency unless the user supplied current exact terms and the verified current category/page rule explicitly permits the Level 4 offer; always exclude them under conservative fallback, and continue to exclude ratings, review counts, contact details, URLs, QR codes, social handles, and calls to action;
- Russian-looking transliterations when a normal Russian marketplace term exists.
- internal production labels such as `ВИД СБОКУ`, `ДЕТАЛИ`, `КРУПНЫЙ ПЛАН`, `МАТЕРИАЛЫ`, or `ХАРАКТЕРИСТИКИ` as shopper titles;
- isolated attributes such as `КРУГЛЫЙ НОСОК`, `ОВЕЧЬЯ КОЖА`, or `ШЕРСТЬ` as the complete page headline when a fuller sourced decision statement is available.

Proofread case agreement, singular/plural, adjective/noun agreement, unit abbreviations, punctuation, and line breaks. Keep a headline under roughly 35 characters where possible and a benefit under roughly 55 characters.

## Product and brand truth

- Use the supplied logo file as-is; do not redraw, simplify, translate, or invent a logo.
- Include a brand only when explicit trustworthy evidence establishes it and the user has not excluded it. If brand is absent, conflicting, unconfirmed, or user-excluded, keep all added consumer content unbranded; never substitute a store/seller name or placeholder.
- Preserve product packaging and physical labels exactly, even when they are not Russian.
- When `excluded_visible_fields` forbids a brand, model, SKU, internal number, or exact value in images, do not add or deliberately feature it. Use a truthful source view/crop where the excluded content is not visible; if an unavoidable physical label conflicts with the exclusion, pause for user direction rather than redrawing the label or silently violating the exclusion.
- Keep color, finish, part count, fasteners, controls, seams, outsole, accessories, and proportions invariant across all slides.
- For multi-color products, lock one confirmed primary colorway and at most one confirmed secondary colorway. Do not rotate colors by page, and do not convert a photographed appearance into an unsourced catalog color name.
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

If the official page remains unreachable after one retry, do not claim it was verified. Record `platform_check.status` as `conservative-fallback`, include the retrieval error, apply every conservative default above, use a text-free hero, leave unavailable field limits as unknown, and flag an upload-time Seller-cabinet recheck as mandatory. Use `verified` only when the official rule text was actually available.
