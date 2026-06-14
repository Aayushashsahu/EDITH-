## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-06-14 - [Modal Focus Lifecycle and Keyboard Accessibility]
**Learning:** Implementing full keyboard accessibility for dynamically rendered modals (like auto-focusing the first input on open, handling Escape to close, intercepting Enter to submit while skipping textareas, and restoring focus on close) significantly improves UX and accessibility without requiring complex dependencies.
**Action:** Always implement these focus lifecycle management techniques when building or modifying custom UI modals to ensure keyboard power users and screen readers can smoothly navigate.
