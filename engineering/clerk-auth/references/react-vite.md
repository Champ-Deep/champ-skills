# Clerk on React + Vite

Self-contained walkthrough. This is the stack ChampUTM and ChampLens use, so
it is the most battle-tested path. Code is TypeScript; for plain JS drop the
type annotations.

If the project is Create React App instead of Vite, every step is identical
except the env var prefix: CRA uses `REACT_APP_CLERK_PUBLISHABLE_KEY` and
`process.env.REACT_APP_...` instead of `import.meta.env.VITE_...`.

## 1. Install the SDK

```bash
npm install @clerk/clerk-react
```

(Use `pnpm add` / `yarn add` / `bun add` if the project's lockfile says so.)

## 2. Environment variables

Create or edit `.env.local` in the project root:

```
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxx
```

A pure React/Vite single-page app needs only the publishable key. The secret
key never goes in frontend code, because anything in a Vite bundle is public.

Create `.env.example` next to it so the next developer knows the contract:

```
VITE_CLERK_PUBLISHABLE_KEY=
```

Confirm `.gitignore` ignores local env files. Add this block if missing:

```
.env.local
.env*.local
```

## 3. Wrap the app in ClerkProvider

Edit the entry file (`src/main.tsx` or `src/main.jsx`). Read the publishable
key from env, fail loudly if it is missing, and wrap the root component:

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { ClerkProvider } from "@clerk/clerk-react";
import App from "./App";
import "./index.css";

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing VITE_CLERK_PUBLISHABLE_KEY in .env.local");
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/">
      <App />
    </ClerkProvider>
  </React.StrictMode>
);
```

The explicit missing-key check matters. Without it, Clerk fails with a vague
runtime error and the cause is not obvious. The throw makes the problem
self-explanatory.

## 4. Sign-in / sign-up / user-button UI

Clerk ships prebuilt components. The four you almost always want:

- `<SignedIn>` — renders children only when the user is signed in.
- `<SignedOut>` — renders children only when signed out.
- `<SignInButton>` / `<SignUpButton>` — open Clerk's hosted auth modal/page.
- `<UserButton>` — the avatar dropdown (profile, sign out).

A typical header:

```tsx
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/clerk-react";

function Header() {
  return (
    <header className="app-header">
      <span className="logo">ChampUTM</span>
      <nav>
        <SignedOut>
          <SignInButton mode="modal" />
          <SignUpButton mode="modal" />
        </SignedOut>
        <SignedIn>
          <UserButton afterSignOutUrl="/" />
        </SignedIn>
      </nav>
    </header>
  );
}
```

`mode="modal"` keeps the user on the page. Drop it to use Clerk's hosted
full-page flow instead.

To read the user in code, use the hooks:

```tsx
import { useUser, useAuth } from "@clerk/clerk-react";

function Profile() {
  const { isLoaded, isSignedIn, user } = useUser();
  if (!isLoaded) return <div>Loading...</div>;
  if (!isSignedIn) return <div>Please sign in.</div>;
  return <div>Hello, {user.firstName}</div>;
}
```

## 5. Protect routes

Decide the gating model. Two common ones:

### Option A: gate the whole app

If the entire tool should require login, wrap everything below the header:

```tsx
import { SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";

function App() {
  return (
    <>
      <Header />
      <SignedIn>
        <MainApp />
      </SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
}
```

### Option B: per-route protection with React Router

If some routes are public (a marketing landing page, a free public generator)
and others are private, protect only the private routes. Create a guard:

```tsx
import { SignedIn, SignedOut, RedirectToSignIn } from "@clerk/clerk-react";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  return (
    <>
      <SignedIn>{children}</SignedIn>
      <SignedOut>
        <RedirectToSignIn />
      </SignedOut>
    </>
  );
}
```

Use it in the route tree:

```tsx
<Routes>
  <Route path="/" element={<PublicHome />} />
  <Route
    path="/dashboard"
    element={
      <ProtectedRoute>
        <Dashboard />
      </ProtectedRoute>
    }
  />
</Routes>
```

ChampUTM uses this split: the public link generator stays open, the analytics
and saved-campaign features sit behind `ProtectedRoute`. That "free public
feature + premium gated feature" pattern is worth copying for tools that want
a public hook.

### Optional: dedicated sign-in pages

If you prefer real routes over modals, render Clerk's full components on their
own routes:

```tsx
import { SignIn, SignUp } from "@clerk/clerk-react";

<Route path="/sign-in/*" element={<SignIn routing="path" path="/sign-in" />} />
<Route path="/sign-up/*" element={<SignUp routing="path" path="/sign-up" />} />
```

## Verify

1. `npm run dev` starts clean, no Clerk errors in the browser console.
2. Signed out, a protected route bounces to sign-in.
3. Sign up → land signed-in → `<UserButton>` avatar shows.
4. Sign out → back to signed-out state.
5. `git status`: `.env.local` is not staged.

## Deploy

Add `VITE_CLERK_PUBLISHABLE_KEY` to the host (Vercel/Netlify) env settings for
production and preview, then redeploy. In the Clerk dashboard, add the
production domain under the application's allowed domains so Clerk accepts
requests from it.
