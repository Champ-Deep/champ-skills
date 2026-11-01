# Node and container-build gotchas for a resurrected repo

Read when a package that compiles locally fails on a runner or inside an image.
Each of these presents as a code error and is not one.

## 1. A build that times out downloading is a network path, not a dependency

Symptom: `npm ci` or a package fetch in a Dockerfile build crawls (one package
per 80 s) or dies with `ETIMEDOUT`, while the identical install on the host
finishes normally. The log's own package counter is the tell: if it moves, the
build is healthy and slow.

Cause: on a container bridge (OrbStack, Docker Desktop on macOS) Node 19+ uses
happy-eyeballs connection racing with a 250 ms family-autoselection timeout. An
unreachable IPv6 answer burns that budget on every connection attempt, so the
install stalls while the host, which resolves differently, succeeds.

Fix in the Dockerfile's build stage, because the build does not inherit your
shell and a shell `export` fixes only your terminal:

```dockerfile
FROM node:22-slim AS build
ENV NODE_OPTIONS=--network-family-autoselection-attempt-timeout=2000
RUN npm ci
```

A retry loop is the wrong fix: it re-rolls the same losing family. Widen the
timeout so the IPv4 fallback lands. Prove it by the download rate (hundreds of
packages in 30 s rather than one in 80 s), not by the build exiting zero once.
The same knob in your shell makes `npm` and `npx` behave alike on the host, so
host and runner stop diverging for the same reason.

## 2. Named versus default imports under `NodeNext`

A CommonJS dependency compiled under `NodeNext` resolves differently from an ESM
one, so `import x from 'pkg'` can bind the module object while
`import * as x` binds the namespace, and the reverse for a default-only export.
The failure is `x is not a function` at runtime on a type that passed `tsc`.
Check the package's own `exports` and `type` field before editing call sites;
widening the type or casting to `any` hides the mismatch without fixing it.

Also check the installed version: a transitive dependency pinned below the API
your code uses (a missing or renamed export) is a lockfile problem, not a code
problem, and a version bump or `npm dedupe` is the fix.

## 3. Local green is not runner green

- Install strictly from the lockfile (`npm ci`); `npm install` silently repairs a
  lockfile that only resolves on your platform, so CI passes on something the
  runner cannot reproduce.
- A lockfile with many `node_modules/<pkg>/<platform>` entries was resolved
  against one OS (esbuild and rollup ship around seventy platform-specific
  optional deps between them). Prove the install on the runner's image before
  believing any local result:
  `docker run --rm -v "$PWD":/w -w /w node:22-slim sh -c "node -v && npm ci"`
- A browser-driven suite ships as a library plus a separately downloaded binary.
  `npm ci` delivers the library only, so a fresh runner dies at
  `browserType.launch` with "Executable doesn't exist" while your machine, which
  downloaded it once, stays green. Install it as its own named CI step.

## 4. Run the widest suite once, and name the command

A path-filtered run is a report about those paths. Its pass count reads like a
branch-wide green and is not one, and a red test outside the filter is then a
test you never observed rather than one that passed. Run the unfiltered suite at
least once per branch and once on the baseline, compare totals, and put the
command next to every number you report. When two runs report different totals,
the first question is which command produced each, not which test broke.