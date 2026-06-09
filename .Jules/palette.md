## 2025-05-22 - Keyboard Accessible Interaction Areas
**Learning:** Custom visual interaction areas (like the "orb" voice toggle) created with generic `<div>` tags require manual implementation of keyboard accessibility (e.g., `role="button"`, `tabindex="0"`, and `onkeydown` handlers for 'Enter' and 'Space') to be usable by non-mouse users.
**Action:** Always verify that interactive elements not using semantic HTML (like `<button>`) have appropriate ARIA roles, tabindex, and keyboard event handlers.
## 2026-06-09 - Intuitive Modal Focus Lifecycle
**Learning:** Keyboard-only and screen reader users can get trapped or confused if focus isn't managed when a modal opens and closes. Modals should automatically trap/shift focus to the first interactive element upon opening, and restore focus to the original active element (like a main command bar) upon closing.
**Action:** Always implement a complete focus lifecycle for custom modals (using `requestAnimationFrame` if necessary to handle async DOM updates), ensure the `Escape` key closes the modal, and intelligently handle `Enter` key submissions to avoid breaking standard inputs (like `<textarea>`).
