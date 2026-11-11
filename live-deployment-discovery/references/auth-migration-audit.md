# Auth and identity migration audit

Procedure for "were the signups transferred?", "can these people still
sign in?" after an auth vendor swap. Sections 1 to 5 are read-only and write
nothing to production: run them before repeating any migration claim, and before
telling a named person their account works. Section 6 is the write half, and it
runs only after the decision in section 5 has been approved with those counts
attached.

## 1. Establish which store is production

The deploy config states intent; match its ids against the platform's own list
before querying anything.

```bash
wrangler whoami                                   # which account the CLI is on
wrangler d1 list                                  # database name -> uuid
gh api repos/<o>/<r>/contents/worker/wrangler.jsonc?ref=main -q .content | base64 -d
```

The top-level (non-environment) `d1_databases[]` entry is production; each
`env.<name>` block carries its own database id and its own database. Querying a
database that merely looks like production yields a confident answer about
nothing, so check the id against `d1 list`, not the name.

## 2. Query the store

```bash
wrangler d1 execute <db> --remote --json --command "<sql>" 2>/dev/null \
  | python3 -c 'import sys,json; print(json.dumps(json.load(sys.stdin)[0]["results"], indent=1))'
```

The response is a list whose first element holds `results` and `meta`; unwrap it
instead of reading the raw dump. Read-only battery, table names adapted to the
schema in front of you:

| Question | Query shape |
|---|---|
| how many identities exist | `count(*)` on the user table |
| how many can sign in | `count(*)` of users with an `EXISTS` against the credential or provider-account table |
| method per person | join user to credential, `group by` provider id |
| imported versus freshly minted | `length(<pw>)` and `substr(<pw>,1,3)` per provider |
| has anyone actually used it | `count(*)` on the session table, joined back to email |
| the person the user named | `where lower(email) = lower('<literal>')` |
| retired or placeholder rows | count where the active flag is 0, or the email is a placeholder |
| rows still owned by the right person | join each asset to its owner and to the org holding the row; count owners who are not active members of that org (expect 0, and a non-zero is a data finding separate from the auth one) |
| who is actually locked out | split the no-credential set by method: password rows (locked until section 6 runs), provider-only rows (they link to the migrated identity on their first sign-in, so they are unproven rather than locked), and rows created after the cutover (already work) |

Never `select` the credential column itself. Length plus prefix separates
imported from native without printing anything secret, and the prefix is what
belongs in the report.

## 3. Prove the importer's absence in the repo

```bash
gh search code --repo <o>/<r> "<importer-stem>"
for r in $(git for-each-ref --format='%(refname)' refs/remotes refs/heads); do
  git grep -l "<importer-stem>" $r -- '*.mjs' '*.ts' '*.py' '*.sql' 2>/dev/null
done
```

One branch read proves nothing about the others. Absence on every ref, paired with
a store that holds identities but no credentials, is a single finding: the code
half shipped and the data half never ran.

## 4. Reconcile identities across the vendor's instances

List the vendor's users separately for each instance it exposes, development and
production being separate id spaces for the same person. Two shapes to check:

- the id stored on the live row came from the non-production instance, so it
  matches the vendor's format but resolves to nothing in production;
- the production id sits on a retired placeholder row while the active row
  carries the other one.

An id that matches the vendor's format is not the same as an id from the instance
that issued the credentials. When the vendor hands back both lists, diff them by
email, not by id.

## 5. Report

1. Findings table first: store queried, identities, sign-in-capable, the
   difference as a lockout count, sessions, and the named person's row verbatim.
2. The open decision as numbered options with one recommendation (import the old
   credentials, bind a sender so people can reset, hold), naming what each option
   needs from the user.
3. What was not exercised: the other environment, identities the vendor lists but
   the store does not, and any recovery path left disabled.

Carry the identifier the user typed alongside the record found. When the literal
does not exist, say so and print what does; normalizing it silently to a
near-match hides the wrong-person case the query existed to catch.

## 6. Carry the old credentials across (the write half)

Sections 1 to 5 establish who is locked out and what has to move. This is the
part that changes production, so it runs only after that decision is approved
with the counts attached.

1. **Take a restore point before anything else.** `wrangler d1 time-travel info
   <db>` prints the current bookmark; save it with the run. A bad import is
   restored from that bookmark, not repaired by hand afterwards.
2. **Get the export from the vendor's console and treat the file as a secret.**
   Password hashes are released only through an explicit user-export control,
   usually behind a step-up code mailed to the user (hand that gate over, see the
   `browser-agent-automation` skill). In Clerk the path is dashboard.clerk.com >
   app > instance > Configure > Instance (settings) > User exports; other vendors
   bury an equivalent under privacy or data settings. Store it mode 600 outside
   every repo, and check `gh repo view --json isPrivate,visibility` first: a
   public repo is the normal case for these projects, and the file must never
   reach a ref.
3. **Write the importer dry-run by default.** `--selftest`, then a dry run that
   prints counts only, then `--apply` as a separate explicit step. The counts
   must separate: rows read, matched to an active identity, unmatched, matched
   but with no digest (provider-only: they link on first sign-in, not a failure),
   digest in a format the target does not verify, already holding a credential,
   and to insert.
4. **Treat the export as untrusted input that becomes executable SQL.** Validate
   every digest against a strict pattern for the exact hash format the target's
   verifier accepts before it is spliced into a statement, and put an
   injection-shaped row in the selftest so the pattern is proven to reject it
   rather than assumed to.
5. **Match on lowercased email against active rows only, and make the insert
   idempotent** (`WHERE NOT EXISTS` on user plus provider) so a re-run after a
   partial failure adds nothing. Before any case normalization of stored emails,
   check for a lowercase twin: a blind `lower()` update collides with an existing
   row and either fails or merges two people.
6. **Never print an email or a hash**, in the dry run or the apply. Counts and
   the lockout delta are the report.
7. **Re-count after the apply**: credential rows must equal the pre-count plus
   the inserted count. That still is not proof that anyone can sign in. The proof
   is one migrated password user and one provider-only user each completing a
   real sign-in and seeing their own data.
