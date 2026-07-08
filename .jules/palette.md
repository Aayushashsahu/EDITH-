## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-18 - [Dynamic Modal Focus Lifecycle]
**Learning:** For dynamic modals populated via `innerHTML`, an intuitive focus lifecycle is critical for accessibility. Using `requestAnimationFrame` ensures auto-focus targets are mounted before selection. Supporting document-level `Escape` to close and `Enter` to submit (with caveats for `TEXTAREA` requiring `Ctrl+Enter` / `Meta+Enter` and ignoring native buttons/links) dramatically improves keyboard usability without mouse interaction. Restoring focus to the main input on close keeps the user in flow.
**Action:** Always implement a complete focus lifecycle (auto-focus on open, restore on close) and keyboard shortcuts (Escape, Enter) for dynamic modals, respecting standard HTML behavior (e.g., textareas, native buttons).
