## 2024-05-18 - Making Custom Interactive Elements Accessible
**Learning:** When using generic elements like `div` for interactive components (like the `orb-area`), they inherently lack semantic meaning and keyboard focusability. This makes them completely invisible to screen readers and inaccessible to keyboard users.
**Action:** Always add `role="button"` (or appropriate role), `tabindex="0"`, an `aria-label`, and explicitly handle keyboard events (like 'Enter' or 'Space') to mimic standard button behavior.
