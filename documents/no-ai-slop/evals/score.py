import json, re, difflib, os
from slop_lint import lint
fx = json.load(open('fixtures.json')); m = json.load(open('blind_map.json'))
truth = {f['id']: f for f in fx['slop'] + fx['clean']}
inv = {v: k for k, v in m.items()}
num = lambda t: set(re.findall(r'\d[\d,\.]*%?|\$\d+', t))
rows = []; R = {}
print("EDIT MODE")
for fid, f in truth.items():
    b = inv[fid]; orig = f['text']; ed = open(f'runs/edit/{b}').read().strip()
    before = lint(orig, is_push=f.get('is_push', False)); after = lint(ed, is_push=f.get('is_push', False))
    lost = num(orig) - num(ed); new = num(ed) - num(orig)
    sim = difflib.SequenceMatcher(None, orig.strip(), ed).ratio()
    rows.append((fid, len(before), len(after), sorted(lost), sorted(new), round(sim, 2)))
    print(f"  {fid:22s} findings {len(before):2d} -> {len(after):2d} | numbers lost {sorted(lost)} new {sorted(new)} | similarity {sim:.2f}" + (f" | residual {[(x['rule'],x['match']) for x in after]}" if after else ""))
R['edit'] = rows
print("\nDETECT MODE")
tp=fp=tn=fn=0; recall=[]
alias = {'stacked_fragments':'dramatic_fragment','kicker':'dramatic_fragment'}
for fid, f in truth.items():
    d = json.load(open(f'runs/detect/{inv[fid]}'.replace('.txt','.json')))
    is_slop = fid.startswith('S'); said = d['verdict'] == 'slop'
    tp += is_slop and said; fn += is_slop and not said; fp += (not is_slop) and said; tn += (not is_slop) and not said
    if is_slop:
        got = {alias.get(x['pattern'], x['pattern']) for x in d['findings']}
        exp = set(f['expect']); hit = exp & got
        recall.append(len(hit)/len(exp))
        print(f"  {fid:22s} expected {len(exp)} caught {len(hit)} missed {sorted(exp-got)}")
print(f"  verdicts: TP {tp} FN {fn} FP {fp} TN {tn}; mean pattern recall {sum(recall)/len(recall):.0%}")
print("\nGENERATION: baseline vs gated (linter findings)")
tot=[0,0]
for k in sorted(json.load(open('briefs.json'))):
    b = open(f'runs/baseline/{k}.txt').read(); g = open(f'runs/gated/{k}.txt').read()
    lb, lg = lint(b), lint(g); tot[0]+=len(lb); tot[1]+=len(lg)
    print(f"  {k:20s} baseline {len(lb)} {[(x['rule'],x['match'][:40]) for x in lb]}\n  {'':20s} gated    {len(lg)} {[(x['rule'],x['match'][:40]) for x in lg]}")
print(f"  totals: baseline {tot[0]} vs gated {tot[1]}")
