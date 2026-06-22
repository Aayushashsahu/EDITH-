## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-06-22 - [Keyboard Accessibility for Modals]
**Learning:** Managing a full keyboard focus lifecycle is critical for accessibility in dynamically injected UI modals. This involves using `requestAnimationFrame` to wait for elements injected via `innerHTML` to become available before calling `.focus()`, returning focus to the primary context (`cmd-in`) on closure, and supporting intuitive global interactions like `Escape` to close and `Enter` to submit, while handling exceptions for `TEXTAREA` (requiring modifiers) and native focused elements like `BUTTON` or `A` to prevent conflict.
**Action:** Always implement a complete focus loop (focus on open, restore on close) and global keyboard bindings (`Escape`, `Enter`) when creating or modifying custom modal implementations.
