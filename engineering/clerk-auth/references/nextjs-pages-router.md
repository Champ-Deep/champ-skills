# Clerk on Next.js (Pages Router)

For older Next.js projects that use a `pages/` directory instead of `app/`.
Most new tools use App Router; reach for this file only if `pages/` is the
real structure.

## 1. Install

```bash
npm install @clerk/nextjs
```

## 2. Environment variables

Same as App Router. In `.env.local`:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxx
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxx
```

Add `.env.example` with the same keys empty, and confirm `.env*.local` is
gitignored.

## 3. Middleware

Identical to App Router. Create `middleware.ts` (Next 15 and earlier) or
`proxy.ts` (Next 16+) at the project root or in `src/`:

```ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher(["/dashboard(.*)"]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect();
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

## 4. Wrap the app

Edit `pages/_app.tsx`:

```tsx
import type { AppProps } from "next/app";
import { ClerkProvider } from "@clerk/nextjs";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ClerkProvider {...pageProps}>
      <Component {...pageProps} />
    </ClerkProvider>
  );
}
```

## 5. Auth UI

The components are the same: `<SignedIn>`, `<SignedOut>`, `<SignInButton>`,
`<SignUpButton>`, `<UserButton>`. Put them in a shared layout or header
component rendered by your pages.

```tsx
import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
} from "@clerk/nextjs";

export function Header() {
  return (
    <header>
      <SignedOut>
        <SignInButton mode="modal" />
        <SignUpButton mode="modal" />
      </SignedOut>
      <SignedIn>
        <UserButton afterSignOutUrl="/" />
      </SignedIn>
    </header>
  );
}
```

## 6. Read the user

**Client side:** `useUser()` and `useAuth()` hooks, same as everywhere.

**Server side** (`getServerSideProps`):

```tsx
import { getAuth } from "@clerk/nextjs/server";
import type { GetServerSidePropsContext } from "next";

export async function getServerSideProps(ctx: GetServerSidePropsContext) {
  const { userId } = getAuth(ctx.req);
  if (!userId) {
    return { redirect: { destination: "/sign-in", permanent: false } };
  }
  return { props: { userId } };
}
```

**API routes** (`pages/api/...`):

```tsx
import { getAuth } from "@clerk/nextjs/server";
import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { userId } = getAuth(req);
  if (!userId) return res.status(401).json({ error: "Unauthorized" });
  res.json({ userId });
}
```

## Verify and deploy

Same checklist as the App Router file: clean dev start, protected route
redirects when signed out, sign-up works, no env file staged in git, host env
vars set and a redeploy triggered.
