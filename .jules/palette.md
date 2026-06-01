## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2025-05-22 - Modal Focus Management & Keyboard Shortcuts
**Learning:** For frontend UI changes involving modals, full keyboard accessibility requires an intuitive focus lifecycle (auto-focusing inputs on open, restoring focus to the main command bar on close), and supporting document-level `Escape` key closure and `Enter` key form submissions to reduce friction for power users.
**Action:** Always implement comprehensive focus management and global/scoped keyboard shortcuts (Escape/Enter) when designing custom modal dialogue components.
