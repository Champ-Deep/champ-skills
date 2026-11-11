# Turning a delivered page into a reusable engine

Use this when one page built by hand should become the thing every future client build starts from. The target is a template plus a fictional sample client that reproduces the delivered page exactly, so the first new client is a data swap rather than a redesign.

## Procedure

1. **Freeze the delivered build as the reference.** Keep the exact file that was shown, plus the data and copy that produced it, in one private folder. Everything later is checked against it.
2. **Mark what is client-specific.** Every string, list, count and chart value in the page either comes from the client's data or is the shared design. Sort them into two columns; the second column is the template, the first becomes data and tokens.
3. **Parameterise in one direction.** One file per client holds the tables, the config and the copy. The template and stylesheet stay identical for every client. Never type the same number into the copy and the data: compute it from the table, or the two drift and the ledger gate cannot catch it.
4. **Prove parity on the reference client.** Build the reference client through the engine and diff its visible text against the frozen page with markup stripped and whitespace collapsed: require zero differing lines. A structural change usually shows up as a text difference before anything renders wrong, and a zero-diff build is the proof the extraction changed nothing a reader can see.
5. **Replace the real client with a fictional sample.** New sessions must be able to build, probe and screenshot without touching real client data. The sample carries invented leads, sends and copy, and its comments document every field the template reads.
6. **Re-run the probe on every mode.** Dropping sections changes which assertions still apply, so the probe skips what the build drops and each mode gets its own pass. A probe written against the original markup breaks the moment a selector changes; re-point assertions at the new structure rather than restoring the old one.
7. **Grep the leak out before anything is pushed.** Client name, people, markets and any other client identifier must return zero hits across the skill folder, while the real client's data stays in the private folder. This is the check that stops a private client's leads from shipping in a public repo.
8. **Rebuild the packaged copy after every change.** A skill shipped as a zip runs stale code when the zip is older than the folder; rebuild and re-upload it whenever the engine, kit or sample changes.

When the skill folder is read-only (a downloaded or installed copy), copy it out to a writable working directory and `chmod -R u+w` before building: a read-only copy fails on the first file the build writes, and the error reads as a broken build rather than a permission.

## Proof before handoff

- Reference client built through the engine: visible-text diff against the frozen page is empty.
- Probe passes in every shipped mode, with dropped-section assertions skipped.
- Leak greps print zero.
- The skill loads (`skill_view` returns it and its linked files).
- The packaged zip validates and was rebuilt from the current folder.
