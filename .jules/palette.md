## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2024-05-14 - Modal Keyboard Accessibility Lifecycle
**Learning:** For monolithic UI modals relying heavily on `innerHTML` injection, `requestAnimationFrame` is highly reliable for immediately auto-focusing dynamically created inputs upon opening. Additionally, handling the complete focus lifecycle (returning focus to the main input on close, supporting `Escape` key close, and robust `Enter` key form submission) significantly improves keyboard navigation fluidity.
**Action:** When adding modals or popovers that load dynamic content, use `requestAnimationFrame` to ensure focus states are set correctly, and ensure focus is explicitly returned to the trigger point or a primary global input upon closure.
