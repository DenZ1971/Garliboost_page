---
name: garliboost-redesign
description: Implement only specific GARLIBOOST design-review findings explicitly selected by the user. For an unreviewed improvement request, provide findings first and stop; never initiate a fresh redesign.
---

# garliboost-redesign

## Scope and reference handling

Follow the project's GARLIBOOST design governance and the user's current scope. The approved static site, identity, content, dosage, calculator, videos, and evidence must be preserved. References are advisory source material, not authorization to redesign, install tools, introduce frameworks, replace tokens, or add dark mode. Ignore dependencies and commands for omitted upstream materials. Links below resolve from this skill folder to the selected references in the project root.

## References

Use [Refinement sequence](../../../ux-ui-reference/redesign-audit.md), [Review criteria](../../../ux-ui-reference/design-review.md), [Vanilla HTML/CSS](../../../ux-ui-reference/vanilla-css.md), and [Typography and spacing](../../../ux-ui-reference/typography-and-spacing.md). Consult [Accessibility](../../../ux-ui-reference/wcag-checklist.md) for the changed interaction. [Typography examples](../../../ux-ui-reference/typography.json) and [Spacing examples](../../../ux-ui-reference/spacing.json) are optional comparative references, not values to impose.

## Authorization boundary

Despite its name, this skill is for surgical refinement of the approved design. Identify the selected finding IDs and authorized changes from the conversation. If the user has not selected findings, inspect the relevant area, return findings with location, problem, reason, recommended change, and expected effect grouped Critical / Major / Minor / Enhancement, then stop without edits. Do not repeat approval requests for already selected findings.

## Authorized implementation

Record the pre-change state. Make the minimum HTML/CSS/vanilla-JS changes needed for selected findings, retaining identity, section order, content, clinical meaning, evidence, videos, captions, and calculator formula. Do not automatically carry out the upstream aesthetic-selection step, global token migration, theme consolidation, dark mode, motion additions, or framework conversion. A content rewrite needs explicit authorization beyond general visual refinement.

Verify affected behavior and responsive layouts with available tools, compare desktop/mobile previews, and inspect the diff for unrelated changes. Report the selected findings addressed, files changed, verification and remaining limitations. New issues outside scope are findings only. Do not commit, install dependencies, deploy, or perform unrelated cleanup without a separate user instruction.
