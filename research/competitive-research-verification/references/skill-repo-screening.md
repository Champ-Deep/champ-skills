# Screening a candidate skill or tool repo

Use this whenever a third-party skill, plugin or tool repo is a candidate for adoption: the
screening phase that runs before any fan-out and before any install.

Runs before any fan-out and before any install. Everything here is read-only on a scratch
clone; nothing in a candidate repo executes until its scripts clear the security surface below
and Deep has approved adoption.

## 1. Clone shallow, then measure the file surface

```bash
git clone --depth 1 <url> "$BH_AGENT_WORKSPACE/eval/<name>"
du -sh <clone>
find <clone> -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head
find <clone> -name SKILL.md -o -name 'CHANGELOG*' -o -name 'LICENSE*' | head -40
```

A README cannot be run. The clone costs seconds and hands over the gates, the hooks, the
churn history and the file census that ranking depends on. Read the changelog for major
versions: an upstream with several in a few months means anything we pin goes stale fast.

## 2. Security surface, before executing anything in it

```bash
grep -rhoE "https?://[a-zA-Z0-9._-]+" <clone> --include='*.mjs' --include='*.js' | sort | uniq -c | sort -rn
grep -rlE "child_process|execSync|spawn\(|fetch\(|eval\(|new Function|process\.env\.[A-Z_]+" <clone> --include='*.mjs' --include='*.js'
grep -rn -iE "<!--.*(agent|assistant|ignore|curl|bash|install)" <clone>/*/README.md
```

Expected hosts are the vendor's own: font and CDN hosts, stock-photo or icon APIs,
127.0.0.1. Any other host, any key-shaped env var, or an install command hidden in an HTML
comment is a named finding in the report, and the script does not run until Deep approves it.
Also read the frontmatter of every SKILL.md for hooks: hooks fire in Claude Code only, so any
gate they wire up must be invoked by command in our briefs.

## 3. Licence and bundled assets

```bash
gh api repos/<owner>/<repo> --jq '{license:.license.spdx_id, pushed:.pushed_at[0:10], stars:.stargazers_count}'
find <clone> -iname 'LICENSE*' -o -iname 'NOTICE*' -o -iname '*credits*.json' -o -iname '*third*party*'
```

`license: null` means no licence: adoption, vendoring and redistribution are Deep's call, not
ours. Then census what ships inside. Icon packs, logo packs and photographs carry their own
licences and trademark marks, and adopting on Deep's machine is a different act from copying
them into our tree: `champ-skills` is public, so an asset-heavy candidate is installed from
upstream pinned and never vendored.

## 4. Version state of the copy we already hold

```bash
diff -u <our-local-copy> <clone>/<same-file> | head -40
```

A local copy proves nothing about currency. Upstreams park old versions in a retired-versions
repo, so a file in our tree can be an archived release that reads as canonical, and an
untracked copy has no version at all. Name the release we actually hold before quoting its
rules.

## 5. Conflict table against standing conventions

One row per conflict, each row ending in a scope split or a no.

| Candidate rule | Our standing rule | Verdict |
|---|---|---|
| builds from its own starter and kit, forbids edits | one mandated component source for client pages | split: the kit only where the mandate does not bind |
| forbids violet in any page design | a house brand's primary is purple | split: candidate owns structure, palette stays brand |
| bans scroll-in reveals | the motion style asks for scroll beats | trial: run its allowed motion on one section before adopting |
| gate wired to a frontmatter hook | our lanes run on Hermes | name the invoking command in every brief |
| bundles trademark logo packs and share-alike photos | our skills repo is public | install from upstream, never vendor |

A conflict never resolves to silence: either the split is written into the adoption, or the
candidate does not go in.

## 6. Run its key-free gates on a build we already own

```bash
node <clone>/<skill>/scripts/<linter>.mjs <owned-page.html>
node <clone>/<skill>/scripts/<checker>.mjs index.html --quick --widths 1440,390 \
  --profile .eval/chrome --page <kind>
```

The cheapest deciding evidence there is: our own artifact, seconds, no key, no child agents.
Pick an owned build close to the candidate's intended use. Then split the output before you
quote it: findings that encode the candidate's house style, its grid, its banned motion, its
palette rules, against universal defects, clipped text, contrast, overflow, missing label,
broken focus. Quote both numbers, because a raw FAIL count from a style gate mostly measures
distance from its house style, and reporting it whole reads as "our build is broken" when the
build is fine and the styles simply differ.
