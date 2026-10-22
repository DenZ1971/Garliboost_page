# GARLIBOOST: направление существенного redesign

## Status

**Статус:** research-backed draft. Документ задаёт направление, но не является разрешением на изменение production-кода.

До реализации нужно подтвердить:

1. допустимо ли менять порядок основных секций;
2. является ли `https://formspree.io/f/mvkggory` рабочим и одобренным endpoint формы;
3. можно ли использовать текущую фотографию пастбища как основной брендовый образ и есть ли актуальный packshot упаковки;
4. разрешены ли новые тексты FAQ/возражений и сокращение повторяющихся фрагментов после отдельного контентного и юридического согласования;
5. какая локаль и домен идут следующими после RU.

## Confirmed Facts

- GARLIBOOST представлен как дополнительный корм на основе жидкого чесночного аллицина для КРС, телят, свиней, коз и овец.
- Основной публичный маршрут сейчас один: `site/ru/index.html`; опубликована только локаль `ru`.
- Сайт статический: semantic HTML, CSS, vanilla JavaScript, нативные MP4 и WebVTT. Framework и build pipeline не используются.
- Production-источник: `production-src/template/page.html`, `production-src/locales/ru.json`, `production-src/assets/`; публикация генерируется в `site/`.
- Текущая визуальная база: тёплый cream background, тёмный agricultural green, brick/red accent, Georgia + Arial, тонкие правила, крупная farm photography.
- Основная конверсия по интерфейсу: заявка «Обсудить задачу фермы» с квалифицирующими полями о хозяйстве, животных и задаче.
- Содержательные опоры: объяснение продукта, ситуации в хозяйстве, разграничение питания и лечения, точная схема применения, calculator, два видео о мастите, одно видео о телятах, клинический протокол и другие PDF.
- Дозировка и calculator уже реализованы и не должны меняться без отдельного подтверждения бизнес-правил.
- Текущие videos имеют русские WebVTT subtitles и ручной toggle; JavaScript останавливает другие видео при старте одного.
- В коде есть skip link, semantic landmarks, keyboard tabs, focus styles, live form status и mobile menu с Escape/focus handling.
- Существующие проверки фиксируют отсутствие horizontal overflow на 1440, 1280, 768 и 390 px, работу calculator, tabs, form validation и videos. Это не заменяет новый accessibility audit после redesign.
- Общий вес production assets около 50 MB: около 45 MB video, 3.5 MB images и 1.1 MB documents. Самый большой MP4 около 25.4 MB; hero JPEG около 3.57 MB.
- README говорит, что RU form недоступна до выбора провайдера, но template содержит Formspree endpoint и JavaScript выполняет `fetch` при submit. Фактический статус endpoint не подтверждён.
- `domain` равен `null`; canonical/hreflang, root redirect, sitemap и robots пока не определены.

## Assumptions and Open Questions

### Неблокирующие assumptions

- Primary audience: владельцы и управляющие хозяйств, herd managers, ветеринарные специалисты и B2B distributors.
- Решение принимается не импульсивно: пользователь сначала проверяет применимость, дозировку, уровень доказательности и возможность поставки.
- Desktop чаще используется для изучения документов и принятия решения; mobile — для первого знакомства, просмотра видео и быстрого обращения.
- Redesign должен эволюционировать существующую аграрно-редакционную идентичность, а не превращать сайт в новый бренд.
- Текущие утверждения, legal wording, evidence distinctions и dosage считаются защищённым content baseline.

### Вопросы перед production implementation

- Кто принимает заявку, где хранятся персональные данные, какая privacy notice обязательна и нужна ли consent checkbox?
- Должна ли заявка быть единственной конверсией, или нужен дополнительный канал: телефон, email, distributor inquiry или request a callback?
- Есть ли подтверждённые distributor geography, delivery terms и языковая очередность?
- Есть ли оригинальные горизонтальные фото продукта, фермы и животных с правами на коммерческое использование?
- Можно ли удалить/объединить повторы только после content review, не меняя клинический смысл?
- Нужны ли отдельные routes для продукта, evidence и контактов, или long-form landing остаётся единственной страницей?

## Business

### Offer

Дополнительный корм в жидкой форме для профессионального животноводства. Ценность интерфейса не в обещании результата, а в ясном ответе на четыре вопроса: что это, для каких животных, как точно применять и на каких типах данных основаны утверждения.

### Audience

