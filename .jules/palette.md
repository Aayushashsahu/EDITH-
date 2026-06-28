## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2025-05-23 - Modal Focus Lifecycle and Keyboard Controls
**Learning:** Vanilla JS modals injecting elements via `innerHTML` require using `requestAnimationFrame` to safely auto-focus inputs because the DOM needs to update first. Also, global `Enter` key listeners for form submission inside modals must carefully avoid intercepting `TEXTAREA` newlines (unless modified by Ctrl/Meta) and native interactive elements like `BUTTON` or `A`.
**Action:** When implementing custom modals, always include an intuitive focus lifecycle (auto-focus first input on open, restore focus to main UI on close) and document-level keydown handlers for `Escape` and smart `Enter`.
