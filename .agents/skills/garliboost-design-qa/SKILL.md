---
name: garliboost-design-qa
description: Verify GARLIBOOST responsive layout and existing interactions or check approved refinements for regressions. Report results and findings without automatically fixing the site.
---

# garliboost-design-qa

## Scope and reference handling

Follow the project's GARLIBOOST design governance and the user's current scope. The approved static site, identity, content, dosage, calculator, videos, and evidence must be preserved. References are advisory source material, not authorization to redesign, install tools, introduce frameworks, replace tokens, or add dark mode. Ignore dependencies and commands for omitted upstream materials. Links below resolve from this skill folder to the selected references in the project root.

## References

Use [Review criteria](../../../ux-ui-reference/design-review.md), [Accessibility checklist](../../../ux-ui-reference/wcag-checklist.md), [Breakpoint examples](../../../ux-ui-reference/breakpoints.json), and [Vanilla implementation principles](../../../ux-ui-reference/vanilla-css.md).

## Verification

Establish the authorized scope and current comparison point. Inspect available local testing tools before use; do not install dependencies or create a test pipeline. Check 1440px and 390px plus intermediate widths and both sides of the actual navigation breakpoint. Do not replace existing breakpoints with reference values.

Verify overflow, alignment, reading order, touch targets, closed/open burger menu, close button, navigation selection, Escape and focus behavior, language control visibility, three videos and Russian subtitle toggles, animal tabs, calculator valid/invalid input, form validation and demo-only submission, and evidence links as relevant to the scope. Preserve the calculation: 500 kg → 500 ml per 7 days → approximately 71.4 ml/day → approximately 35.7 ml twice daily. Never send real form data.

Inspect rendered previews and report observed behavior, viewport, expected result, actual result, and pass/fail/not-checked. Use existing suitable checks only after inspecting their side effects; keep temporary captures outside source directories. Do not claim a skipped check passed. Group defects by Critical / Major / Minor / Enhancement with ID, location, problem, reason, recommendation, and expected effect. Stop without auto-fixes or commits.
