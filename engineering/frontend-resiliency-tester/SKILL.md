---
name: frontend-resiliency-tester
description: React frontend resiliency and edge-case testing. Generates layered test suites (component, integration, E2E) using Vitest + React Testing Library and Playwright. Covers input validation, boundary testing, error boundaries, failure resilience, responsive/accessibility, and state management edge cases. Use whenever the user mentions frontend testing, React testing, edge cases, stress testing, resiliency, UI stability, test coverage, error boundaries, boundary conditions, accessibility testing, responsive testing, or race conditions. Also trigger for "test my component", "find edge cases", "stress test this UI", "make this bulletproof", "regression tests", or validating that a React frontend handles failure gracefully. MANDATORY TRIGGER for any React/frontend testing or QA task.
---

# Frontend Resiliency Tester

Generate layered, production-grade test suites for React + TypeScript frontends. This skill produces tests that catch real bugs — not just happy-path confirmations.

## Stack Assumptions

- **React 19** + **TypeScript** (strict mode)
- **Tailwind CSS** for styling
- **React Query (TanStack Query)** for server state
- **Vitest** + **React Testing Library** for unit/integration
- **Playwright** for E2E
- Libraries: `clsx`, `tailwind-merge`, `class-variance-authority` (cva)

If the user's stack differs, adapt — but default to the above.

## Core Philosophy

> Test the contract, not the implementation. If a refactor breaks your tests but not your app, the tests were wrong.

Before writing any tests, read the **React + TypeScript Patterns Reference** at `references/react-ts-patterns.md` for the coding standards these tests are designed to enforce.

---

## Test Layers

### Layer 1: Component Tests (Vitest + RTL)

Test each component in isolation. One responsibility per component = one focused test file.

**What to test:**
- Props contract: required props render correctly, optional props use defaults, invalid props are handled
- TypeScript safety: ensure typed props catch bugs at compile time (no `any` leaks)
- User interactions: clicks, inputs, form submissions
- Conditional rendering: loading, error, empty, success states
- Accessibility: ARIA attributes, keyboard navigation, focus management

**What NOT to test:**
- Internal state values directly (test the rendered output instead)
- Implementation details like hook internals
- Tailwind class names (test visual behavior, not class strings)

**Pattern — Early return testing:**
```typescript
// Components should use early returns for loading/error/empty states
// Test each branch independently:
it('shows spinner while loading', () => { ... });
it('shows error message on failure', () => { ... });
it('shows empty state when no data', () => { ... });
it('renders user profile on success', () => { ... });
```

**Pattern — Controlled vs Uncontrolled inputs:**
```typescript
// Controlled: test value + onChange contract
it('transforms input to uppercase on change', () => {
  render(<ControlledInput />);
  fireEvent.change(screen.getByRole('textbox'), { target: { value: 'hello' } });
  expect(screen.getByRole('textbox')).toHaveValue('HELLO');
});

// Uncontrolled: test submit behavior, not intermediate state
it('submits the form value on click', () => {
  render(<UncontrolledForm onSubmit={mockFn} />);
  fireEvent.change(screen.getByRole('textbox'), { target: { value: 'test' } });
  fireEvent.click(screen.getByRole('button', { name: /submit/i }));
  expect(mockFn).toHaveBeenCalledWith('test');
});
```

### Layer 2: Custom Hook Tests

Custom hooks (`use*`) encapsulate reusable logic. Test them via `renderHook` from RTL.

**What to test:**
- Return value shape and types
- State transitions (initial → loading → success/error)
- Dependency changes trigger re-execution
- Cleanup on unmount (abort controllers, subscriptions)

**Pattern — useFetch hook:**
```typescript
it('returns loading true initially, then data on success', async () => {
  const { result } = renderHook(() => useFetch<User[]>('/api/users'));
  expect(result.current.loading).toBe(true);
  await waitFor(() => expect(result.current.loading).toBe(false));
  expect(result.current.data).toHaveLength(3);
  expect(result.current.error).toBeNull();
});
```

### Layer 3: Integration Tests

Test feature slices — how components, hooks, and queries work together.

**What to test:**
- Feature flows: search → filter → select → action
- React Query integration: cache invalidation after mutations
- State lifting: parent-child state coordination
- Compound component composition (Card + Card.Body + Card.Footer)
- Error boundaries catching child errors

**Pattern — React Query mutation + cache invalidation:**
```typescript
it('refreshes user list after deleting a user', async () => {
  render(<UserDashboard />, { wrapper: QueryWrapper });
  // Wait for initial load
  await screen.findByText('Alice');
  // Delete
  fireEvent.click(screen.getByTestId('delete-alice'));
  // Verify refetch happened and Alice is gone
  await waitFor(() => expect(screen.queryByText('Alice')).not.toBeInTheDocument());
});
```

### Layer 4: E2E Tests (Playwright)

