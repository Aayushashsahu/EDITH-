## 2025-01-24 - Accessibility Keyboard Handlers on Non-Native Elements
**Learning:** In constraint-heavy environments (like where custom CSS shouldn't be added), substituting native `<button>` tags for interactive non-semantic elements (like `<span>` or `<div>`) can risk visual layout breakage due to default browser styling of the button tag.
**Action:** Achieve keyboard accessibility safely on these elements by adding `role="button"`, `tabindex="0"`, and `onkeydown` event handlers specifically for 'Enter' and 'Space' keys, mapping them to the existing click handlers.
