# Clerk on Next.js (App Router)

Self-contained walkthrough for a Next.js project with an `app/` directory.
Code is TypeScript; drop type annotations for plain JS.

## 1. Install the SDK

```bash
npm install @clerk/nextjs
```

## 2. Environment variables

Create or edit `.env.local`:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxx
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxx
```

Next.js needs both: the publishable key for the client, the secret key for
server-side calls. The `NEXT_PUBLIC_` prefix is what exposes the first one to
the browser. The secret key has no prefix and stays server-only.

Add `.env.example`:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
```

Confirm `.gitignore` ignores `.env*.local`. Add it if missing. A committed
`sk_` key is a credential leak: rotate it in the Clerk dashboard immediately
if it ever lands in git history.

## 3. Add the middleware

Clerk's middleware is what makes `auth()` work anywhere in the app. Without
it, server code that calls `auth()` throws.

Create the file at the project root, or inside `src/` if the project uses a
`src/` directory.

- **Next.js 15 and earlier:** name it `middleware.ts`.
- **Next.js 16 and later:** name it `proxy.ts`. The contents are identical;
  only the filename changed.

Check the `next` version in `package.json` to pick the right name.

```ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

// Routes that require a signed-in user. Everything else stays public.
const isProtectedRoute = createRouteMatcher([
  "/dashboard(.*)",
  "/admin(.*)",
]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    // Skip Next.js internals and static files
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    // Always run for API routes
    "/(api|trpc)(.*)",
  ],
};
```

By default Clerk protects nothing. You opt routes in. Edit the
`createRouteMatcher` list to match the routes this tool wants private. If the
whole tool should require login, use `["/(.*)"]` but leave the sign-in routes
reachable (Clerk handles that automatically).

## 4. Wrap the app in ClerkProvider

Edit `app/layout.tsx`. Wrap the whole tree and add auth UI to the layout so it
appears on every page:

```tsx
import type { Metadata } from "next";
import {
  ClerkProvider,
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/nextjs";

export const metadata: Metadata = { title: "ChampLens" };

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <header className="app-header">
            <span className="logo">ChampLens</span>
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
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
```

## 5. Read the user in server and client code

**Server components / route handlers / server actions:**

```tsx
import { auth, currentUser } from "@clerk/nextjs/server";

export default async function DashboardPage() {
  const { userId } = await auth();      // null if signed out
  const user = await currentUser();     // full user object, or null
  return <div>Hello, {user?.firstName}</div>;
}
```

`auth()` is also how you enforce protection inside a specific server action or
API route: `const { userId } = await auth(); if (!userId) { ... }`.

**Client components:**

```tsx
"use client";
import { useUser } from "@clerk/nextjs";

export function Profile() {
  const { isLoaded, isSignedIn, user } = useUser();
  if (!isLoaded) return <div>Loading...</div>;
  if (!isSignedIn) return <div>Please sign in.</div>;
  return <div>Hello, {user.firstName}</div>;
}
```

## 6. Optional: dedicated sign-in / sign-up pages

The modal buttons from step 4 are enough for most internal tools. If you want
real routes instead, create catch-all pages:

`app/sign-in/[[...sign-in]]/page.tsx`:

```tsx
import { SignIn } from "@clerk/nextjs";
export default function Page() {
  return <SignIn />;
}
```

`app/sign-up/[[...sign-up]]/page.tsx`:

```tsx
import { SignUp } from "@clerk/nextjs";
export default function Page() {
  return <SignUp />;
}
```

Then point Clerk at them by adding to `.env.local`:

```
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
```

## Verify

1. `npm run dev` starts clean.
2. A protected route signed-out redirects to sign-in.
3. Sign up → signed in → `<UserButton>` shows.
4. A server component calling `auth()` does not throw (proves the middleware
   file is named and placed correctly).
5. `git status`: no `.env.local` staged, no `sk_` key in the diff.

## Deploy

Add `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` to the host
(Vercel/Netlify) for production and preview, then redeploy. Add the production
domain to the Clerk application's allowed domains. The single most common
production failure is a missing `CLERK_SECRET_KEY` on the host: the build
succeeds, then every request 500s.
