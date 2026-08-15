# Ozon image selection and optional intake

## Optional information prompt

Tell the user they may provide any useful product information and that confirmed, decision-relevant information may appear in the listing images, title, or description. Do not present the list as mandatory and do not block merely because fields are absent.

Prompt concisely for any of the following that the user has:

- exact product name, category, brand, model, SKU, color, and sales variant;
- confirmed core selling points and what makes the product different;
- intended audience and truthful use contexts;
- exact parameters written as value, unit, measured quantity, and source;
- material, construction, compatibility, care, quantity, and package contents;
- sharp product, detail, packaging, accessory, underside, interior, or in-use photos;
- existing reusable size-chart, after-sales, packaging, care, or other generic listing assets, plus whether the user wants any of them rebuilt;
- brand assets, desired mood, visual references, and content that must not appear.

Explain the consequence: useful confirmed information can be visualized or written; absent or low-value information will be omitted; unsupported claims will not be inferred.

When the user communicates in Chinese, use a concise prompt such as:

> 你可以提供产品名称、核心卖点、适用人群、期望场景、具体参数、材质结构、包装清单、品牌资料和产品照片。我们会先判断哪些信息真正有助于购买决策；被采用且能够确认的信息会出现在商品图、标题或描述中，无关、重复或缺少依据的内容不会强行展示。

## Information value filter

Prefer information that resolves a purchase uncertainty: exact identity, variant, differentiating construction, material, fit, dimensions, capacity, compatibility, quantity, package contents, setup, care, limitation, or a supported use case.

Usually omit internal codes that do not identify the shopper's variant, exhaustive low-impact specifications, repeated synonyms, generic praise, irrelevant company history, decorative facts, unsupported effects, and information already communicated more clearly on another page.

Treat user-supplied “selling points” as candidate claims. Include them only when they are specific, relevant, internally consistent, and supported by a user statement or stronger evidence. Do not place every supplied fact into the artwork.

## Reusable asset exclusion

Before accepting image types or filling automatic slots, inventory reusable assets the user already has. For each asset record `asset_id`, `type`, source/path, reusable scope, and `rebuild_requested`.

- When `rebuild_requested` is false, add the covered type to `excluded_from_generation`, do not regenerate it, and do not count it among the ten new pages.
- Preserve the user's intent by listing the reusable asset separately in delivery, then fill the released generation slot with a product-specific buyer question.
- Generate the covered type only when the user explicitly asks to rebuild or replace the reusable asset.
- Do not assume an old asset is reusable merely because its type is common; confirm that the user identifies it as reusable and that it matches the current listing context.

## Text image-type menu

Let the user name or select up to eight types in ordinary text. Normalize synonyms to these types:

1. `hero` — first-screen product identity and strongest supported value;
2. `core-benefit` — a decisive supported difference;
3. `usage-scene` — truthful placement, scale, handling, or use;
4. `multi-angle` — source-supported exterior views or structure;
5. `atmosphere` — category-relevant mood without replacing product proof;
6. `detail` — material, construction, controls, seams, finish, or craftsmanship visible in sources;
7. `brand-story` — supplied, relevant, verifiable brand information;
8. `size-capacity-size-chart` — sourced dimensions, capacity, fit, or size mapping;
9. `comparison` — sourced factual comparison without fabricated before/after results;
10. `specification` — decision-relevant product data;
11. `process` — sourced manufacturing or setup process;
12. `package-accessories` — confirmed package contents, accessories, or gifts;
13. `series` — confirmed colors, variants, or SKUs;
14. `composition` — sourced ingredients, layers, materials, or component structure;
15. `after-sales` — documented warranty, return, or service information currently allowed on Ozon;
16. `usage-advice` — evidence-based setup, care, or cautions.

Do not expose internal enum names unless useful; show natural user-language labels.

For a Chinese text selection, present the natural labels without requiring a UI checkbox:

> 可从以下类型中选择最多 8 种，直接回复名称即可：首屏主视觉、核心卖点图、使用场景图、多角度图、场景氛围图、商品细节图、品牌故事图、尺寸/容量/尺码图、效果对比图、详细规格/参数图、工艺制作图、配件/赠品图、系列展示图、商品成分/结构图、售后保障图、使用建议图。你选择的类型会优先处理；如果你已经有通用尺码图、售后图、包装图等可复用资产，它们会单独保留而不占 10 张新图名额，除非你要求重做。其余位置由我们根据商品资料和购买决策价值补足，始终至少保留 2 张自动选择。

## Selection policy

Always plan ten newly generated product-specific consumer-facing pages. Accept at most eight user-selected types. User selections have the highest priority and must appear in the plan, but they do not authorize invented evidence, prohibited claims, or regeneration of an excluded reusable asset.

- Zero selected: choose all ten from evidence and buyer questions.
- One to seven selected: keep the types still requiring generation and automatically fill the remaining slots; satisfy excluded types with their reusable assets.
- Eight selected: keep the types still requiring generation and automatically fill to ten; when none is excluded, this means two automatic pages.
- More than eight selected: ask the user to reduce the list to eight before generation.
- After reusable-asset exclusions, compute `automatic_count = 10 - count(user-selected types still requiring generation)`. An excluded type is satisfied by the reusable asset but its new-generation slot is replaced.

If two selected types overlap, keep both only by assigning different buyer questions and evidence. For example, a scene may prove scale while an atmosphere page communicates placement context. If meaningful separation is impossible, explain the overlap and ask the user which interpretation matters; do not silently discard a selected type.

If a selected type lacks enough evidence, state exactly what information or source view would make it possible and explain that the information can then appear in that page. Use a conservative truthful version of the same type when possible. If the type cannot be produced truthfully at all, pause that page rather than replacing it silently.

## Dynamic automatic priority

Use this baseline, then adapt it to category and buyer uncertainty:

1. First: hero, core benefit, decision-critical size/specification, source-visible detail, and structure/multi-angle.
2. Next: usage scene, package contents, compatibility, configuration, care, or usage advice when relevant.
3. Conditional: atmosphere, composition, accessories/gifts, series, after-sales, brand story, process, or comparison.

The baseline is not absolute. Package contents can outrank a scene for a bundle; compatibility can be essential for electronics accessories; size can be essential for footwear; accessories remain low priority when they do not change the buying decision.

Choose automatic pages by scoring: purchase-decision value, evidence strength, category relevance, visual distinctness, and non-duplication. Record the reason for every choice.

Never use an automatic slot for a size chart, after-sales card, packaging card, care card, or other type already covered by `excluded_from_generation`.

## Colorway selection

For products with multiple visible or supplied colors, separate visual observation from confirmed catalog identity. A photo may support visible appearance but does not establish a backend color name.

1. Select one confirmed `primary_colorway` for set identity. If the catalog name is unavailable, reference the exact source image/variant without inventing a color name.
2. Select at most one confirmed `secondary_colorway` and list the exact pages where it may appear plus the purchase-decision rationale.
3. Keep the primary colorway dominant across identity-sensitive pages. Do not rotate colors mechanically, assign one color per page, or alternate colors merely for variety.
4. Add a `series` or colors page only when the available color choices are confirmed and color selection is itself an important buyer question.

## Ten-page visual system

Before generation, define one shared visual system: exact product identity, primary and optional secondary colorway, palette, typography, lighting, contrast, graphic language, Russian tone, margins, safe zones, product scale range, information hierarchy, reusable component grammar, layout archetypes, and visual rhythm. Keep these consistent across all ten pages.

Vary composition, crop, scene intensity, and information density so the set does not look like one template with replaced text. Give every page one dominant decision message and ensure the product remains recognizable at mobile thumbnail size.
