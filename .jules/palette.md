## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2025-01-26 - Keyboard Focus and Event Lifecycle for Vanilla JS Modals
**Learning:** When modals are created dynamically using `innerHTML` rather than existing purely in the DOM, setting focus immediately often fails because the DOM hasn't rendered yet. A `requestAnimationFrame` callback ensures the UI is ready to accept focus. Additionally, managing `Escape` and `Enter` globally via the document requires checking `.open` state, allowing standard interactive element usage (checking `active.tagName` for buttons/anchors), checking `e.defaultPrevented`, and requiring `Ctrl/Meta+Enter` for textareas to prevent eating regular newlines.
**Action:** Always wrap initial `.focus()` calls in `requestAnimationFrame` when injecting modal body HTML. For document-level keyboard listeners on modals, always whitelist native interactive tags and respect default prevented statuses to avoid unexpected interactions.

## 2026-07-30 - Async UI Loading States
**Learning:** Network latency or fetch failures can cause modal submission buttons to get permanently locked in a loading or disabled state if exceptions are not handled correctly.
**Action:** Always wrap async `fetch` API calls tied to button interactions in `try...catch...finally` blocks, and ensure the button's disabled state, text, and opacity are reset in the `finally` block to prevent permanent UI lockups.
