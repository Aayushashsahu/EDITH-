## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-07-24 - Circular Focus Indicators
**Learning:** When adding `:focus-visible` outlines to non-rectangular UI components (like circular orbs), browsers default to drawing a square box.
**Action:** Always match the component's `border-radius` (e.g. `50%`) on the `:focus-visible` state specifically for those elements to ensure the outline wraps the shape correctly.
