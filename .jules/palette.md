## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2026-06-15 - Modal Keyboard Accessibility and Focus Lifecycle
**Learning:** In the custom, monolithic vanilla JS frontend, the lack of native `<dialog>` usage led to poor modal keyboard accessibility. Using pseudo-selectors like `:not(.open)` for Playwright visibility checks was unreliable; standard `Enter` key handlers conflicted with native interactive elements (`BUTTON`, `A`) or blocked newline input in `TEXTAREA`.
**Action:** Implemented a robust focus lifecycle using `requestAnimationFrame` for initial auto-focus of inputs on open, and returning focus to the primary command bar (`#cmd-in`) on close. Enabled `Escape` document-level closure, and carefully implemented `Enter` key form submission that requires `Ctrl+Enter`/`Meta+Enter` for `TEXTAREA` elements to avoid breaking standard multiline inputs.
