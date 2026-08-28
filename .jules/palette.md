## 2024-05-18 - [Accessibility on Non-Semantic Elements]
**Learning:** Adding `role="button"`, `tabindex="0"`, `aria-label`, and `onkeydown` handlers (for Enter and Space keys) effectively retrofits keyboard accessibility onto existing `<span>` and `<div>` elements with `onclick` handlers, improving UX without requiring structural HTML changes that might break layout or styling.
**Action:** Always check for `onclick` attributes on non-semantic tags and apply this pattern if changing the tag to `<button>` is risky or unfeasible.

## 2025-01-26 - Keyboard Focus and Event Lifecycle for Vanilla JS Modals
**Learning:** When modals are created dynamically using `innerHTML` rather than existing purely in the DOM, setting focus immediately often fails because the DOM hasn't rendered yet. A `requestAnimationFrame` callback ensures the UI is ready to accept focus. Additionally, managing `Escape` and `Enter` globally via the document requires checking `.open` state, allowing standard interactive element usage (checking `active.tagName` for buttons/anchors), checking `e.defaultPrevented`, and requiring `Ctrl/Meta+Enter` for textareas to prevent eating regular newlines.
**Action:** Always wrap initial `.focus()` calls in `requestAnimationFrame` when injecting modal body HTML. For document-level keyboard listeners on modals, always whitelist native interactive tags and respect default prevented statuses to avoid unexpected interactions.
## 2025-01-26 - Async Modal Buttons & Finally Block
**Learning:** For async fetch operations triggered inside dynamic modals, it's critical to restore the loading state within a `finally` block. Without it, failed requests leave the UI disabled and permanently stuck.
**Action:** Always wrap async submit actions in `try...finally` to ensure the modal's primary button unconditionally resets to a usable state, regardless of whether the network request succeeds or fails.

## 2026-08-02 - [Async Loading States on UI Buttons]
**Learning:** When implementing async loading states on UI buttons, always wrap the network request in a `try...finally` block to unconditionally reset the button state (`btn.disabled = false`), preventing the UI from getting permanently stuck if the request fails.
**Action:** Use `try...finally` pattern for all async operations triggered by user actions.
## 2024-08-04 - Strict ARIA labels required for unlabelled input fields in innerHTML modals
**Learning:** Monolithic vanilla JS apps heavily relying on dynamic `innerHTML` modal templates often lack structural semantic `<form>` contexts or explicit `<label>` tags to maintain minimalistic styling. This causes screen readers to misidentify input/textarea elements, treating them only by their `placeholder` attribute (if at all), matching the "Bad UX Code" pattern.
**Action:** When working on dynamic `innerHTML` templates lacking semantic context, always ensure inputs and textareas strictly carry explicit descriptive `aria-label` attributes for accessibility compliance.

## 2025-01-26 - Dynamic innerHTML Containers and Modals Require Explicit ARIA Attributes
**Learning:** Monolithic vanilla JS apps that rely heavily on dynamic `innerHTML` to update content in UI components like notification zones, chat logs, and custom modals often bypass native semantic elements. Without native roles, screen readers won't announce changes (for chat/notifications) or understand the context (for modals).
**Action:** When updating or creating dynamic `innerHTML` containers for notifications or live chat, always add `aria-live="polite"` so screen readers announce changes. For custom modals built from generic `<div>` tags, ensure they include `role="dialog"`, `aria-modal="true"`, and `aria-labelledby` linking to a visible title element to provide the correct semantic structure.
