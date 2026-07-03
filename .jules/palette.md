## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2026-07-03 - [Modal Keyboard Accessibility Lifecycle]
**Learning:** Implementing full keyboard accessibility for dynamically injected modals requires explicit focus management. Using `requestAnimationFrame` ensures auto-focusing elements works reliably after `innerHTML` injection. Handling `Enter` key submissions globally requires careful exclusion of native interactive elements (like `BUTTON` and `TEXTAREA`) and respecting `e.defaultPrevented` to prevent conflicts with custom components. Restoring focus to the previously active element (or fallback command bar) upon closure completes the loop.
**Action:** Apply this comprehensive focus lifecycle and keydown handling pattern to any custom modal system to ensure robust keyboard navigation and accessibility.
