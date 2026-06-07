## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-11-09 - [Modal Focus & Keyboard Flow in Vanilla JS]
**Learning:** Fully accessible custom modals require more than just role attributes; they need an explicit focus lifecycle using `requestAnimationFrame` to reliably move focus onto inputs upon opening and restoring it to the original context upon closing, coupled with global `keydown` listeners for standard `Escape` and `Enter` handling.
**Action:** Always implement explicit focus lifecycle management and global keydown interceptors (that ignore inputs properly on Enter or require modifiers) when building or modifying custom modal components without a framework.
