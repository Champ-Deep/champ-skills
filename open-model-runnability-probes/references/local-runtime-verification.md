# Local runtime verification (after the weights land)

The SKILL.md probes settle whether a download is worth doing. This settles whether
the installed runtime works, how fast it really is, and whether it stays local, all
before anything is wired to it.

## Procedure

1. **Install pinned, then freeze.** Dedicated venv, exact package version, then
   `pip freeze > requirements-lock.txt`. Pinning the model package does not pin
   torch/transformers/huggingface_hub; the freeze is what makes the setup
   reproducible next month.
2. **First inference on your own input**, not the model card's example. Print the
   structured output and the probability/score values so later runs are comparable.
3. **Benchmark the device the loader actually chose, warm and cold.**
   - Cold (first call) includes weight load, often download; it is not a latency
     number. Warm (second and third call) is the number to report, and report both.
   - Pass the accelerator explicitly when the API takes a device argument. The
     default resolved to CPU in one install while an explicit `device="mps"` gave
     a 200x speedup on the same machine, so the default device choice can dominate
     every latency claim about the model.
   - Measure on the target hardware. A T4 figure from the model card says nothing
     about this laptop.
4. **Prove it is offline.** Rerun the same script with
   `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1`, ideally with networking down. A local
   model that silently phones home is not a local model, and a missing tokenizer or
   encoder config only shows up here.
5. **Record first-inference loader warnings as part of the verdict.** A loader that
   clamps an out-of-range hyperparameter shipped by the checkpoint is telling you
   the affected outputs are uncalibrated. Carry that caveat to wherever the numbers
   will be read; do not let it die in the terminal scrollback.
6. **Treat zero-shot as unproven.** Decision and classification checkpoints can
   score near chance on a domain task while looking confident. Run your own labelled
   examples before wiring it into a product path, and treat fine-tuning as the step
   that makes it usable rather than an optional extra.
7. **Price the disk and swap before the download, then again before loading.**
   Venv plus weights plus framework can cost multiple GB; check free space as part
   of the go/no-go, not after. On macOS swap lives on the same volume as the
   weights, so watch `sysctl vm.swapusage` while the download runs: swap growth
   spends free disk one for one. If swap is near capacity, do not load weights
   larger than the memory actually left, since the load will be served from disk
   and the benchmark will measure thrashing instead of the model. Free memory
   first (close the VMs and browsers), then load.
8. **Verify the bytes against the repo before trusting the file.** After a
   resumed (`curl -C -`) download completes, compare the file's size and
   `shasum -a 256` against the `lfs.oid` from
   `https://huggingface.co/api/models/ORG/REPO/tree/main`. A resume that retried
   a partial segment and an interrupted transfer both look finished to `ls`.
9. **Install into the runtime's own model directory.** Drop the GGUF where the
   server auto-discovers it (`~/.hermes/models` for Hermes's llama.cpp preset
   generation, not `~/models`), and keep the load as a separate, deliberate step:
   landing the file must not start the server or consume the memory yet.

## Reporting

Lead with: device, warm ms, cold ms, checkpoint size, disk cost, and whether the
offline rerun passed. Separate what you ran from what the model card claims.

State the swap and free-disk figures next to the timing when the machine was
under pressure: a load measured while swap was near capacity is a measurement of
thrashing, not of the model, and saying so is cheaper than a re-run.

A speed number published without those two figures is not reproducible on
another machine, so quote them in the same sentence as the number rather than in
a footnote the reader skips.
