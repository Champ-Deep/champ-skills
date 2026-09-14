# Platform Guidelines

## React / Next.js

### Architecture Patterns

**CSS Modules** for component-scoped styles — zero runtime cost, full CSS feature access.
**Tailwind CSS** for utility-first rapid development — customize the config aggressively. Don't ship with default Tailwind tokens; override colors, fonts, spacing.
**CSS-in-JS** (Styled Components, Emotion) for truly dynamic styles based on props — but avoid for static styles due to runtime overhead.

### Performance

- Use **Server Components** by default in Next.js App Router — only add `'use client'` when you need interactivity or browser APIs
- **Image optimization**: Use Next.js `<Image>` component — automatic WebP/AVIF, lazy loading, blur placeholder
- **Font optimization**: Use `next/font` — eliminates layout shift, self-hosts fonts
- **Dynamic imports**: `dynamic(() => import('./Heavy'))` for code splitting heavy components
- **Bundle analysis**: `@next/bundle-analyzer` — run before each major release

### Component Patterns

```jsx
// Design tokens via CSS custom properties — works across any styling system
const TokensProvider = () => (
  <style>{`
    :root {
      --color-primary: oklch(55% 0.2 260);
      --space-sm: 0.5rem;
      --space-md: 1rem;
      --radius-md: 0.5rem;
    }
  `}</style>
);

// Compound components for complex UI — cleaner API than prop-drilling
const Card = ({ children }) => <div className={styles.card}>{children}</div>;
Card.Header = ({ children }) => <div className={styles.header}>{children}</div>;
Card.Body = ({ children }) => <div className={styles.body}>{children}</div>;

// Usage: <Card><Card.Header /><Card.Body /></Card>
```

### Common Mistakes

- Importing heavy libraries client-side that could be server-side
- Not using `Suspense` boundaries around data-fetching components
- Using `useEffect` for data fetching instead of React Query / SWR
- Skipping `key` props or using array indexes as keys

---

## Vue / Nuxt

### Architecture Patterns

**Scoped styles** (`<style scoped>`) — Vue's default component isolation.
**CSS custom properties** for design tokens — reactive with `v-bind()` in `<style>`.
**Pinia** for global state — composable, TypeScript-friendly.
**Nuxt UI** or **Shadcn-Vue** — customize tokens before using components.

### Performance

- **Lazy hydration** (`LazyComponent`) for below-fold components
- **useLazyAsyncData** for non-critical data
- **Nuxt Image** module for automatic optimization
- **Tree-shaking**: Import only what you use from component libraries

### Component Patterns

```vue
<template>
  <button :class="buttonClasses" v-bind="$attrs">
    <slot />
  </button>
</template>

<script setup>
const props = defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' }
});

const buttonClasses = computed(() => ({
  'btn': true,
  [`btn--${props.variant}`]: true,
  [`btn--${props.size}`]: true
}));
</script>
```

---

## Svelte / SvelteKit

### Architecture Patterns

**Scoped CSS** by default — no class name collisions, zero runtime overhead.
**Svelte stores** for reactive global state — simpler than Redux/Pinia.
**SvelteKit** for SSR/SSG — load functions for data fetching.
**Transitions API** for smooth animations — built-in `fly`, `fade`, `slide`, `scale`.

### Performance

Svelte has the best out-of-box performance of any major framework — compiles to vanilla JS, no virtual DOM. Focus on:
- **Lazy loading routes** via dynamic imports in SvelteKit
- **Intersection Observer** for scroll-triggered features
- **Web Vitals**: Svelte's compile step eliminates most React performance anti-patterns

### Motion Patterns

```svelte
<script>
  import { fly, fade } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
  let visible = false;
</script>

{#if visible}
  <div
    transition:fly={{ y: 20, duration: 300, easing: cubicOut }}
  >
    Content
  </div>
{/if}
```

---

## Tailwind CSS / shadcn/ui

### Customization (Non-Negotiable)

**Override the default tokens immediately.** Default Tailwind produces instant visual clichés.

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Replace these with OKLCH values from your palette
        primary: 'oklch(55% 0.22 260)',
        surface: 'oklch(98% 0.005 80)',
      },
      fontFamily: {
        // Replace Inter with your chosen font
        sans: ['Your Font', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        // Establish a consistent radius vocabulary
        sm: '4px',
        md: '8px',
        lg: '12px',
        xl: '16px',
      }
    }
  }
}
```

### shadcn/ui Customization

1. Install components via CLI — they live in your codebase, not a dependency
2. Modify component source directly — you own it
3. Override CSS variables in `globals.css` for theme-wide changes
4. Use `cn()` utility for conditional class merging

### Common Mistakes

- Using `bg-blue-500` directly instead of semantic token (`bg-primary`)
- Not purging unused styles in production
- Using arbitrary values (`w-[317px]`) instead of design tokens
- Mixing Tailwind with conflicting CSS-in-JS

---

## HTML / CSS (Vanilla)

### Architecture Principles

**CSS custom properties for all tokens** — single source of truth, no build step required.
**Progressive enhancement** — start with working HTML, layer CSS, then JS.
**BEM naming** for class-based CSS — Block, Element, Modifier prevents conflicts.

```css
/* Token layer */
:root {
  --color-primary: oklch(55% 0.2 260);
  --font-body: 'Charter', 'Bitstream Charter', 'Sitka Text', Cambria, serif;
  --space-unit: 4px;
  --radius-base: 8px;
}

