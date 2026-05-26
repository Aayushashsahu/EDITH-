## 2025-05-22 - Keyboard Accessible Interaction Areas
**Learning:** Custom visual interaction areas (like the "orb" voice toggle) created with generic `<div>` tags require manual implementation of keyboard accessibility (e.g., `role="button"`, `tabindex="0"`, and `onkeydown` handlers for 'Enter' and 'Space') to be usable by non-mouse users.
**Action:** Always verify that interactive elements not using semantic HTML (like `<button>`) have appropriate ARIA roles, tabindex, and keyboard event handlers.
## 2026-05-26 - Layout-Preserving Accessibility for Spans
**Learning:** When custom CSS constraints prohibit replacing interactive `<span>` or `<div>` tags with native semantic `<button>` elements due to visual layout breakage, keyboard accessibility can be safely achieved by augmenting the existing tags with `role="button"`, `tabindex="0"`, and `onkeydown` event handlers for 'Enter' and 'Space'. This preserves the existing design while making the interactions accessible.
**Action:** When adding accessibility to legacy non-semantic tags with strict visual styling, use the `role/tabindex/onkeydown` pattern as a safe alternative to native `<button>` replacements.
