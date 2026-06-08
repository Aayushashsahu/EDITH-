## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2026-06-08 - [Modal Keyboard Accessibility and Focus Lifecycle]
**Learning:** Implementing intuitive focus lifecycles and complete keyboard support for modals significantly improves a11y. For vanilla JS setups without dedicated UI libraries, combining `requestAnimationFrame` for reliable autofocus on input fields upon opening, restoring focus to the primary interactive element on close, and centralizing `Enter` form submissions + `Escape` close handling in a global keydown listener (while avoiding interference with textarea line breaks or active buttons/links) creates a seamless, robust user experience.
**Action:** Use this pattern as the standard for any custom modal implementations in this project to guarantee baseline keyboard accessibility.
