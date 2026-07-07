## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-19 - [Modal Keyboard Lifecycle and Accessibility]
**Learning:** When modals inject content dynamically via `innerHTML`, autofocusing inputs requires `requestAnimationFrame` to ensure elements are present in the DOM before `focus()` is called. Furthermore, a robust document-level key event listener (`Escape` to close, `Enter` to submit via `.m-btn`) greatly improves UX but must respect `e.defaultPrevented`, native interactive element focus (`BUTTON`, `A`), and require modifier keys for `<textarea>`s to avoid intercepting legitimate input. Lastly, focus should be restored to the primary input (like a command bar) upon modal closure for a seamless loop.
**Action:** Always implement a complete "open → autofocus → interact (Esc/Enter) → close → restore focus" lifecycle for custom modals to ensure full keyboard accessibility.
