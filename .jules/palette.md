## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-07-06 - Keyboard focus styles for circular components
**Learning:** Adding `:focus-visible` to custom circular interactive elements like `#orb-area` results in a default square focus outline rendered by the browser. This looks broken visually.
**Action:** Always specify the matching `border-radius` (e.g., `50%`) on the `:focus-visible` pseudo-class for non-rectangular components to ensure the focus outline wraps the component geometry smoothly.
