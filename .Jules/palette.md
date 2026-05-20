## 2024-05-20 - Adding Accessibility to Custom HUD Toast Notifications
**Learning:** Custom UI overlay elements for notifications (like Stark-style HUD toasts) completely bypass screen readers unless explicitly marked as live regions. Because they are absolutely positioned and visually transient, screen reader users miss critical system feedback.
**Action:** Always wrap custom toast notification containers with `aria-live="polite"` and `aria-atomic="true"` to ensure screen readers announce the dynamic content automatically when it is injected into the DOM.

## 2024-05-20 - Keyboard Focus on Interactive Elements
**Learning:** When removing native input outlines to achieve a specific aesthetic (like a glowing CLI look), users relying on keyboard navigation lose track of their position entirely.
**Action:** Use `:focus-visible` instead of `:focus` to provide strong visual indicators (like outlines or borders) *only* when the user is navigating via keyboard, preserving the clean look for mouse users while maintaining accessibility.