/* Component layer */
.card { /* Block */
  background: var(--color-surface);
  border-radius: var(--radius-base);
}
.card__header { /* Element */
  padding: calc(var(--space-unit) * 4);
}
.card--featured { /* Modifier */
  border: 2px solid var(--color-primary);
}
```

### Performance

- **System font stacks** for zero-FOUT performance-critical apps
- **Critical CSS** inline for above-fold, async the rest
- **Logical properties** (`margin-inline`, `padding-block`) for bidirectional support

---

## React Native

### Design System

React Native has no CSS — use `StyleSheet.create()` for performance.

```jsx
const styles = StyleSheet.create({
  button: {
    backgroundColor: colors.primary,
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.md,
    minHeight: 44, // Touch target minimum
  },
  buttonText: {
    color: '#fff',
    fontFamily: fonts.sans,
    fontSize: 16,
    fontWeight: '600',
  }
});
```

### Platform-Specific

```jsx
import { Platform } from 'react-native';

const shadow = Platform.select({
  ios: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  android: {
    elevation: 4,
  },
});
```

### Performance

- **FlatList / SectionList** — never `ScrollView` with `map()` for long lists
- **memo()** — wrap expensive components
- **Animated API** — use native driver (`useNativeDriver: true`) for 60fps
- **Image**: Use `@shopify/flash-list` for image-heavy lists

### Navigation

- **React Navigation** — standard choice, well-maintained
- **Expo Router** — file-based routing (if using Expo)
- Deep linking support is table stakes — configure from day one

---

## Flutter

### Design System

```dart
ThemeData customTheme = ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: const Color(0xFF635BFF), // Your brand color
    brightness: Brightness.light,
  ),
  useMaterial3: true,
  textTheme: TextTheme(
    headlineLarge: TextStyle(
      fontFamily: 'YourFont',
      fontWeight: FontWeight.bold,
    ),
  ),
);
```

### Material 3 Principles

- Use **dynamic color** (`ColorScheme.fromSeed`) — generates full tonal palette from brand color
- Use **semantic components** (FilledButton, OutlinedButton, TextButton) — not custom widgets for standard interactions
- **Custom painters** for truly bespoke UI elements — but profile performance

### Performance

- **const constructors** — reduces rebuilds
- **ListView.builder** — lazy list rendering
- **RepaintBoundary** — isolate expensive subtrees
- **Avoid `BuildContext` lookups in loops** — cache Theme.of(context) above loops

---

## SwiftUI

### Design System

```swift
// Define tokens via extension
extension Color {
  static let brandPrimary = Color("BrandPrimary") // From asset catalog
  static let surface = Color(.systemBackground)
}

extension Font {
  static let displayLarge = Font.custom("YourFont", size: 36)
    .weight(.bold)
}

// ViewModifier for consistent component styling
struct CardStyle: ViewModifier {
  func body(content: Content) -> some View {
    content
      .padding(16)
      .background(.background)
      .clipShape(RoundedRectangle(cornerRadius: 12))
      .shadow(color: .black.opacity(0.08), radius: 8, y: 4)
  }
}
```

### Platform Integration

- **SF Symbols** — use for icons; they scale with Dynamic Type and match platform
- **Dynamic Type** — use `.font(.body)` system fonts or `scaledFont` for custom fonts
- **Environment values** (`@Environment(\.colorScheme)`) for dark mode
- **Adaptive layouts** (`GeometryReader`, `ViewThatFits`) for iPad/Mac Catalyst

### Performance

- **LazyVStack / LazyHStack** for long lists
- **.drawingGroup()** for complex custom graphics
- **@State vs @StateObject** — use @State for simple values, @StateObject for ObservableObject

---

## Cross-Platform Considerations

### Design Token Strategy

Maintain a single source of truth for tokens, exported to each platform:

```
tokens/
  tokens.json         ← Single source (Style Dictionary format)
  web/
    tokens.css        ← CSS custom properties
  ios/
    tokens.swift      ← Swift constants
  android/
    tokens.xml        ← Android resources
  rn/
    tokens.ts         ← TypeScript constants
```

Tools: **Style Dictionary** (Amazon), **Theo** (Salesforce), or **Token Transformer** (Figma Tokens plugin).

### Typography Cross-Platform

| Platform | System Font | Custom Font Loading |
|---------|-------------|---------------------|
| Web | `system-ui, sans-serif` | Google Fonts / self-hosted WOFF2 |
| iOS | SF Pro | Via `Info.plist` + asset catalog |
| Android | Roboto | Via `res/font/` directory |
| React Native | System default | `expo-font` or `react-native-vector-icons` |
| Flutter | Roboto (Android), SF Pro (iOS) | `pubspec.yaml` fonts section |

### Touch Target Minimum (all platforms)

| Platform | Minimum | Recommended |
|---------|---------|-------------|
| Web | 44×44px (WCAG) | 48×48px |
| iOS HIG | 44×44pt | 48×48pt |
| Android Material | 48×48dp | 56×56dp |
| Flutter | 48×48dp | 56×56dp |

---

**Avoid**: Platform-specific UI patterns on the wrong platform (e.g., iOS bottom sheet UX on Android). Ignoring system font scaling. Hard-coding colors without tokens. Building complex navigation before defining deep link structure.
