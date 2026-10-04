#!/usr/bin/env python3
"""
_clef_run.py: run Cloudflare CLEF locally and answer a batch of SystemOne questions.

    python _clef_run.py <clef_snapshot_dir> <input.json> <output.json>

Run this with the interpreter that has torch + transformers (a separate venv from the
rest of the toolkit). semantic.py invokes it only when CLEF_PATH and CLEF_PY are both set,
so the main pipeline never needs torch installed.

Input is a SystemOne record:  {"state": str, "questions": {id: question}}
Output is the model's answers, keyed by question id, so the caller can blend them.

All questions go out in ONE call. CLEF evaluates each question against the same state in
isolation, which is the documented batching pattern: N questions cost one forward pass, not
N.
"""
import json
import os
import sys


def main():
    if len(sys.argv) != 4:
        sys.exit("usage: _clef_run.py <clef_dir> <input.json> <output.json>")
    clef_dir, in_path, out_path = sys.argv[1:4]

    if not os.path.isdir(clef_dir):
        sys.exit(f"clef: not a directory: {clef_dir}")

    sys.path.insert(0, clef_dir)
    try:
        import torch
        from joint_schema_model import (collate_records, encode_record,
                                        load_release_model)
    except ImportError as e:
        sys.exit(f"clef: cannot import the model from {clef_dir}: {e}\n"
                 f"  Install torch + transformers in the interpreter at CLEF_PY, and "
                 f"point CLEF_PATH at a downloaded Cloudflare/clef snapshot.")

    record = json.load(open(in_path, encoding="utf-8"))

    # MPS on Apple silicon, CPU otherwise. The model is large, so it is loaded in fp32 on
    # CPU unless MPS reports available; inference_mode keeps peak memory down.
    device = "mps" if getattr(torch.backends, "mps", None) and \
        torch.backends.mps.is_available() else "cpu"
    try:
        model, processor = load_release_model(clef_dir, device=device)
        encoded = encode_record(processor.tokenizer, record, processor=processor)
        batch = collate_records([encoded], processor.tokenizer.pad_token_id,
                                torch.device(device))
        with torch.inference_mode():
            logits = model(batch)[0]
    except TypeError:
        # Older signature: load_release_model(path, device="cuda") only.
        model, processor = load_release_model(clef_dir, device="cpu")
        encoded = encode_record(processor.tokenizer, record, processor=processor)
        batch = collate_records([encoded], processor.tokenizer.pad_token_id,
                                torch.device("cpu"))
        with torch.inference_mode():
            logits = model(batch)[0]

    def _probs(v):
        """Real CLEF hands back a torch tensor; a stub or another backend may hand back a
        plain list of floats. Normalise both to a probability list."""
        if hasattr(v, "float") and hasattr(v, "softmax"):
            return v.float().softmax(-1).tolist()
        if hasattr(v, "softmax"):
            return v.softmax(-1).tolist()
        vals = list(v)
        import math
        ex = [math.exp(x) for x in vals]
        z = sum(ex) or 1.0
        return [x / z for x in ex]

    answers = {}
    # Per the Cloudflare example: logits = model(batch)[0], then
    # zip(encoded.questions, logits). Each entry is one question's per-option logits.
    for question, question_logits in zip(encoded.questions, logits):
        probs = _probs(question_logits)
        if getattr(question, "question_type", None) == "noul" or \
                len(probs) == 2:
            # noul: YES is index 0 in the joint schema
            answers[question.question_id] = float(probs[0])
        else:
            answers[question.question_id] = {
                "probs": probs,
                "option_ids": list(getattr(question, "option_ids", []) or []),
            }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(answers, f)
    print(f"clef: {len(answers)} answers on {device}")


if __name__ == "__main__":
    main()