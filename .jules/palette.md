## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-19 - [Modal Keyboard Accessibility and Focus Lifecycle]
**Learning:** For modal interfaces injected dynamically via `innerHTML` without frameworks, ensuring a complete keyboard accessibility lifecycle is crucial. `requestAnimationFrame` is necessary to reliably set focus on inputs right after DOM insertion. Returning focus to the main application context (like the command bar) on close prevents focus from being lost in the body. Finally, mapping `Escape` to close and `Enter` to submit (while handling `TEXTAREA` explicitly with `Ctrl+Enter`) creates a seamless keyboard-only flow.
**Action:** Always implement this focus lifecycle (auto-focus on open, restore focus on close) and keyboard mapping (Escape to cancel, Enter to submit) when building or modifying custom modals to ensure screen reader and power user compatibility.
