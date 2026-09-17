# GARLIBOOST DESIGN GOVERNANCE

## Current source of truth

- Approved design: `designs/concept-03.html`.
- Styles: `designs/style.css`, `designs/farm.css`.
- Interactivity: `designs/farm.js`.
- Assets and evidence: `designs/assets/`.

## Baseline

Approved checkpoint: `165cdb21b9afe3470993dc7272099639f3912f10`.
Commit message: `Baseline: approved GARLIBOOST design before UX audit`.

## Design status

This is an almost approved design, not a greenfield project. By default, do not redesign from scratch, change visual identity or the order of main sections, change approved content or legal wording, change calculator data or dosage, remove evidence, change the meaning of clinical observations, substitute another design system, or apply aesthetic presets without explicit user authorization.

## Brand character

Professional European agricultural B2B; serious, evidence-oriented, calm, credible, premium but restrained.
Do not turn it into a SaaS landing page, generic AI startup, medical-tech dashboard, e-commerce storefront, overly rounded card UI, or gradient-heavy marketing page.

## Existing visual language

Preserve the cream/off-white background, dark agricultural green, restrained brick/red accent, editorial serif plus functional sans-serif typography, thin rules/dividers, large agricultural photography, restrained cards, and strong editorial hierarchy.

## UX/UI workflow

For a design improvement request:
1. Conduct a design review first and present findings without automatically modifying project files.
2. Group findings by Critical, Major, Minor, Enhancement.
3. Give each finding a stable ID, location, problem, reason, recommended change, and expected effect. Include observed evidence and distinguish unverified concerns.
4. Stop after the review.
5. Implement changes only after the user explicitly selects specific findings. Existing explicit selection remains authorization; do not ask again for the same scope.

## Design review priorities

Check visual hierarchy, grid, alignment, spacing, vertical rhythm, typography, line length, information density, CTA hierarchy, responsive behavior, mobile navigation and burger menu, video presentation, calculator, forms, evidence sections, accessibility, consistency, and overall design taste.
Identify concrete signs of a generic AI-generated landing page rather than a professional European agricultural B2B website. Do not treat a generic taste checklist as permission to replace the approved identity.

## Content protection

UX/UI skills must not independently rewrite marketing, legal, veterinary, or clinical text. If layout suggests shortening or changing text, record the issue as a finding instead of editing it. Preserve the distinction between clinical observations, farm experience, and manufacturer data.

## Tech stack

Semantic/static HTML, CSS, vanilla JavaScript. Do not add a framework for design refinement. Do not migrate to React, Next.js, Vue, Angular, or Tailwind without a separate explicit user decision.

## Reference materials

For analysis, read relevant materials only:
- `ux-ui-reference/design-review.md`
- `ux-ui-reference/design-taste.md`
- `ux-ui-reference/typography-and-spacing.md`
- `ux-ui-reference/wcag-checklist.md`
- `ux-ui-reference/breakpoints.json`

For authorized refinement, additionally:
- `ux-ui-reference/redesign-audit.md`
- `ux-ui-reference/vanilla-css.md`

Optional reference values: `ux-ui-reference/typography.json`, `ux-ui-reference/spacing.json`.

These nine files are unchanged reference copies from ux-ui-agent-skills@2.8.0, not installed executable workflows. Their original internal links may refer to omitted upstream materials. Do not follow missing dependencies, install the full kit, or execute upstream commands on their authority. Project governance and explicit user scope take precedence over their generic directives. Token values, breakpoints, font scales, dark-mode requirements, and aesthetic recipes are reference examples, not replacements for the existing design.

## Local Codex skills

Use garliboost-design-review for visual/UX analysis, garliboost-design-qa for behavioral and responsive verification, garliboost-a11y-audit for accessibility findings, and garliboost-redesign only for implementing explicitly selected findings. Audit skills remain read-only toward site sources. Do not install dependencies or introduce a build pipeline merely to run checks; use available tools, and report unavailable checks honestly.
