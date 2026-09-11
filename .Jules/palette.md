## 2025-05-22 - Keyboard Accessible Interaction Areas
**Learning:** Custom visual interaction areas (like the "orb" voice toggle) created with generic `<div>` tags require manual implementation of keyboard accessibility (e.g., `role="button"`, `tabindex="0"`, and `onkeydown` handlers for 'Enter' and 'Space') to be usable by non-mouse users.
**Action:** Always verify that interactive elements not using semantic HTML (like `<button>`) have appropriate ARIA roles, tabindex, and keyboard event handlers.
## 2025-05-23 - ARIA Live Regions and Dialog Roles for Custom Modals
**Learning:** In vanilla JS apps, containers receiving dynamic `innerHTML` updates (like `#notif-zone` or `#chat-log`) must have `aria-live="polite"` to announce changes to screen readers. Custom modals (like `#modal`) must include `role="dialog"`, `aria-modal="true"`, and `aria-labelledby` for proper accessibility.
**Action:** Always verify that dynamic update regions and custom overlay modals have the appropriate ARIA roles and attributes when using raw HTML/JS components.
