## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2026-06-16 - [Modal Keyboard Accessibility Lifecycle]
**Learning:** Implementing a full keyboard lifecycle for modals (auto-focusing inputs on open, restoring focus on close, and handling Escape/Enter document-level) significantly improves accessibility, but requires careful event delegation to avoid overriding standard interactions (like newlines in textareas or activating other focused buttons).
**Action:** Apply this comprehensive modal focus and keyboard handling pattern to all custom modal implementations.
