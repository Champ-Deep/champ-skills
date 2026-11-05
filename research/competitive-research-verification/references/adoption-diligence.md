# Adoption diligence: "open-source" claims and market-exit signals

Depth for two checks that decide an adopt-versus-build call. Both are cheap and both
are routinely skipped.

## 1. "Open-source X" means: which layer of X is in the repo?

Connector platforms, scraping services, SDK vendors and hosted APIs all publish an
open-source repo. The repo's LICENSE file answers what we may do; the git tree answers
what we get. Read both, per candidate, before ranking. A MIT repo can be a client that
calls a closed cloud, which is the single most common way this category misleads.

Run once per candidate and read the tree listing, not the description:

```bash
gh api repos/<owner>/<repo> --jq '[.spdx_id, .pushed_at, .archived, .stargazers_count] | @tsv'
gh api repos/<owner>/<repo>/git/trees/HEAD?recursive=1 --jq '.tree[].path' > /tmp/tree.txt
# what actually implements the thing we are adopting:
grep -Ei 'oauth|connect|provider|connector' /tmp/tree.txt | head -30
```

| Claim on the marketing page | What the tree shows | Adopt? |
|---|---|---|
| MIT, "1000+ integrations" | SDK and types only: zero connector implementations, zero OAuth code, no server package | No: the integrations live in their cloud |
| "Open source" | LICENSE file present, no `src/`/`lib/` at all | No: licence without source |
| Community edition | repo `archived: true`, changelog announces closed source | No: the OSS line is dead |
| Open source | LICENSE present but bars commercial or hosted use (SSPL-ish, 