1. **Владелец/управляющий фермы:** оценивает практичность, экономический контекст, простоту внедрения и доверие к поставщику.
2. **Ветеринар/зоотехник:** проверяет границу между кормовой поддержкой и лечением, дозировку, состав, протоколы и ограничения выводов.
3. **Дистрибьютор/закупщик:** проверяет категорию продукта, упаковку, производителя, документы, географию и контакт.

### Website Goal

Превратить первое сомнение в квалифицированный разговор, не преувеличивая доказательность и не заставляя пользователя собирать цельную картину из разрозненных карточек.

### Primary Conversion

`Обсудить задачу фермы` → заполненная квалифицированная форма. Primary CTA повторяется после hero, после dosage/calculator и после evidence summary. Повторы ведут к одной форме и получают контекстный accessible name, но не создают разные конкурирующие действия.

Secondary actions:

- изучить применение и calculator;
- посмотреть source-specific evidence;
- открыть PDF;
- посмотреть farm videos с subtitles.

### Constraints

- Не менять clinical, veterinary, legal и marketing claims без отдельного согласования.
- Не менять dosage, calculator math и виды животных.
- Не смешивать manufacturer data, clinical observations и individual farm experience.
- Сохранить static HTML/CSS/JS и locale-driven template.
- Не добавлять framework, dependency-heavy slider, animation library или third-party tracker как часть visual redesign.
- Цель accessibility: WCAG 2.2 AA.

## Existing Product Review

Ниже — review текущего интерфейса. «Observed» означает подтверждение кодом/скриншотом; «Unverified» — риск, требующий проверки.

### Critical

| ID | Location | Problem | Why it matters | Recommended change | Expected effect | Evidence |
|---|---|---|---|---|---|---|
| GB-C01 | Form / README / privacy | README утверждает, что form endpoint отсутствует, но template отправляет персональные данные в Formspree. Неясны production status и privacy basis. | Это может затронуть consent, data handling и доверие; визуальный redesign не должен маскировать неопределённый workflow. | До implementation подтвердить endpoint, recipient, retention, privacy text и error/recovery flow. Если endpoint не одобрен, form должна быть явно disabled или заменена согласованным каналом. | Устраняет юридический и операционный blocker конверсии. | Observed: `page.html` + `farm.js` противоречат `production-src/README.md`; состояние Formspree unverified. |

### Major

| ID | Location | Problem | Why it matters | Recommended change | Expected effect | Evidence |
|---|---|---|---|---|---|---|
| GB-M01 | Whole-page conversion flow | На mobile primary form находится после очень длинного linear journey; после hero нет устойчивой серии context CTAs. | Пользователь, уже убедившийся после dosage или evidence, вынужден продолжать длинный scroll. | Ввести три одинаковых conversion checkpoints: hero, calculator/evidence transition, final consultation section. Не использовать постоянную sticky кнопку, пока она не проверена на перекрытие контента. | Более короткий путь к заявке без агрессивного sales-поведения. | Observed: одна form near footer; full mobile capture около 12.5k px. |
| GB-M02 | Situations, farm experience, clinical observations, evidence | Иерархия типов доказательств существует в тексте, но визуально распределена между small labels, cards, videos и отдельным evidence list. | Быстрое сканирование может смешать manufacturer statement, protocol observation и testimonial. | Сделать source taxonomy частью системы: обязательный label, source, scope, limitation и link для каждого evidence block; собрать их в единый Evidence Hub. | Повышает доверие и снижает риск неверной интерпретации. | Observed: соответствующие labels есть, но используют близкий размер/цвет и разнесены по секциям. |
| GB-M03 | Hero | Hero сильно выражает проблему фермы, но слабее идентифицирует сам продукт: packshot отсутствует, category line и 500 ml note вторичны. | B2B-пользователь должен за первый viewport понять, что предлагается и какое действие ожидается. | Сохранить farm photograph и problem-led headline, но добавить компактный product identity block: категория, животные, форма применения и primary CTA. Использовать packshot только после подтверждения актуальности. | Быстрее формирует корректную mental model без превращения hero в ecommerce. | Observed: hero photo + headline dominate; product explanation ниже и текстом. |
| GB-M04 | Mobile long-form rhythm | Mobile page превращает почти каждую desktop composition в последовательный stack с близкой плотностью; визуальные reset moments редки. | Длинное чтение становится монотонным, distinctions между explanation, proof и action ослабевают. | Проектировать mobile как отдельный editorial sequence: короткие section intros, source bands, one-column evidence index, media resets и optional disclosure для supporting detail. | Улучшает ориентацию и уменьшает cognitive fatigue. | Observed: 390 px capture; repeated heading/text/rule/card stacks. |
| GB-M05 | CSS architecture / responsive behavior | `farm.css` содержит последовательные исторические override passes и много повторных `@media(max-width:600px)`. | Redesign поверх каскада увеличит риск regressions и затруднит token consistency. | При implementation собрать новый semantic token layer и component sections в одном mobile-first stylesheet; не переписывать unrelated generator logic. | Более предсказуемая responsive system и меньший regression surface. | Observed: 30.5 KB stylesheet, multiple later overrides for same selectors/breakpoint. |

