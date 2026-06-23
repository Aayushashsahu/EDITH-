## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2025-02-12 - [Modal Focus and Keyboard Accessibility]
**Learning:** In a vanilla JS app heavily reliant on `innerHTML` for dynamic modals, inputs don't natively autofocus, and modals lack `Escape` key and `Enter` key handlers. Using `requestAnimationFrame` allows newly injected DOM elements (like inputs) to be reliably targeted for autofocus. Combining this with a document-level event listener scoped to active modals creates a robust, accessible keyboard lifecycle (Escape to close, Enter to submit) without disrupting focus states on buttons or blocking multiline text entry.
**Action:** Always implement a complete focus lifecycle (focus inward on open, restore focus outward on close) and document-level keyboard shortcuts for any custom modal system.
