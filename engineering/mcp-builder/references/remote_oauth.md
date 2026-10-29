# Remote MCP over OAuth (Clerk)

How a remote MCP server gets sign-in instead of only shared bearer keys, and how
to test it when no real IdP exists on the machine.

## The discovery chain a client walks

Before any tool call, an MCP client resolves three documents. Serve each from the
server itself so a self-hosted deployment needs no extra service:

1. `GET /.well-known/oauth-protected-resource` (and the `/mcp`-suffixed variant,
s   because clients ask at the path they called) -> `{authorization_servers: [<issuer>]}`.
   Reachable without auth, or the whole chain fails on the first hop.
2. `GET <issuer>/.well-known/oauth-authorization-server` -> endpoints: `authorization_endpoint`,
   `token_endpoint`, `registration_endpoint`, `jwks_uri`, `code_challenge_methods_supported`.
3. Dynamic client registration POSTs to `registration_endpoint`, gets a `client_id`,
   then PKCE (S256) against the authorization endpoint.

## Where the identity provider fits

- The IdP (Clerk) lives at its own issuer URL. Enable **dynamic client registration**
  on the instance, or step 3 stalls with no `registration_endpoint`.
- The MCP server validates tokens itself, at the protected route, rather than
  proxying: fetch the issuer's JWKS and check signature, `iss`, `aud`, `exp` on the
  bearer token. `aud` accepts the server's own public URL, its `/mcp` path, or the
  client id, because deployments disagree about which one the IdP stamps.
- The user directory is NOT the allowlist. Map IdP subject (`sub`) to an internal
  workspace explicitly, and refuse subjects not on the configured list. A token
  that verifies proves authentication, not authorization.
- Keep bearer API keys working on the same route alongside OAuth. Automation and
  human clients then share one endpoint and one tool list.

## Testing without a real IdP

Fake the issuer inside the test process (an ASGI app serving the two well-known
docs, a registration endpoint, and a token endpoint that signs a JWT with a
generated RSA key whose JWKS it also serves). The assertions that matter:

- no token -> 401 with the resource metadata URL in `WWW-Authenticate`;
- a token signed by someone else / wrong `iss` / wrong `aud` / expired -> 401;
- an allowed subject -> 200 and the full tool list;
- a valid but unlisted subject -> refused;
- a bearer API key -> still 200.

Name this in the report as a fixture: the handshake shape is proven, real sign-in
at the live IdP is not. Ship a `scripts/` probe that runs the same chain against a
locally started server so the live path can be checked the moment credentials exist.

## Pitfalls

- Serving only the resource document and forgetting the path-suffixed one: some
  clients request `/.well-known/oauth-protected-resource/mcp` first.
- Validating the token but never checking `aud` or the allowlist: any token minted
  for any other app in the tenant gets in.
- Assuming sign-ups are open. Restrict registration at the IdP, then allowlist;
  an open sign-up plus a token check is an open door with a lock on the inside.
