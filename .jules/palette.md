## 2024-05-24 - Interactive Custom Elements Keyboard Support
**Learning:** Custom interactive elements (like the main orb `div` used for voice input) lack native keyboard semantics, which makes them inaccessible to keyboard-only users who can't trigger `onclick`.
**Action:** When building interactive `div` or `span` elements, always add `role="button"`, `tabindex="0"`, an appropriate `aria-label`, and an `onkeydown` handler to support `Enter` and `Space` key activation, alongside global `:focus-visible` styles to indicate focus.