Test critical user journeys end-to-end in a real browser.

**What to test:**
- Authentication flows (login → dashboard → logout)
- Form submissions with validation feedback
- Navigation and routing
- Responsive behavior at mobile/tablet/desktop breakpoints
- Optimistic UI updates (useOptimistic) — verify instant feedback then server sync

**Pattern — useOptimistic verification:**
```typescript
test('like button updates instantly then syncs', async ({ page }) => {
  await page.goto('/posts/1');
  const likeCount = page.getByTestId('like-count');
  await expect(likeCount).toHaveText('42');
  await page.getByRole('button', { name: /like/i }).click();
  // Optimistic: instant
  await expect(likeCount).toHaveText('43');
  // After server sync: still 43 (or reverts on error)
});
```

---

## Edge Case Categories

When generating tests, always cover these categories:

### 1. Input Validation & Boundaries
- Empty strings, null, undefined
- Extremely long strings (10K+ characters)
- Special characters: `<script>`, SQL injection patterns, unicode, emoji
- Number boundaries: 0, -1, MAX_SAFE_INTEGER, NaN, Infinity
- Date edge cases: leap years, timezone boundaries, epoch

### 2. State Management Edge Cases
- Redundant state detection: verify derived values aren't stored separately (test that `fullName` is always `${firstName} ${lastName}`)
- Rapid state updates (debounce/throttle behavior)
- State during unmount (no "update after unmount" warnings)
- useReducer action exhaustiveness (all action types handled)
- Local vs global state: ensure UI state (dropdowns, modals) isn't polluting global stores

### 3. Async & Network Failures
- API timeout (>30s)
- Network offline / intermittent
- Race conditions: rapid fire requests, stale closures
- Retry behavior (React Query retries)
- Abort on unmount
- 4xx and 5xx responses with and without error bodies

### 4. Responsive & Layout
- Viewport: 320px (small mobile) → 2560px (ultrawide)
- Container overflow with dynamic content
- Text truncation and wrapping
- Image loading failures (broken src)
- CSS class conflicts when using `cn()` (tailwind-merge resolution)

### 5. Accessibility
- Screen reader announcements for dynamic content
- Focus trap in modals
- Keyboard navigation (Tab, Escape, Enter, Arrow keys)
- Color contrast ratios (WCAG AA minimum)
- ARIA labels on interactive elements

### 6. Component Pattern Resilience
- Compound components: missing sub-components (e.g., `<Card>` without `<Card.Body>`)
- Render props: null/undefined return
- Generic List component: empty array, single item, 10K items
- React 19 `use()`: promise rejection, slow resolution
- `ref` as prop (React 19): verify ref forwarding without forwardRef
- `useActionState`: form submission errors, pending state, re-submission

---

## Test Generation Workflow

1. **Analyze** the component/feature code
2. **Identify** which test layers apply
3. **Map** edge case categories to the specific code
4. **Generate** test files following naming conventions:
   - `ComponentName.test.tsx` — component tests
   - `useHookName.test.ts` — hook tests
   - `feature-name.integration.test.tsx` — integration tests
   - `feature-name.e2e.spec.ts` — Playwright E2E
5. **Include** setup utilities (mock providers, query wrappers, test factories)
6. **Output** a test coverage summary showing what's covered per edge case category

## Naming Conventions (Mirrors Codebase)

Follow the same conventions the codebase uses:
- Components: **PascalCase** (`UserProfileCard.test.tsx`)
- Hooks: **use prefix** (`useAuth.test.ts`)
- Variables in tests: **camelCase**, descriptive (`const mockUserResponse = ...`)
- Constants: **SCREAMING_SNAKE_CASE** (`const MAX_RETRY_COUNT = 3`)
- Booleans: **is/has/can prefix** (`isLoading`, `hasError`, `canEditPost`)
- Test descriptions: plain English, behavior-focused ("shows error when email is invalid")

## File Structure

Output tests mirroring the feature-based folder structure:
```
src/
  features/
    users/
      components/
        UserCard.test.tsx
        UserForm.test.tsx
      hooks/
        useUsers.test.ts
      __integration__/
        user-dashboard.integration.test.tsx
  shared/
    components/
      Button.test.tsx
      Modal.test.tsx
    hooks/
      useFetch.test.ts
      useDebounce.test.ts
  e2e/
    auth-flow.e2e.spec.ts
    user-management.e2e.spec.ts
```

## React Query Test Utilities

Always provide a query wrapper for tests involving React Query:

```typescript
// test-utils/query-wrapper.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

export function createQueryWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
```

## References

- **React + TypeScript patterns:** See `references/react-ts-patterns.md` for the full coding standards these tests validate — component design, TypeScript usage, state management, custom hooks, naming, folder structure, React Query patterns, Tailwind best practices, React 19 features, and component patterns.
