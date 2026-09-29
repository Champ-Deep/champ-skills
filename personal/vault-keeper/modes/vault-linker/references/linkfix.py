import os,re,sys,collections
root=os.environ.get("VAULT") or os.path.expanduser("~/mnt/Celsus")
APPLY = "--apply" in sys.argv
SKIP={"_ARCHIVE-2026-09-09","studio","Excalidraw"}

DENY = set("""TOOLS after SETUP default SECURITY USER script scripts form forms wikilinks wikilink
INSTALL MEMORY route template output YYYY-MM-DD refresh proxy layout analytics DAD videos HEARTBEAT
PHONE EMAIL WA QUOTE NAME name error HISTORY History fetch SOUL TIER SIZE DATES redirect contributing
connection loading links link image logging runtime self-hosting authentication accessibility
unauthorized sitemap date note debugging REVIEW TASKS Vision brief PIPELINE README ARCHITECTURE
IDENTITY CHANGELOG marketing CLAUDE Celsus TRIAGE-SKILL MULTI_AGENT_SETUP REALITY_SEED_FORMAT
morning-routine vault-keeper vault-linker champ-brainstorm day-planner sprint-mode interactive-quiz
meeting-intake celsus-cortex doc-coauthoring schedule firecrawl vinh-copywriting champions-group-brand
paa-seo-builder reach-engage interview-prep daily-social-triage command-center-ingest leadscon-priority
champtrack-it-audit champvox-build-prompt feedback_seo_ai_era feedback_no_em_dashes
champgraph_mcp.py graphiti_tools.py deependhq.com deependhq celsus-command-center shealth.ai
champions.ranch.farm""".split())

ALIAS = {
 "Sreedeep":"Sreedeep Surapaneni","LakeB2B":"Lake B2B","SPAN":"SPAN Global Services",
 "Bryan":"Bryan (Amarjeet)","Champion Infratech":"InfraTech","Champion InfraTech":"InfraTech",
 "Infratech":"InfraTech","ChampIQ":"Champ IQ","SGS":"SPAN Global Services",
}

files=[]
for dp,dns,fns in os.walk(root):
    dns[:]=[d for d in dns if d not in SKIP and not d.startswith('.')]
    for f in fns:
        if f.endswith(".md"): files.append(os.path.join(dp,f))

stats=collections.Counter(); touched=set()

def flatten_nested(t):
    # [[ A [[X|Y]] B ]] -> [[ A Y B ]]   (repeat until stable)
    n=0
    for _ in range(6):
        new=re.sub(r'(\[\[[^\[\]]*?)\[\[([^\[\]|]+)\|([^\[\]]+)\]\]', r'\1\3', t)
        new=re.sub(r'(\[\[[^\[\]]*?)\[\[([^\[\]|]+)\]\]', r'\1\2', new)
        if new==t: break
        n+=1; t=new
    return t,n

for p in files:
    try: orig=open(p,encoding="utf-8").read()
    except: continue
    t=orig
    # 0. malformed trailing backslash inside link
    t2=re.sub(r'\[\[([^\[\]|]+?)\\\]\]', r'[[\1]]', t)
    if t2!=t: stats["malformed_backslash"]+=1; t=t2
    # 1. nested link corruption
    t,nn=flatten_nested(t)
    if nn: stats["nested_flattened"]+=nn
    # 2. "[[Lake]] B2B" -> "[[Lake B2B]]"
    t2=re.sub(r'\[\[Lake\]\]\s+B2B', '[[Lake B2B]]', t)
    if t2!=t: stats["lake_split"]+=1; t=t2
    t2=re.sub(r'\[\[Lake\]\]', 'Lake', t)
    if t2!=t: stats["lake_bare"]+=1; t=t2
    # 3. deny-list unlink  [[W]] or [[W|D]] -> W / D
    def unlink(m):
        tgt=m.group(1).strip(); disp=(m.group(2) or tgt).strip()
        if tgt in DENY:
            stats["unlinked:"+tgt]+=1
            return disp
        return m.group(0)
    t=re.sub(r'\[\[([^\[\]|#]+?)(?:\|([^\[\]]*))?\]\]', lambda m: unlink(m), t)
    # 4. alias rewrite  [[Alias]] -> [[Canonical|Alias]]
    def alias(m):
        tgt=m.group(1).strip(); disp=m.group(2)
        if tgt in ALIAS:
            stats["alias:"+tgt]+=1
            return "[[%s|%s]]" % (ALIAS[tgt], disp.strip() if disp else tgt)
        return m.group(0)
    t=re.sub(r'\[\[([^\[\]|#]+?)(?:\|([^\[\]]*))?\]\]', lambda m: alias(m), t)
    if t!=orig:
        touched.add(p)
        if APPLY: open(p,"w",encoding="utf-8").write(t)

print(("APPLIED" if APPLY else "DRY RUN"), "files changed:",len(touched))
tot=0
for k,v in stats.most_common(400):
    tot+=v
    if v>=3 or not k.startswith("unlinked:"): print(f"{v:6d}  {k}")
print("total edits:",tot)
