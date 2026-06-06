## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-06-07 - Smart Modal Keyboard Handling & Focus Management
**Learning:** When implementing global keydown event listeners for modal dialogues (e.g. `Escape` to close, `Enter` to submit) in vanilla JS, you must explicitly check `document.activeElement` to prevent `Enter` from inappropriately firing primary buttons if native interactive elements (`BUTTON`, `A`) are already focused by the user. Additionally, you should exempt `TEXTAREA` tags from default `Enter` form submissions (requiring `Ctrl+Enter` or `Meta+Enter` instead) so users can still insert newlines naturally.
**Action:** Always implement a smart focus lifecycle for custom modals: use `requestAnimationFrame` to autofocus the first input on open, restore focus to the primary command bar on close, and use selective tag/role exclusion logic for the `Enter` key.
