## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-06-27 - [Modal Focus & Keybindings Lifecycle]
**Learning:** Implementing explicit auto-focus via requestAnimationFrame on modal open and restoring focus to main inputs on close is crucial for keyboard users, as is handling document-level Escape and contextual Enter logic. For textareas, explicitly require Ctrl+Enter or Meta+Enter to avoid blocking newlines. Avoid Enter interception when native interactive elements are focused.
**Action:** Apply this comprehensive focus and keybinding lifecycle whenever dynamically injecting modal content via innerHTML.
