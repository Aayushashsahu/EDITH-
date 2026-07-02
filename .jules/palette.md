## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-07-02 - [Focus Outline Shapes for Non-Rectangular UI Elements]
**Learning:** Standard `:focus-visible` outlines on non-rectangular elements (like the circular orb/microphone toggle) apply as squares by default, which looks unpolished and breaks the aesthetic. Using `border-radius: 50%` with `:focus-visible` accurately conforms the outline to the element's visual shape, improving both accessibility and design consistency.
**Action:** When adding global `:focus-visible` styles, explicitly override the `border-radius` for prominently curved or circular interactive elements.
