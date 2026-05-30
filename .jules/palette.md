## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-30 - [Modal Focus Flow and Keyboard Shortcuts]
**Learning:** In command-line or text-heavy interfaces, preserving focus state across modal interactions (e.g., auto-focusing inputs on modal open, and restoring focus to the main command bar on modal close) drastically reduces friction and the need to switch to a mouse. Additionally, adding document-level `Escape` key handlers and `Enter` key listeners on inputs inside modals creates a much smoother power-user experience.
**Action:** When implementing or refining modals, always ensure an intuitive focus lifecycle (open focus -> interact with keyboard -> close and restore focus).
