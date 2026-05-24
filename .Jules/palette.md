## 2025-05-22 - Keyboard Accessible Interaction Areas
**Learning:** Custom visual interaction areas (like the "orb" voice toggle) created with generic `<div>` tags require manual implementation of keyboard accessibility (e.g., `role="button"`, `tabindex="0"`, and `onkeydown` handlers for 'Enter' and 'Space') to be usable by non-mouse users.
**Action:** Always verify that interactive elements not using semantic HTML (like `<button>`) have appropriate ARIA roles, tabindex, and keyboard event handlers.
## 2025-05-22 - Improve accessibility of non-semantic tags
**Learning:** Changing non-semantic interactive tags (`<span>`, `<div>`) directly to `<button>` can lead to visual regressions because browsers apply default styling (borders, padding, background, text-align) to `<button>` elements that can break layouts.
**Action:** Instead of changing the tag name to `<button>`, add keyboard accessibility to existing non-semantic elements using `role="button"`, `tabindex="0"`, and an `onkeydown` event handler for 'Enter' and 'Space' keys. This ensures the functionality is accessible without risking layout breakages from default button styling.
