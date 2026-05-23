## 2024-05-23 - Interactive Elements Semantics
**Learning:** In custom UI components, using `<div>` or `<span>` with `onclick` handlers often strips them of native keyboard accessibility. Elements like `+ ADD` or task rows need manual handling for focus (`tabindex`) and keyboard events (`keydown`) if built this way.
**Action:** Always prefer native semantic `<button>` elements for complex interactive features. It provides built-in keyboard navigation (Tab focus) and interaction (Enter/Space to trigger) without writing custom JS, which is essential for accessibility.
