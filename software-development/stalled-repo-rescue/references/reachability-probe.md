# Deciding what may stay in the tree during a rescue

Run before any deletion in the dead set the reachability probe reports. The
probe names files the entrypoint never imports; that is a question about
packaging, not a verdict on the work.

## 1. Does it import packages the manifest never declares?

```bash
grep -rhoE "from ['\"][^./][^'\"]*['\"]|require\(['\"][^./][^'\"]*['\"]\)" <suspect files> \
  | sort -u | grep -v node_modules
```

Cross-check each bare import against `package.json`. A package absent from the
manifest with code that imports it is a real feature whose dependencies were
never added, not abandoned work: it cannot have run, which is exactly why it
looks unreachable.

## 2. Is there a design doc or spec for it?

```bash
find . -maxdepth 3 \( -name 'plan.md' -o -name 'SPEC*' -o -name 'ADR*' -o -name 'README*' \) -newer package.json
grep -rli '<feature name>' docs/ README.md 2>/dev/null
```

A documented intent plus a coherent implementation is a product. Deleting it
destroys work that only looks dead because nothing wired it up.

## 3. Does it look like a coherent unit?

Size, consistent naming, a barrel export, a matching test file. Hundreds of
lines with consistent naming and a test file is a feature; a 40-line fragment
with a different naming scheme and no test is a prototype.

## The rule

**Isolate, do not delete.** A coherent Node or server-side package living inside
a browser `src/` tree is a packaging bug: give it its own directory, its own
`package.json` declaring the dependencies it imports, and its own `tsconfig.json`.
Use `git mv` so history follows the files.

## Reporting

Give each dead-set entry a verdict with the command output behind it: reachable
misplaced, coherent feature never wired, or prototype. Only the third is a
deletion candidate, and the deletion is still the reviewer's call.