## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-19 - [Modal Keyboard Accessibility Lifecycle]
**Learning:** For frontend UI changes involving modals, a full keyboard accessibility lifecycle ensures an intuitive experience. Using `requestAnimationFrame` allows reliable auto-focusing of inputs on modal open, and restoring focus to the main interface upon closure prevents screen readers or keyboard users from getting lost. Furthermore, global `Escape` key handling and context-aware `Enter` key handlers (that explicitly ignore native interactive tags and avoid blocking `TEXTAREA` newlines) make modals feel like native OS dialogs.
**Action:** Always implement this focus-management lifecycle (auto-focus on open, restore on close, Escape to close, Enter to submit) when building or modifying custom modal dialogs.
