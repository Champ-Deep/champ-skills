#!/usr/bin/env python3
"""
Evidence pass: fetch, for each active repo, the manifests and signals needed to
derive topics and a description from what the code actually is.

No mutation. Writes evidence.json only.
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

SP = os.path.dirname(os.path.abspath(__file__))
VIEWER = "Champ-Deep"

# Framework -> topic, matched against manifest text.
STACK_RULES = [
    # frontend frameworks
    (r'"next"\s*:', "nextjs"), (r'"react"\s*:', "react"),
    (r'"vue"\s*:', "vue"), (r'"svelte"\s*:', "svelte"),
    (r'"@angular/core"', "angular"), (r'"astro"', "astro"),
    (r'"vite"', "vite"), (r'"tailwindcss"|"@tailwindcss', "tailwindcss"),
    (r'"next-auth"|"@auth/core"|"@clerk/nextjs"|"clerk"', "authentication"),
    (r'"@trpc/server"|"trpc"', "trpc"),
    (r'"framer-motion"|"motion"', "framer-motion"),
    (r'"@radix-ui/', "design-system"),
    # backend / api
    (r'fastapi|uvicorn', "fastapi"), (r'flask', "flask"),
    (r'django', "django"), (r'express', "express"),
    (r'"hono"', "hono"), (r'fastify', "fastify"),
    # ai / llm
    (r'openai|langchain_openai|openai-python', "llm"),
    (r'anthropic|claude-code|@anthropic-ai', "anthropic"),
    (r'langchain|llama-index', "rag"),
    (r'transformers|torch', "machine-learning"),
    (r'openrouter', "llm"),
    (r'tesseract|pytesseract|easyocr', "ocr"),
    (r'playwright', "playwright"), (r'puppeteer', "puppeteer"),
    (r'selenium', "selenium"), (r'beautifulsoup|scrapy|lxml', "web-scraping"),
    (r'firecrawl', "web-scraping"),
    # data
    (r'sqlalchemy|prisma|drizzle|typeorm|sequelize', "orm"),
    (r'postgres|psycopg|asyncpg', "postgresql"),
    (r'mongodb|pymongo|mongoose', "mongodb"),
    (r'supabase', "supabase"),
    (r'pandas|numpy', "data-analysis"),
    (r'networkx', "graph-analysis"),
    (r'neo4j', "neo4j"),
    (r'elasticsearch', "elasticsearch"),
    (r'pinecone|chromadb|qdrant|weaviate', "vector-database"),
    # infra
    (r'docker|docker-compose', "docker"),
    (r'terraform', "terraform"),
    (r'aws-sdk|boto3', "aws"),
    (r'firebase|@supabase', "saas"),
    (r'websocket|socket\.io', "websockets"),
    (r'celery|bullmq|rq\b', "job-queue"),
    (r'redis|aioredis', "redis"),
    (r'prometheus|grafana', "observability"),
    (r'sentry', "sentry"),
    # infra-as-code / devops
    (r'vercel', "vercel"), (r'railway', "railway"),
    # auth
    (r'passport|bcrypt|jwt', "authentication"),
    # doc / pdf
    (r'pymupdf|fitz|pypdf|reportlab|weasyprint', "pdf"),
    (r'docx|python-docx', "docx"),
    (r'openpyxl|pandas.*xlsx', "spreadsheet"),
    (r'pptx|python-pptx', "pptx"),
]

PURPOSE_RULES = [
    (r"scrap|crawl|harvest", "web-scraping"),
    (r"email|smtp|imap|mailbox|inbox", "email"),
    (r"\bcrm\b|pipeline|lead|prospect|outreach|campaign", "sales-automation"),
    (r"\bseo\b|serp|keyword|backlink", "seo"),
    (r"linkedin|\bsocial\b", "social-media"),
    (r"chatbot|assistant|\bagents?\b", "ai-agents"),
    (r"video|avatar|reel", "video"),
    (r"audio|voice|speech|\btts\b", "voice"),
    (r"qr-code|webxr|augmented-reality", "augmented-reality"),
    (r"location|\bgeo\b|\bmaps?\b|google-maps", "maps"),
    (r"chart|dashboard|analytics", "analytics"),
    (r"quiz|\bgame\b|reward", "gamification"),
    (r"resume|\bcv\b|recruit|hiring|candidate", "recruitment"),
    (r"invoice|billing|payment|checkout", "billing"),
    (r"documents?|\bpdf\b|signing|contract", "document-management"),
    (r"knowledge|wiki|graph|\brag\b", "knowledge-graph"),
    (r"react-native|expo|flutter|\.swift|kotlin-compose", "mobile"),
    (r"security|audit|pentest", "security"),
    (r"\blabels?\b|annotation|labelling", "data-engineering"),
    (r"health|longevity|wellness|fitness|patient", "healthtech"),
    (r"\btravel\b|itinerary", "travel"),
    (r"\blms\b|course|\bedtech\b", "edtech"),
    (r"real-estate|property", "real-estate"),
    (r"legal|compliance|\bcontracts?\b", "legaltech"),
    (r"campus|student|university", "edtech"),
]

# A 20-topic repo is a repo nobody reads. Cap it: topics are a discovery hint,
# not a keyword dump.
MAX_TOPICS = 8


def gh(path, timeout=40, tries=3):
    import time
    last = None
    for i in range(tries):
        try:
            p = subprocess.run(["gh", "api", path], capture_output=True,
                               text=True, timeout=timeout)
            if p.returncode == 0:
                if not p.stdout.strip():
                    return None
                try:
                    return json.loads(p.stdout)
                except json.JSONDecodeError:
                    return None
            err = (p.stderr or "")
            if any(c in err for c in ("502", "503", "504")):
                last = err
                time.sleep(1.5 * (i + 1))
                continue
            return None
        except subprocess.TimeoutExpired:
            last = "timeout"
            time.sleep(1.5 * (i + 1))
    return {"__error__": last}


def evidence_for(full_name, default_branch):
    ev = {"full_name": full_name, "manifests": {}, "dirs": [], "readme_head": None,
          "has_dockerfile": False, "has_package_json": False}
    tree = gh(f"repos/{full_name}/git/trees/{default_branch}?recursive=1")
    if isinstance(tree, dict):
        paths = [t["path"] for t in tree.get("tree", []) if t.get("type") == "blob"]
    else:
        paths = []
    ev["paths"] = paths
    ev["has_dockerfile"] = any(p.lower().endswith(("dockerfile", "docker-compose.yml",
                                                    "docker-compose.yaml")) for p in paths)
    ev["dirs"] = sorted({p.split("/")[0] for p in paths if "/" in p})[:40]

    for m in ["package.json", "requirements.txt", "pyproject.toml", "go.mod",
              "Cargo.toml", "setup.py", "Gemfile", "composer.json"]:
        if m in paths:
            c = gh(f"repos/{full_name}/contents/{m}")
            if isinstance(c, dict) and c.get("content"):
                import base64
                try:
                    txt = base64.b64decode(c["content"]).decode("utf-8", "replace")
                    ev["manifests"][m] = txt[:6000]
                except Exception:
                    pass

    rd = gh(f"repos/{full_name}/readme")
    if isinstance(rd, dict) and rd.get("content"):
        import base64
        try:
            ev["readme_head"] = base64.b64decode(rd["content"]).decode("utf-8", "replace")[:1500]
        except Exception:
            pass
    return ev


def clean_prose(text):
    """Strip markup before matching intent keywords.

    A shields.io badge reads `?style=social`, which was enough to tag a PDF
    tool as a social-media project. HTML tags, badge URLs and image alts are
    chrome, not prose, and none of them should be able to vote on a topic.
    """
    t = re.sub(r"https?://\S+", " ", text)          # badge/URL noise
    t = re.sub(r"<[^>]+>", " ", t)                  # raw HTML tags
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)     # images
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)  # links -> label
    t = re.sub(r"[#>*_`~|]", " ", t)                # md syntax chars
    return t


def derive(ev, repo):
    """Derive topics, separating trustworthy signal from noise.

    Manifest dependencies are what the author DECLARED they built with, so they
    are strong evidence. File paths are not: a Python repo with a
    `data/video/voice/` directory is not a video product. Reading purpose topics
    out of the path list produced topics like 'education' and 'voice' on a PDF
    tool, purely from folder names. So purpose is read from the description and
    README prose only, and the path list is used for nothing at all.
    """
    manifests = " ".join(ev["manifests"].values()).lower()

    # Prose = the author's own words about intent. Descriptions and the opening
    # of the README are the only places intent is stated on purpose.
    prose = clean_prose(" ".join([
        repo.get("description") or "",
        repo["name"],
        (ev.get("readme_head") or "")[:900],
    ])).lower()

    stack, purpose = set(), set()
    for pat, topic in STACK_RULES:
        if re.search(pat, manifests) or re.search(pat, prose):
            stack.add(topic)
    for pat, topic in PURPOSE_RULES:
        if re.search(pat, prose):          # prose only, never paths
            purpose.add(topic)

    lang = repo.get("language")
    if lang:
        stack.add({"Python": "python", "TypeScript": "typescript",
                   "JavaScript": "javascript", "HTML": "html",
                   "Rust": "rust", "Shell": "shell"}.get(lang, lang.lower()))

    # Rank: the language, then what it is, then what it is built from.
    topics = [t for t in [lang.lower() if lang else None] if t]
    topics += sorted(purpose)[:3]
    topics += sorted(stack)[:max(1, MAX_TOPICS - len(topics) - 1)]
    if repo["private"]:
        topics.append("private")
    seen, out = set(), []
    for t in topics:
        if t and t not in seen and re.fullmatch(r"[a-z0-9][a-z0-9+.\-]*", t):
            seen.add(t)
            out.append(t)
    return out[:MAX_TOPICS + 1]


def main():
    audit = json.load(open(sys.argv[1]))
    R = audit["repos"]
    NAME_KEYS = ["-backup", "_backup", ".backup-", "backup-", "(copy)", "-copy", "-old", "_old"]

    def is_backup(r):
        n = r["name"].lower()
        return any(k in n for k in NAME_KEYS) or bool(
            r.get("description") and "backup" in r["description"].lower())

    targets = [r for r in R if not r["fork"] and not is_backup(r)]
    print(f"evidence pass over {len(targets)} active repos", file=sys.stderr)
    out = {}
    with ThreadPoolExecutor(max_workers=7) as ex:
        futs = {ex.submit(evidence_for, r["full_name"], r["default_branch"]): r for r in targets}
        done = 0
        for f in as_completed(futs):
            r = futs[f]
            try:
                ev = f.result()
            except Exception as e:
                print(f"  ! {r['full_name']}: {e!r}", file=sys.stderr)
                continue
            ev["derived_topics"] = derive(ev, r)
            ev["name"] = r["name"]
            ev["description"] = r.get("description")
            ev["private"] = r["private"]
            ev["language"] = r.get("language")
            ev["stars"] = r["stars"]
            ev["file_count"] = r["file_count"]
            ev["days_idle"] = r["days_idle"]
            ev["has_readme"] = r["has_readme"]
            ev["has_license_file"] = r["has_license_file"]
            out[r["full_name"]] = ev
            done += 1
            if done % 10 == 0 or done == len(targets):
                print(f"  {done}/{len(targets)}", file=sys.stderr)
    json.dump(out, open(sys.argv[2], "w"), indent=1)
    print(f"wrote {sys.argv[2]} ({len(out)} repos)", file=sys.stderr)


if __name__ == "__main__":
    main()
