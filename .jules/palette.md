## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-06-25 - Modal Keyboard Accessibility and Focus Lifecycle
**Learning:** For dynamic, client-side modals (especially those injected via `innerHTML`), the focus lifecycle must be managed explicitly. Without auto-focusing on open, returning focus on close, and handling intuitive keys like Escape (close) and Enter (submit), the modals are functionally inaccessible to keyboard-only users. Furthermore, native element interactivity needs respect (e.g. TEXTAREA needs Ctrl+Enter so regular Enter can insert newlines).
**Action:** When creating or modifying dynamic modals, always implement a complete keyboard access lifecycle: requestAnimationFrame to focus first inputs, event listeners for Escape/Enter on the document scoped to the modal open state, and restoring focus to the primary UI element when closed.
