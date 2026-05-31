## 2024-12-07 - Improved Modal Keyboard Accessibility
**Learning:** Full keyboard support in modals (auto-focusing inputs on open, closing with Escape, and supporting Enter for form submission) drastically reduces friction for power users and screen readers, but requires manually tracking and restoring focus when the modal closes.
**Action:** Always implement a complete focus lifecycle (`lastFocusedElement` tracking and restoration) and global Escape key handlers when building custom modal components to ensure they feel native and accessible.
