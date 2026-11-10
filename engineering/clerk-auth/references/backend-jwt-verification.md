# Verifying user bearer tokens on a backend (JWT + JWKS)

Provider-agnostic: the same code verifies Better Auth, Keycloak or Clerk tokens
once the issuer publishes a JWKS. The pattern has two halves, one check
function and one env contract. Everything else follows from those.

## 1. One verifier for every caller

One function decides who is calling: API keys first (a workspace or tenant
token, cheap, no network), then JWTs. Both the REST layer and any MCP SDK
bearer middleware call it, so there is exactly one place where a token can be
turned into a workspace id. Two verifiers drift: the SDK one accepts a token the
REST dependency rejects, and the difference surfaces as a bug in an unrelated
endpoint.

```python
def check(token):
    w = db.workspace_for_key(token)          # long-lived key, no network
    if w:
        return AccessToken(token=token, client_id="api_key", scopes=[], subject="ws:" + w["id"])
    if not enabled() or not token or token.count(".") != 2:
        return None                          # fail closed when not configured
    claims = verify_jwt(token)
    if not claims or not allowed(claims):
        return None
    return AccessToken(token=token, client_id=claims.get("azp", ""), scopes=[],
                       expires_at=claims.get("exp"), subject=claims["sub"])
```

Subjects carry the tenant: `ws:<id>` for an API key, the raw user id for a JWT.
Map both to a workspace through one helper, so an API key row and a signed-in
user row are never interchangeable (a marker row for a user id must not be a
usable API key).

## 2. The env contract

| Env | Meaning | Default |
|---|---|---|
| `..._AUTH_ISSUER` | Auth server base URL; required, and its presence is what switches the service into OAuth mode | unset = API keys only |
| `..._AUTH_JWKS` | JWKS URL | `<issuer>/jwks` |
| `..._AUTH_AUDIENCE` | Required `aud` claim | issuer (Better Auth's default) |
| `..._PUBLIC_URL` | This service's own base URL, for the protected-resource document | required in OAuth mode |
| `..._ALLOWED_USERS` | Who may sign in: user ids or emails, `*` for all verified users | unset = nobody |

Keep the prefix uniform across services; only the issuer and public URL change
per deployment. The allow-list is the invite model: on a self-serve app it is
what makes open sign-up safe to ship, and it is decided together with the
provider, not bolted on later.

## 3. verify_jwt

- Read `kid` from the **unverified** header first, then fetch only that key.
- Look the key up in a TTL cache (an hour is plenty; keys rarely rotate). An
  unknown `kid` forces one refresh, which is how a rotation heals itself.
- `jwt.decode(token, key, algorithms=[...], issuer=..., audience=..., options={"require": ["sub", "exp"]})`.
  Fetching JWKS per request does not survive a rotation under load, and a cache
  with no refresh path pins you to a revoked key forever.
- Any failure returns `None`: bad signature, wrong issuer, wrong audience,
  expired, and the JWKS host being unreachable (wrap `URLError`, `TimeoutError`
  and `ValueError` in the same except). Fail closed. A network blip that
  propagates turns into a 500 on every request instead of a 401.

Pitfalls worth one line each:

- Derive the algorithm from the key object (`key.algorithm_name`) rather than a
  pinned constant: a provider that rotates between EdDSA and RS256 otherwise
  fails with an algorithm-mismatch error that reads like a bad signature.
  Never trust the token header's own `alg` claim; that is the classic
  algorithm-confusion hole.
- Never take `iss`/`aud` from the token to decide what to verify against. The
  issuer env is the trust anchor; a token naming its own issuer authorizes
  itself.
- If the service exposes MCP as well, its
  `/.well-known/oauth-protected-resource` document must point at the issuer so
  clients know where to sign in.
- An API key is a bearer credential too: log its workspace on rejection, never
  the key material.

## 4. Keys in the environment

Read secrets out of the env file with `grep '^KEY=' file | cut -d= -f2-` and
pass them inline (`KEY="$(grep ...)" cmd`), never `source` the file. Sourcing
loads every unrelated variable in it into whatever shell or cron runs next, so
the same script behaves differently depending on how it was launched.

## 5. Deploy check: three calls, not a green suite

Local unit tests prove the crypto; the integration proves wiring. Run it
against the deployed URL:

1. Valid user bearer token -> 2xx
2. Forged, expired or wrong-audience token -> 401
3. API key -> 2xx

Report the three status codes. A verifier only exists end to end, and this is
the difference between a working login and a service that rejects everything
or accepts anything.
