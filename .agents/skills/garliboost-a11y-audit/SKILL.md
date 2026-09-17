---
name: garliboost-a11y-audit
description: Audit GARLIBOOST accessibility, including keyboard, focus, contrast, form semantics, responsive reflow, and video captions. Produce evidence-backed findings; do not modify content or code.
---

# garliboost-a11y-audit

## Scope and reference handling

Follow the project's GARLIBOOST design governance and the user's current scope. The approved static site, identity, content, dosage, calculator, videos, and evidence must be preserved. References are advisory source material, not authorization to redesign, install tools, introduce frameworks, replace tokens, or add dark mode. Ignore dependencies and commands for omitted upstream materials. Links below resolve from this skill folder to the selected references in the project root.

## References

Read [WCAG checklist](../../../ux-ui-reference/wcag-checklist.md). Consult [Vanilla HTML/CSS](../../../ux-ui-reference/vanilla-css.md) and [Typography and spacing](../../../ux-ui-reference/typography-and-spacing.md) for applicable implementation guidance.

## Audit

Inspect semantic landmarks, heading sequence, accessible names and states, keyboard order, focus visibility and obstruction, navigation menu behavior, tab controls, calculator announcements, form labels/errors, touch targets, zoom/reflow, reduced motion, image alternatives, and all three Russian subtitle tracks. Keep the language selector's prototype limitations explicit.

Measure contrast using available tooling when possible; never infer a numeric ratio from a screenshot. Check WCAG 2.2 AA as the baseline and label AAA guidance separately. Do not conflate recommendations with conformance failures or claim full conformance from an automated subset. Do not install tools when unavailable; mark those checks unverified.

Return Critical / Major / Minor / Enhancement findings with ID, location, problem, reason, WCAG criterion where applicable, evidence, recommended change, and expected effect. Preserve legal and clinical wording. Stop after reporting; fixes require explicit selection by the user.