### Minor

| ID | Location | Problem | Why it matters | Recommended change | Expected effect | Evidence |
|---|---|---|---|---|---|---|
| GB-m01 | Source labels / footnotes | Source and limitation copy часто 11–14 px и визуально близко к metadata. | Это содержательно важная информация, а не декоративный caption. | Minimum 14 px mobile / 15 px desktop, 1.5 line-height; key limitation stays adjacent to claim. | Лучше читаемость и compliance comprehension. | Observed in CSS and screenshots. |
| GB-m02 | Controls and borders | Общий line token `#d5d5c7` на `#fcfaf3` имеет низкий контраст (~1.42:1); он подходит для decorative rules, но не для обязательной границы control/focus state. | Interactive affordance не должна зависеть от слабой hairline. | Разделить `border.decorative` и `border.control`; control border/state должны пройти 3:1 non-text contrast. | Более ясные fields, tabs и disclosure controls. | Measured token pair; не утверждается, что каждый текущий control нарушает WCAG. |
| GB-m03 | Locale architecture / JS | Несколько сообщений menu и calculator hardcoded на русском в `farm.js`. | Следующая локаль потребует обхода JSON architecture или дублирования JS. | Перед multi-locale rollout передавать UI messages через data attributes/locale payload. | Сохраняет единый template и уменьшает translation drift. | Observed in `farm.js`. |

### Enhancement

| ID | Location | Problem | Why it matters | Recommended change | Expected effect | Evidence |
|---|---|---|---|---|---|---|
| GB-E01 | Navigation | Long page имеет anchor navigation, но не показывает текущий смысловой этап. | На desktop/tablet пользователю полезна ориентация внутри длинного документа. | Добавить restrained sticky section index после hero или active nav state; отключать/упрощать на mobile. | Быстрее возврат к dosage, evidence и contact. | Opportunity inferred from page length. |
| GB-E02 | Evidence documents | PDF links находятся в конце evidence flow и выглядят как обычные text links. | Профессиональная аудитория оценивает provenance и document metadata. | Использовать document rows с типом, датой, языком, форматом/размером и external-file behavior. | Документы становятся проверяемым ресурсом, а не footer appendix. | Existing PDFs and links confirmed. |

## Existing Product

### Preserve

- cream/green/brick palette and restrained editorial tone;
- problem-led farm context and landscape photography;
- serif display + sans functional pairing;
- explicit source distinctions and limitations;
- dosage calculator behavior, animals tabs, videos, subtitles, PDFs and consultation fields;
- semantic static architecture, generator and locale separation;
- straight edges, small radius, hairline rules and minimal shadows.

### Evolve

- hero from «problem poster» to «problem + identifiable offer + action»;
- sections from repeated two-column/card patterns to a deliberate photographic/document rhythm;
- evidence from scattered fragments to a navigable taxonomy;
- CTA hierarchy from start/end to contextual checkpoints;
- responsive implementation from accumulated overrides to mobile-first component rules;
- typography from browser-default Georgia/Arial toward a controlled, self-hosted editorial pair if approved.

### Replace

- duplicated visual patterns that make unlike evidence types look equivalent;
- tiny evidence metadata and weak control borders;
- generic equal-weight metric/card rows where one fact is primary;
- production styles that depend on repeated late overrides;
- any unverified form state or consent wording.

## Reference Research

Research performed through Inspo MCP on 2026-09-20. Initial `recommend` selected **Photographic**; focused searches covered **Long Document** and mobile photographic behavior. Four references from different sites were retained and compared.

### Search Brief

Professional European agricultural B2B; farm owners, herd managers, veterinarians and distributors; consultation rather than ecommerce; precise dosage; explicit separation of manufacturer data, clinical observations and farm experience; calm, evidence-led, premium but restrained; warm editorial agriculture; strong desktop and mobile long-form reading.

### Retained References

