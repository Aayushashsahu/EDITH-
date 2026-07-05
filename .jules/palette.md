## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-19 - [Modal Keyboard Accessibility and Focus Lifecycle]
**Learning:** For dynamic modals created via `innerHTML`, autofocusing inputs requires `requestAnimationFrame` to ensure the DOM is ready. Additionally, comprehensive keyboard support requires handling `Escape` for closing, conditionally handling `Enter` for form submission (avoiding interference with focused buttons, native interactions, and standard newlines in textareas unless accompanied by a modifier key like `Ctrl` or `Meta`), and restoring focus to the primary command bar when closed.
**Action:** Always implement a complete focus lifecycle (auto-focus on open, restore on close) and full keyboard event support for dynamic modals to ensure seamless accessibility.
