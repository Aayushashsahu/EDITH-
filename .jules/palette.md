## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2026-07-04 - [Modal Focus Lifecycle]
**Learning:** When modals inject inputs dynamically via `innerHTML`, standard `autofocus` attributes often fail. Using `requestAnimationFrame` ensures elements exist in the DOM before attempting to focus them. Restoring focus to the main input on close and implementing global Escape/Enter handlers creates a seamless keyboard loop.
**Action:** Always implement a complete focus lifecycle (focus inward on open, restore outward on close) and document-level key handlers for custom modal components to ensure full keyboard accessibility.