| Reference | Role in GARLIBOOST | What not to copy |
|---|---|---|
| [Stanford](https://stanford.edu), `stanford-edu` | Institutional authority through one place-defining photograph, restrained accent, serif/sans contrast and clear bottom-of-hero action. | Centered university wordmark, Stanford red, campus composition and exact hero sequence. |
| [BBC Earth](https://bbcearth.com), `bbcearth-com` | Mobile hero that keeps logo, headline, subject and CTA within the first viewport; visual-first documentary confidence. | Media catalogue rails, lime CTA, oversized campaign numeral and entertainment framing. |
| [Effective Altruism FAQ](https://effectivealtruism.org), `effectivealtruism-org--faqs` | Warm off-white long-document clarity, ruled disclosure rows, objection handling and large type with little ornament. | Exact FAQ composition, geometric sans identity and unrelated conversion model. |
| [Craig Mod](https://craigmod.com), `craigmod-com` | Quiet editorial materiality, warm image-led mobile rhythm, restrained serif/sans pairing and proof attached directly to the object. | Awards/laurel motif, book-cover composition and personal-portfolio navigation. |

### Cross-reference Findings

- Shared register: light, editorial, minimal, calm and serious.
- Three references use photographic macrostructure; one supplies long-document logic. GARLIBOOST needs both, not a pure version of either.
- Authority comes from one dominant image, high type contrast, generous seams and low accent frequency—not from many cards or effects.
- Long content remains legible when hairlines, metadata and spacing express hierarchy; decoration is unnecessary.
- Mobile succeeds when the hero is complete, navigation is compact and the next content block appears immediately after the first action.
- Inspo component search produced useful hero/CTA patterns but no suitable long-document stat component. GARLIBOOST metrics therefore need a project-specific evidence table rather than a borrowed dashboard pattern.

### Patterns Deliberately Avoided

- pure cinematic hero with no product category or CTA;
- medical-tech white/blue dashboard;
- SaaS bento cards, pills everywhere, gradients and glowing metrics;
- rustic/organic craft branding, garlic illustrations or wellness language;
- ecommerce packshot-first hero and price-oriented CTA;
- oversized proof numbers without source, scope and limitation;
- autoplay video, carousel, parallax and decorative scroll choreography;
- copying any reference's section order, palette, identity, assets or JSX.

## Macrostructure

### Selected Structure

**Photographic entry + editorial evidence document + consultation close.**

Hero creates recognition and stakes. The middle behaves like a well-edited dossier: what the product is, where it fits, how it is used and what each evidence source can support. The end converts with a qualified, low-pressure consultation.

### Page and Section Flow

1. **Compact header** — logo, Product, Application, Evidence, Farm experience, Contacts, language, primary CTA on wide desktop; accessible menu below 1050 px.
2. **Photographic hero** — current problem-led H1; concise category/product identity; primary CTA; secondary link to application; farm photograph; optional verified packshot inset.
3. **Decision strip** — three immediate facts: product category, supported animals, liquid application/500 ml. This replaces generic benefit cards above the fold.
4. **What GARLIBOOST is / is not** — formula, controlled application, and explicit boundary with veterinary diagnosis/treatment.
5. **Farm situations** — four use contexts, each visibly labelled by source type; no equal-looking unsupported claims.
6. **Application workspace** — animal tabs, fixed dosage explanation, calculator and storage note. A contextual consultation CTA follows the result, not inside the calculator.
7. **Evidence Hub** — source taxonomy first, then protocol metrics, limitations and document index. Primary evidence precedes anecdotal material.
8. **Farm experience** — two mastitis videos and one calf video as documentary stories with context, subtitles and explicit scope.
9. **Questions and boundaries** — concise disclosures for «это лекарство?», «как считать дозу?», «что означают наблюдения?», «можно ли совмещать с назначенным лечением?». Copy requires veterinary/legal approval.
10. **Consultation** — short reassurance, qualification form, contact/fallback channel, privacy and response expectation.
11. **Footer** — distributor, product owner, category/registration wording, document/legal links and locale status.

Changing the current section order, especially placing Evidence before Farm experience, requires explicit user approval before implementation.

### Rationale

- Farm owners first need relevance, then practical application, then proof and contact.
- Veterinary users need source hierarchy and limitations before testimonials.
- The calculator acts as the highest-intent interactive moment and deserves a nearby conversion checkpoint.
- Alternating photo, text, workspace, evidence matrix and video prevents a 12k-pixel mobile stack from becoming visually uniform.
- Proof is not delayed to the footer, but conversion also does not interrupt every section.

### Alternatives Considered

1. **Pure Photographic:** rejected because long technical/legal content would become secondary and hard to compare.
2. **Pure Long Document:** rejected because the product would lose agricultural place, emotional relevance and existing brand character.
3. **Split Studio:** rejected because repeated left-copy/right-media splits already contribute to monotony and feel like an agency/product showcase.
4. **Stat-led dashboard:** rejected because available observations do not justify a clinical dashboard metaphor and could overstate evidence.

## Original Design Direction

### Design Thesis

**«Полевой досье»: реальная ферма с редакционной точностью.**

The site should feel like a calm, well-prepared document brought to a farm meeting: grounded in place, easy to scan, precise about sources, practical about application and restrained in claims. Photography carries context; typography and rules carry evidence; brick accent marks action and provenance.

### Visual Character

- Warm, low-chroma, materially agricultural—not rustic.
- Large landscape moments appear only at narrative resets: hero and one mid-page evidence/farm transition.
- Content sections use asymmetric editorial grids, not repeated equal cards.
- Source labels behave like document metadata, not marketing eyebrows.
- Numbers are tabular and always paired with scope/source.
- Most surfaces stay flat; depth comes from tonal paper layers and hairlines.
- Radius language is sharp to 4 px; pills are reserved for tabs/status choices.
- Motion is functional, short and optional.

### Differentiation from References

- Stanford informs authority, but GARLIBOOST keeps left-aligned problem/product content and an agricultural—not institutional—voice.
- BBC Earth informs first-viewport discipline, but GARLIBOOST uses a still responsive image and no entertainment rail.
- Effective Altruism informs disclosure rhythm, but GARLIBOOST uses serif editorial headings and formal evidence metadata.
- Craig Mod informs warmth/materiality, but GARLIBOOST attaches proof to claims rather than awards to a product object.

## Design System

### Color

Preserve current values where compatible and formalize semantic roles:

| Token | Value | Role |
|---|---:|---|
| `color.surface.canvas` | `#FCFAF3` | Main cream background |
| `color.surface.subtle` | `#EFEEE3` | Calculator, documents, restrained supporting panels |
| `color.surface.field` | `#F7F4EA` | Form/control differentiation |
| `color.ink.primary` | `#353C26` | Main text; measured ~11.01:1 on canvas |
| `color.ink.secondary` | `#626953` | Supporting text; measured ~5.49:1 on canvas |
| `color.brand.forest` | `#102E28` | Strong bands, footer, photo overlays |
| `color.action.primary` | `#AD4226` | Primary CTA and source/action emphasis; white text measured ~5.86:1 |
| `color.action.hover` | `#8F321D` | Hover/pressed family; final value must be verified |
| `color.border.decorative` | `#D5D5C7` | Nonessential rules only |
| `color.border.control` | TBD darker olive/green | Inputs, tabs, disclosure boundaries; must reach 3:1 where required |
| `color.state.error` | TBD | Error text/icon; 4.5:1 and not color-only |
| `color.focus` | `#AD4226` or verified darker variant | 2 px minimum visible ring |

No gradients except a single functional photo scrim. No dark mode in redesign scope.

### Typography

- Proposed self-hosted pair: **Source Serif 4** for display/editorial headings and **Source Sans 3** for body/UI, with `Georgia` and `Arial` fallbacks. This evolves the current serif/sans logic and should be approved/licensed before implementation.
- If no new font assets are approved, retain Georgia/Arial and implement the same scale/rhythm.
- Display: `clamp(2.75rem, 5.8vw, 5.75rem)`, 0.98–1.06 line-height, max 12–16 words and no more than three mobile lines where copy allows.
- H2: `clamp(2rem, 3.6vw, 3.75rem)`, line-height 1.06–1.12.
- H3: `clamp(1.35rem, 2vw, 2rem)`, line-height 1.15–1.25.
- Body: 17–18 px desktop, 16–17 px mobile, line-height 1.55–1.65, max 65ch.
- Metadata/source: minimum 14 px mobile, 15 px desktop, line-height 1.5.
- Numbers: tabular figures; never detach a metric from unit, population and source.

### Grid and Containers

- `layout.container.max`: 1280 px.
- `layout.prose.max`: 65ch.
- Desktop ≥1200: 12 columns, 24 px gutters, 48–64 px side padding.
- Tablet 768–1199: 8 columns, 24 px gutters, 28–32 px side padding.
- Mobile 320–767: 4 columns, 16 px side padding at 320, 20–24 px from 390 upward.
- Full-bleed belongs to media/background only; text stays in padded container.
- Evidence tables may use controlled horizontal scrolling only when semantic reflow would corrupt comparisons; default is stacked rows.

### Spacing and Sizing

Primitive scale: `4, 8, 12, 16, 24, 32, 48, 64, 80, 112, 144`.

- Section seam: `clamp(64px, 8vw, 112px)`.
- Narrative reset before Evidence and Consultation: up to 144 px desktop.
- Card/panel padding: 20–32 px; never exceed surrounding section seam.
- Interactive target: minimum 44×44 px by project preference; never below WCAG 24×24 px minimum.
- Sticky header: approximately 64–72 px, with `scroll-margin-top` on targets.

### Borders, Radius, and Elevation

- Decorative rules: 1 px subtle.
- Controls: 1 px verified control border plus focus ring.
- Radius: 0, 2, 4 px; pills only for tabs/toggles.
- Shadow: none by default; one restrained elevation for open mobile navigation only.
- Do not use colored left strips as generic card decoration. Source type is conveyed by text label + icon/abbreviation + placement, not color alone.

### Imagery and Iconography

- Hero: authentic wide farm/environment image with a deliberate quiet zone for copy.
- Mid-page imagery: documentary stills, animal/farm details, packaging/process only when rights and current labeling are confirmed.
- Packshot must show the approved current package. The old alternate-label product image is not a safe fallback.
- Responsive sources: AVIF/WebP plus JPEG fallback; explicit width/height and focal-point art direction.
- Icons: minimal inline SVG, 20–24 px, consistent stroke. No emoji, decorative garlic icons or stock medical symbols.
- Video posters must remain honest stills from the underlying content and not imply outcomes not shown.

### Motion

- 120–180 ms for hover/press/focus feedback; 180–240 ms for disclosure/menu.
- No scroll-triggered entrances required for comprehension.
- No autoplay, parallax or auto-advancing carousel.
- Under `prefers-reduced-motion: reduce`, remove travel and smooth scrolling; keep state changes immediate.

### Tokens

Use semantic custom properties, for example:

```text
--color-surface-canvas
--color-surface-subtle
--color-ink-primary
--color-ink-secondary
--color-action-primary
--color-border-decorative
--color-border-control
--font-family-display
--font-family-body
--text-display-size
--text-body-size
--space-section
--space-gutter
--layout-container
--radius-control
--motion-fast
```

Raw values belong only in the token declaration layer.

## Components

### Inventory

| Component | Purpose and content | Responsive behavior | States / accessibility |
|---|---|---|---|
| Header + primary nav | Brand, five anchors, locale, CTA | Full nav only when it fits; menu ≤1050 px | Semantic `nav`; Escape, outside click, focus return; current section via `aria-current` if implemented |
| Photographic hero | Problem, category, offer, CTA, secondary anchor, image | 7/5 or overlay desktop; stacked/overlay mobile with complete first viewport | Contrast scrim; no text embedded in image; reduced-motion irrelevant |
| Decision strip | Three factual qualifiers | 3 columns desktop; vertical ruled list mobile | Plain list, not faux cards |
| Product boundary block | What it is / is not; formula; veterinary boundary | Asymmetric 7/5 desktop; single column mobile | Correct heading order; critical limitation never collapsed |
| Situation index | Four farm contexts and source type | 2×2 editorial grid; stacked index mobile | Entire card not clickable unless one clear destination; descriptive links |
| Animal tabs | Species-specific labels/panels | Scroll-free wrapping or select-like disclosure on narrow widths | Arrow/Home/End keys, roles, selected state, focus visible |
| Dosage calculator | Weight input and three outputs | Split workspace desktop; single column mobile | Visible label/error, `aria-invalid`, live but non-chatty output, decimal locale behavior |
| Evidence taxonomy | Explains Manufacturer / Clinical observation / Farm experience | Three ruled columns → stacked definitions | Text + symbol, never color only |
| Evidence metric row | Scope-limited numbers | 5/6-column row desktop; prioritized stacked rows mobile | Each metric bound to unit/scope/source; semantic list or table |
| Document index | PDF title, type, date, language, size | Full-width rows | File type and new-tab behavior announced; focus visible |
| Video case | Poster/video, case context, observation, limitation, subtitle toggle | Paired editorial layout desktop; one story at a time mobile | Native controls, captions, transcript option target, no autoplay; loading/poster states |
| Disclosure/FAQ | Approved objections and boundaries | Full-width ruled rows | Native `details/summary` where suitable; keyboard operable; no content essential to initial understanding hidden |
| Context CTA band | One sentence + consultation action | Wide band desktop, stacked mobile | Same destination/label logic; no sticky overlap |
| Consultation form | Qualified lead capture | 2 columns desktop; 1 column mobile | Visible labels, autocomplete, errors, pending/success/failure, privacy, retry and fallback channel |
| Footer | Legal/product ownership/contact/doc links | 3 columns → ordered stack | Logical DOM order and descriptive links |

### Variants and States

- Buttons: primary, secondary, text link; default, hover, focus-visible, pressed, disabled, pending.
- Evidence labels: manufacturer data, clinical observation, farm experience, application instruction. Same geometry; distinct text/icon and optional subtle tone.
- Form: empty, valid, invalid, submitting, success, network failure. Success must not remove the only contact context.
- Video: poster, metadata loading, ready, playing, caption on/off, unsupported/error. Provide fallback download or source link where appropriate.
- Document: available, missing/unverified, external. Never render a dead link as available.

### Content Requirements

- Existing approved wording is the baseline; design must not silently rewrite it.
- Every claim block requires provenance, scope and limitation at the point of reading.
- Any new FAQ wording needs veterinary/legal/content approval.
- CTA text must describe consultation, not promise treatment, order availability or guaranteed outcome.
- Product photography and package copy must match the current EU label.

## Responsive Behavior

### Desktop

- Hero complete within roughly 760–900 px viewport height; navigation, H1, category, primary CTA and image are all visible.
- Use asymmetry: hero 7/5, product boundary 7/5, application 5/7, evidence full-width index, video stories alternating 5/7 and 7/5.
- Optional sticky header/section index must not obscure focus or anchor targets.
- Section seams remain generous; long evidence text uses 60–65ch columns.

### Tablet

- Do not preserve desktop split at the cost of narrow prose. Collapse hero/product/evidence based on content, not only breakpoint.
- Header uses compact menu; calculator can remain two columns only if both columns stay at least ~320 px.
- Evidence taxonomy may be 2+1; metric row becomes 2–3 columns with explicit reading order.
- Videos remain side-by-side only if native controls and captions are usable.

### Mobile

- Header, hero headline, category line, primary CTA and image subject appear within the first screen or with only a small visual continuation.
- No horizontal scroll at 320 px; no forced two-column microcards.
- Preserve 16–17 px body text and 14 px source metadata; do not solve length by shrinking type.
- Use a sequence of distinct blocks: hero → decision list → explanation → situations → calculator → evidence → video → FAQ → form.
- Video stays inline with native controls; poster height is limited to avoid one vertical video consuming multiple screens before context.
- Form is single-column; submit remains after privacy note only if the note is short and explicit, otherwise before a linked full notice according to legal decision.

### Content Reordering and Reduction Rules

- DOM reading order equals mobile reading order; CSS must not create semantic reordering.
- The source limitation stays adjacent to its claim at all widths.
- Never hide dosage warnings, clinical scope or legal category on mobile.
- Supporting methodology can use disclosure after a visible summary; core conclusions cannot.
- Do not remove videos or documents solely for mobile. Use lazy loading and compact context.

## Accessibility

Target: **WCAG 2.2 AA**.

- One `h1`; headings follow content hierarchy without skipped levels.
- Landmarks: skip link, header, nav, main, section labels and footer.
- All controls operable by keyboard; menu, tabs, disclosures, calculator and form have logical focus order.
- Visible focus ring at least 2 px and not obscured by sticky elements.
- Text contrast at least 4.5:1; large text 3:1; meaningful controls/icons/focus 3:1.
- Do not rely on brick/green color to distinguish evidence type, selected tab, error or success.
- Body remains readable at 200% zoom; page reflows at 320 CSS px without two-dimensional scrolling.
- Touch targets target 44×44 px; WCAG 2.2 minimum 24×24 px is the floor.
- Images get meaningful alt or empty alt when decorative. Farm photography alt describes the scene, not marketing claims.
- Videos retain synchronized captions; add transcript links before treating media accessibility as complete. Audio description need must be assessed per video.
- Form labels remain visible; errors are text, associated to fields and announced. Status uses a suitable live region without moving focus unexpectedly.
- `prefers-reduced-motion` removes smooth scroll and movement.
- Language remains `ru`; foreign phrases or Hebrew content should use `lang` where exposed as text.
- Verify with keyboard-only, VoiceOver, 200% zoom, text-spacing override, 320 px reflow and high-contrast/forced-colors.

## Performance

### Budgets

- LCP ≤2.5 s, INP ≤200 ms, CLS ≤0.1 at p75 on representative mobile.
- Initial page transfer excluding videos/PDFs: target ≤1.2 MB mobile and ≤1.8 MB desktop.
- Hero image: ≤350 KB mobile, ≤700 KB desktop; provide AVIF/WebP/JPEG sources and preload only the selected LCP candidate.
- CSS + first-party JS: target ≤90 KB gzip combined; JavaScript ≤25 KB gzip.
- Fonts: maximum two families, two initial weights each, WOFF2; initial font transfer target ≤160 KB; `font-display: swap` or `optional` after visual testing.
- Video: poster loads initially; no full video transfer before user intent. `preload="metadata"` must be measured; target ≤150 KB per video before play.
- PDF files excluded from initial load and fetched only on activation.
- Third-party scripts: zero in initial render. Form provider request occurs only after explicit submit.

### Strategy and Measurement

- Generate responsive hero sources at actual display widths; do not ship the current 3.57 MB JPEG unchanged as universal LCP asset.
- Set image/video dimensions to reserve layout and prevent CLS.
- Lazy-load below-fold images/posters where native behavior is sufficient.
- Keep menu, tabs, calculator, subtitles and form in vanilla JS; no animation/carousel dependency.
- Measure production-like build at 390×844, 768×1024 and 1440×900; test cold cache and throttled mobile.
- Record Lighthouse/WebPageTest results and real-user CWV after deployment. Lab scores are verification inputs, not the sole acceptance criterion.

## Risks and Unresolved Decisions

1. Form endpoint/privacy status is the only current critical blocker.
2. Reordering Evidence before Farm experience needs explicit approval under project governance.
3. New FAQ or shortened copy requires content/veterinary/legal approval; layout work cannot authorize wording changes.
4. No verified current packshot exists in production assets; an outdated label image must not be reused.
5. Source Serif 4 / Source Sans 3 require an approved self-hosted asset package; otherwise retain system fallbacks.
6. Hero image rights are attributed in footer, but redesign may need crop/format derivatives and confirmation that the license workflow remains compliant.
7. Evidence numbers are scope-sensitive. Visual prominence must not imply group-level efficacy beyond source documents.
8. Only RU is published; hardcoded JS strings will block clean localization if not addressed before the next locale.
9. `domain=null` prevents complete SEO/hreflang design verification.
10. Existing CSS can support the current page, but redesign should not be layered as another override pass.

## Implementation Notes

- Do not edit `designs/`; production work belongs in `production-src/` and is generated to `site/`.
- Implement only after the direction and selected review findings are explicitly approved.
- First implementation batch should establish semantic tokens, grid, type scale, header/hero and section primitives before individual evidence/video modules.
- Preserve calculator functions and tests; treat visual relocation separately from business logic.
- Preserve locale placeholders and move hardcoded UI status strings into the locale mechanism rather than duplicating templates.
- Update browser checks for 320, 390, 768, 1024, 1280 and 1440 px plus 200% zoom and reduced motion.
- Add a dedicated accessibility pass; current functional scripts are not a WCAG certification.

## Verification Checklist

- [ ] Business, audience, goal and primary conversion confirmed by owner.
- [ ] Form provider, recipient, privacy notice and success/recovery flow confirmed.
- [ ] Section reordering explicitly approved.
- [ ] Current package photography and image rights confirmed.
- [ ] Every claim mapped to manufacturer data, clinical observation, farm experience or application instruction.
- [ ] Dosage values and calculator outputs unchanged and tested.
- [ ] Hero complete and readable at 390×844 and 1440×900.
- [ ] No horizontal overflow at 320, 390, 768, 1024, 1280 and 1440 px.
- [ ] Keyboard flow, menu, tabs, disclosures, calculator, videos and form verified.
- [ ] Focus is visible and not obscured; touch targets meet the chosen 44 px target.
- [ ] Contrast measured for text, controls, icons and focus states.
- [ ] Captions verified; transcript/audio-description decision recorded per video.
- [ ] 200% zoom, text-spacing override, reduced motion and forced colors checked.
- [ ] Initial transfer and Core Web Vitals meet the documented budgets.
- [ ] No third-party asset/script loads before user intent without explicit approval.
- [ ] Final implementation matches this document or records an approved deviation.
