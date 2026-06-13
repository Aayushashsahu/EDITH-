## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-06-13 - [Modal Focus & Keyboard Shortcuts]
**Learning:** Adding a complete focus lifecycle to modals (auto-focusing inputs on open and restoring focus to the main input on close) along with standard keyboard shortcuts (`Escape` to close, `Enter` to submit) dramatically improves keyboard accessibility and general UX. Intercepting `Enter` in the modal required a nuanced approach: allowing standard button clicks and newlines in `TEXTAREA`s (unless `Ctrl+Enter` is used) while redirecting standard inputs to the modal's primary action button.
**Action:** Consistently implement this focus lifecycle and keyboard shortcut pattern for all custom modal dialogs to meet accessibility expectations and provide a smoother, more intuitive user experience.
