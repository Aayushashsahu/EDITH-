## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-24 - [Modal Keyboard Accessibility Lifecycle]
**Learning:** For a fully accessible modal experience in vanilla JS without external libraries, implementing an intuitive focus lifecycle is necessary. This includes auto-focusing inputs on open, restoring focus to the main command bar on close, and supporting document-level Escape key closure and Enter key form submissions (while ensuring TEXTAREA elements explicitly require Ctrl+Enter or Meta+Enter to avoid blocking standard newlines).
**Action:** Always implement this focus lifecycle and keyboard listener pattern when introducing new modals or reviewing existing ones.
