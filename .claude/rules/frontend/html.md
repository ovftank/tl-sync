---
paths:
  - "templates/**/*.html"
  - "**/*.html"
---

# Frontend HTML

## Conventions

- UI text: Tiếng Việt
- Dashboard app - NO accessibility/SEO attributes needed (aria-label, role, alt, semantic HTML)
- **Color scheme ONLY**: black (gray-900) and white (gray-50/100/200/300/400/700) - NO green, red, or other colors

## Tech Stack

- **TailwindCSS v4** (CDN): `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`
- **AlpineJS v3.15** (CDN): `https://cdn.jsdelivr.net/npm/alpinejs@3.15.4/dist/cdn.min.js`
- **Font Awesome 4.7**: Icons
- **Jinja2**: Server-side templating

## HTML Tags

**Allowed:** `<!doctype>`, `<html>`, `<head>`, `<body>`, `<div>`, `<form>`, `<section>`, `<label>`, `<input>`, `<button>`, `<script>`, `<style>`, `<meta>`, `<title>`, `<link>`, `<template>`, `<span>`

**NOT used:** `<h1>` - `<h6>` (use `<div>` with text utilities)

## TailwindCSS v4 Breaking Changes

**Renamed utilities (v3 → v4):**

```html
<!-- Shadow -->
shadow-sm (v3)   → shadow-xs (v4)
shadow (v3)      → shadow-sm (v4)

<!-- Ring -->
ring (v3)        → ring-3 (v4)
<!-- Color default changed from blue-500 to currentColor -->
focus:ring → focus:ring-3 focus:ring-blue-500

<!-- Outline -->
outline-none (v3) → outline-hidden (v4)

<!-- Opacity (REMOVED in v4 - use color/opacity syntax) -->
bg-opacity-50 (v3)   → bg-gray-500/50 (v4)
text-opacity-75 (v3) → text-gray-900/75 (v4)
border-opacity-50 (v3) → border-gray-500/50 (v4)
```

**New v4 syntax:**

```css
@import 'tailwindcss';
@theme {
  --color-custom-100: oklch(0.99 0 0);
  --font-display: "Satoshi", sans-serif;
}
```

## Color Palette (Project-Specific)

**IMPORTANT: ONLY use gray/white colors - NO green, red, blue, yellow, etc.**

```html
<!-- Text -->
text-gray-900    <!-- Darkest - headings -->
text-gray-700    <!-- Medium - labels, message text -->

<!-- Backgrounds -->
bg-white         <!-- Main container -->
bg-gray-50       <!-- Card background -->
bg-gray-100      <!-- Message/feedback background -->

<!-- Borders -->
border-gray-200  <!-- Light border -->
border-gray-300  <!-- Input border -->
border-gray-900  <!-- Section divider (bold) -->

<!-- Buttons -->
bg-gray-900      <!-- Primary button -->
bg-gray-700      <!-- Primary button hover -->
hover:bg-gray-100 <!-- Secondary button hover -->

<!-- Focus rings (v4: need explicit color) -->
focus:ring-3 focus:ring-gray-400
focus:border-gray-400
```

**Typography patterns:**

```html
text-sm font-medium text-gray-700    <!-- Label -->
text-lg font-medium text-gray-700    <!-- Section title -->
text-2xl font-semibold text-gray-900 <!-- Main heading -->
```

## UI Patterns

### Loading State

```html
<button :disabled="isLoading" class="disabled:opacity-50 disabled:cursor-not-allowed" x-text="isLoading ? 'Đang lưu...' : 'Lưu'"></button>
```

### Message Feedback

```html
<!-- Only gray/white colors -->
<div x-show="message.text">
  <span class="px-4 py-2 rounded-lg bg-gray-100 text-gray-900" x-text="message.text"></span>
</div>
```

### Form Labels

```html
<!-- Correct -->
<label for="userChatId" class="block text-sm font-medium text-gray-700 mb-2">Chat ID</label>

<!-- Wrong - label must match input purpose -->
<label for="userChatId">Tên</label>
```

## AlpineJS Patterns

### Component Structure

```javascript
const configForm = () => ({
  // State
  adminGroup: { chatid: 0, admins: [] },
  userGroup: { chatid: 0, users: [] },
  admins: [],
  users: [],
  message: { text: '', type: '' },
  isLoading: false,

  // Methods
  addAdmin() { this.admins.push({ chatid: '', prefix: '', topicid: '' }); },
  removeAdmin(index) { this.admins.splice(index, 1); },
  async submitForm() {
    this.isLoading = true;
    try {
      // API call
    } finally {
      this.isLoading = false;
    }
  }
});
```

### Dynamic Lists

```html
<template x-for="(item, index) in items" :key="index">
  <div>
    <button @click="removeItem(index)">Xóa</button>
  </div>
</template>
```