## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-07-24 - [Modal Keyboard Accessibility Lifecycle]
**Learning:** For dynamic modals created via innerHTML, managing the focus lifecycle is critical. `requestAnimationFrame` ensures auto-focus on inputs works reliably since elements are injected dynamically. Restoring focus to the main input on close prevents context loss. Furthermore, global document-level Enter/Escape listeners must handle native focusable elements (Textarea, Button) elegantly without blocking natural default behaviors (like newlines in Textarea, using Ctrl/Cmd+Enter for form submission instead).
**Action:** Implement robust focus management on all dynamic modals. Automatically move focus to inputs on open, restore focus on close, and use explicit keydown interception for Escape/Enter, guarding against intercepting default behavior for textareas and buttons.
