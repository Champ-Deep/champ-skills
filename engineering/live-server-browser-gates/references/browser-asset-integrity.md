# Browser asset integrity before UI repair

Use when a built page passes typechecking but browser hydration stalls or reports a syntax error intermittently.

1. Capture the exact exception URL, line and column with CDP Runtime.exceptionThrown. Do not infer a React state bug from a page whose effects never mounted.
2. Save the actual browser response body for the named script, not only a later curl response. Compare byte lengths and the first differing offset, then run node --check on both bodies. A strict-prefix response that ends mid-string proves an asset-transfer problem, not invalid source code.
3. Preserve that evidence before restarting an owned preview. Never kill another lane's server or clear a shared build directory.
4. If Webpack development delivery is affected, test the framework's default development renderer on an unused port. Do not change application code or permanent bundler configuration to mask a preview-only transfer failure.
5. Repeat the entire route/state matrix on the replacement preview. Keep local production compilation separate from browser proof. A production auth gate refusing a development bypass is expected; never bypass it or fabricate a session.
6. Report which preview mode was verified, the failing asset evidence, and any remaining production-auth or device gaps.

For iterative UI checks, stop editing during capture. Keep fixture state reset per case, persist each completed batch, and enforce audit failures as well as console and geometry assertions in the script's exit condition.
