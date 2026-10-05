---
name: optional-input-degradation
description: "Use when an optional or external input can be absent."
tags: [resilience, backends, adapters, error-handling, tenancy, testing]
related_skills: [adapter-seam-extension, verification-gate-integrity]
---

# Optional input degradation

## The rule

**An optional input that can be absent must degrade to the honest unknown. It must never
propagate, because the caller cannot tell the difference between "this enrichment failed"
and "the request failed".**

Every user-visible path treats those two as identical: a 500 and an empty company both mean
the visitor sees nothing. So a guard missing upstream destroys the thing downstream was
built to deliver.

## The shapes it takes

The same bug wears six costumes. Check each call site against all of them:

| Input | Degrades to |
|---|---|
| Identity / enrichment provider | `None`, visitor unknown, rep told to confirm |
| Model provider | empty answer, which the caller already treats as a refusal |
| Tenant / org slug on a request | not "any tenant", never a fallback or default |
| Related record (client, campaign, rep) | degraded response, not a 500 |
| Unconfigured credential | the local fallback path, chosen by a real check |
| Inherited environment variable | unset it, so one declared source of truth remains |

The tenant row hides best: a hardcoded slug, or a "first org in the database" fallback,
returns another customer's answers and looks like it works.

## Guard the boundary, not the type

A check like `if not self.api_key: ...` is only true when the credential is *absent*. A key
inherited from an unrelated parent process is present, valid-looking and rejected by the
remote, so the guard passes and the exception escapes from a layer that believed it was
covered. Wrap the call:

```python
try:
    return resolver.company(ip)
except Exception:
    log.warning("company resolution failed; continuing as unknown", exc_info=True)
    return None
```

Broad `except` is correct here and narrow `except` is a bug: the failure modes you cannot
enumerate (DNS, TLS, timeouts, 4xx, 5xx, schema drift) are the majority, and the whole
point is that none reach the user.

**Never let the exception cross the endpoint.** If a handler can raise, that is the defect,
not bad luck upstream.

## A comment is a claim, not a guard

`# Any transport failure propagates; the caller treats an exception the same as an empty
answer` describes intended behaviour. With no `try` present the code does not do it, and the
comment actively misleads the next reader. When a comment asserts a degradation path, grep
for the construct that implements it before believing it.

## Pin it with a stub that raises

A test with a healthy stub cannot catch this. The stub must misbehave the way production
does:

```python
class BrokenResolver:
    def company(self, ip): raise RuntimeError("HTTP Error 401: Unauthorized")

def test_a_failing_resolver_leaves_the_visitor_unknown():
    assert identify("198.51.100.7", BrokenResolver(), cloud=None) is None
```

Cover unreachable, unauthorised and malformed separately. They take different paths through
retry and parsing code even when the outcome is the same.

**Never log the provider's error body.** A provider can echo the credential back inside it.
Log the status code only.

## Prove it from an empty state

A suite that only ever runs against pre-seeded data never executes the absent-input path, so
it stays green through every one of these defects. Stand the whole thing up once against an
empty database and drive the real flow. That single run surfaces this class; unit tests
alone will not.

## Start processes from a declared environment

A server launched from a desktop app or shell inherits that process's environment, so a
credential belonging to a different system arrives configured and fails at request time.
Unset provider keys in the launcher script so the `.env` file is the only source, and say
plainly at startup when no key is present rather than failing later inside a request.

## Pitfalls

- **Guarding on presence instead of wrapping the call.** Passes on an invalid inherited key.
- **A comment describing a `try` block that does not exist.** Grep for the construct.
- **A fallback that answers for the wrong tenant.** Silent cross-tenant data, worst outcome.
- **Logging the remote error body.** Leaks the credential you were protecting.
- **Testing only with healthy stubs.** The absent path stays unexercised and green.
- **Conflating "degraded" with "empty".** An absent enrichment is an *unknown*; a genuinely
  free resource is a *fact*. Only the second may be reported as certainty.
