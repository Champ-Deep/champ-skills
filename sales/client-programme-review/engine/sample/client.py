"""SAMPLE CLIENT. Everything here is invented: the client, the companies, the numbers, the events and the links.

This is the one file you edit for a new client (plus ledger.json beside it). Work top to bottom:
  1. the lead table        one row per lead, from the client's own sheet plus our call notes
  2. sends, calls, universe
  3. the named leads       only leads the CLIENT has named; leave empty and the board opens blank
  4. config                markets, filters, what a lead card shows, what the win profile compares
  5. copy                  every sentence on the page; numbers come from the tables above, never typed twice
Copy is inserted as HTML: write & as &amp; and never paste a client's text without reading it.

Build:  python3 ../make.py .            (draft, red ribbon while ledger.json has an open entry)
        python3 ../make.py . --final    (refuses until the ledger is clean)
        PR_MODE=weekly python3 ../make.py . --final      (review | monthly | weekly)
"""
import collections
import os

MODE = os.environ.get("PR_MODE", "review")  # review | monthly | weekly
CLIENT, BRAND, DATE = "Brightline", "LakeB2B", "16 March 2026"  # CLIENT is the short name used in sentences
SLUG = f"2026-03-16 - Brightline x LakeB2B Programme {MODE.title()}"
NOTE_TITLE = f"Brightline x LakeB2B programme {MODE}, {DATE}"

# ---- 1. the lead table ----
# co, role, market, industry, system today, system family, live project?, who decides, timeline, staff, stated pain, lead date
ROWS = [
 ["Alder Haulage", "Fleet Manager", "N", "General haulage", "Spreadsheets", "None", "Yes", "Local", "3 to 6 months", "51 to 200", "Late deliveries", "2026-01-12"],
 ["Birch Cartage", "Operations Director", "N", "General haulage", "RouteDesk", "Legacy", "Yes", "Local", "0 to 3 months", "201 to 500", "Fuel cost", "2026-01-14"],
 ["Cedar Cold Chain", "Head of Transport", "C", "Chilled distribution", "In-house tool", "In-house", "No", "Local", "None set", "201 to 500", "Fuel cost", "2026-01-19"],
 ["Dunmore Parcels", "IT Manager", "C", "Parcel delivery", "RouteDesk", "Legacy", "Planned", "Group", "6 to 12 months", "501 to 1,000", "Driver shortage", "2026-01-21"],
 ["Elmfield Bulk", "Fleet Manager", "S", "Bulk transport", "Spreadsheets", "None", "Yes", "Local", "3 to 6 months", "51 to 200", "Late deliveries", "2026-01-27"],
 ["Fernside Freight", "Operations Manager", "N", "General haulage", "RouteDesk", "Legacy", "No", "Group", "None set", "501 to 1,000", "Fuel cost", "2026-02-02"],
 ["Garrow Distribution", "Head of Transport", "N", "Chilled distribution", "PlanWise", "Legacy", "Yes", "Local", "0 to 3 months", "201 to 500", "Fuel cost", "2026-02-05"],
 ["Harlow Tankers", "Finance Manager", "S", "Bulk transport", "In-house tool", "In-house", "Evaluating", "Local", "6 to 12 months", "51 to 200", "Reporting", "2026-02-11"],
 ["Islay Couriers", "IT Manager", "C", "Parcel delivery", "PlanWise", "Legacy", "Yes", "Group", "3 to 6 months", "1,001 to 5,000", "Driver shortage", "2026-02-17"],
 ["Juniper Logistics", "Fleet Manager", "N", "General haulage", "Spreadsheets", "None", "Yes", "Local", "3 to 6 months", "201 to 500", "Late deliveries", "2026-02-24"],
 ["Kestrel Movers", "Operations Director", "C", "General haulage", "RouteDesk", "Legacy", "No", "Local", "None set", "51 to 200", "Fuel cost", "2026-03-03"],
 ["Larch Transport", "Head of Transport", "N", "Chilled distribution", "PlanWise", "Legacy", "Yes", "Local", "0 to 3 months", "201 to 500", "Fuel cost", "2026-03-10"],
]
KEYS = ["co", "role", "mkt", "ind", "sys", "fam", "proj", "auth", "time", "staff", "pain", "date"]
LEADS: list[dict] = [dict(zip(KEYS, r)) for r in ROWS]
CONTRACTED = 20

# ---- 3. leads the CLIENT has named as progressing (empty list = the board opens blank and the client marks it) ----
NAMED_COS = []
NAMED = {"by": "your team", "on": DATE}
for i, x in enumerate(LEADS):
    x["id"] = i + 1
    x["fn"] = "IT" if "IT" in x["role"] else "Finance" if "Finance" in x["role"] else "Operations"
    x["named"] = x["co"] in NAMED_COS
assert sum(x["named"] for x in LEADS) == len(NAMED_COS) <= 3, "a named lead is not in the table, or more than three are named"

# ---- 2. sends, calls, universe ----
SENDS = [  # name, dates, clicked, opened without a click, not opened, sent
    ["Emailer 1", "6 Jan", 31, 150, 419, 600],
    ["Emailer 2", "20 Jan", 44, 120, 426, 590],
    ["Emailer 3", "3 Feb", 12, 131, 442, 585],
]
for s in SENDS:
    assert s[2] + s[3] + s[4] == s[5], s
CALLS = {"dials": 320, "connected": 26, "voicemail": 118, "period": "2 to 6 February"}
UNIVERSE = {"contacts": 4000, "emailed": SENDS[0][5], "dialled": CALLS["dials"]}  # contacts: sized at kickoff, see the ledger

n = len(LEADS)
count = lambda k, rows=LEADS: dict(collections.Counter(x[k] for x in rows).most_common())
mkt, fam, pain = count("mkt"), count("fam"), count("pain")
live = sum(x["proj"] == "Yes" for x in LEADS)
local = sum(x["auth"] == "Local" for x in LEADS)
emails, clicks = sum(s[5] for s in SENDS), sum(s[2] for s in SENDS)
best, worst = max(SENDS, key=lambda s: s[2]), min(SENDS, key=lambda s: s[2])
connect_pct = round(100 * CALLS["connected"] / CALLS["dials"], 1)

# ---- 4. config ----
MARKETS = {"N": "Northern region", "C": "Central region", "S": "Southern region"}
FILTERS = [["all", f"All {n}", None, None], ["live", "Live project", "proj", "Yes"]] + [[k, v, "mkt", k] for k, v in MARKETS.items()] \
    + [["legacy", "On a legacy planner", "fam", "Legacy"], ["nonops", "IT and finance", "fn", "Operations", True]]  # [key, label, field, value, negate]
CARD = {"facts": [["sys", "Planning today"], ["time", "Timeline"]], "pills": [["proj", "Project"], ["auth", "Decision"]],
        "go": ["Yes", "Local"], "no": ["No"], "na": ["Not asked"]}  # which answers read as green, red, or not asked
DIMS = [["mkt", "Market"], ["ind", "Industry"], ["fn", "Function of the contact"], ["fam", "Planning system"], ["staff", "Company size"],
        ["pain", "Stated pain"], ["proj", "Live project"], ["auth", "Decision taken"], ["time", "Timeline"]]
DISP = {"mkt": MARKETS, "fam": {"None": "No planning system", "Legacy": "Legacy planner"}}
SUF = {"staff": " staff"}
SECTIONS = {"review": ["universe", "work", "emails", "simulation", "leads", "learned", "loop", "research", "tiers"],
            "monthly": ["universe", "work", "emails", "simulation", "leads", "learned", "loop"],
            "weekly": ["work", "emails", "leads", "learned", "loop"]}[MODE]
SIM_RUN = None  # path to the simulation run (client-messaging-simulation); the section hides itself without one

META = {"title": f"Brightline Programme {MODE.title()}",
        "desc": f"Brightline and {BRAND}: {n} leads delivered, what the programme taught us, and what comes next.",
        "chip": "Prepared for Brightline", "short": f"The {n} leads",
        "cta_h": "Name the leads that are moving, and we will bring back their profile.",
        "cta_p": f"Two things to settle: which leads are progressing, and the status of all {n}.",
        "foot": f"Prepared by {BRAND} for Brightline Freight Systems \u00b7 Confidential \u00b7 {DATE}",
        "brand": {"nav_label": f"Programme {MODE}", "cta_url": "#leads", "cta_label": "Mark the leads that are moving", "home_url": "#loop", "home_label": "What we need from you"}}

# ---- 5. copy ----
LESSONS = [
    {"t": "The Northern region answers", "ev": f"{mkt['N']} of {n} leads came from the Northern region.",
     "bars": [[MARKETS[k], v] for k, v in mkt.items()], "max": max(mkt.values()), "next": "Next: weight calling to the Northern region."},
    {"t": "Legacy planners are the pool", "ev": f"{fam['Legacy']} of {n} leads run a legacy planning tool.",
     "bars": [[DISP["fam"].get(k, k), v] for k, v in fam.items()], "max": max(fam.values()), "next": "Next: build lists by installed planner."},
    {"t": "Fuel cost opens the door", "ev": f"{pain['Fuel cost']} of {n} leads named fuel cost first.",
     "bars": [[k, v] for k, v in pain.items()], "max": max(pain.values()), "next": "Next: the first line of every message speaks to fuel cost."},
    {"t": "Something to read beats a meeting ask", "ev": f"{best[0]} drew {best[2]} clicks. {worst[0]}, a plain request for a call, drew {worst[2]}.",
     "bars": [[s[0], s[2]] for s in SENDS], "max": best[2], "next": "Next: every send carries a guide or a customer story."},
    {"t": "Most decisions are taken locally", "ev": f"{local} of {n} leads decide locally. {live} of {n} have a live project.",
     "bars": [["Decides locally", local], ["Live project", live, "#B9B2C4"]], "max": n, "next": "Next: keep both questions on every call."},
    {"t": "The phone alone reaches few people", "ev": f"{CALLS['connected']} of {CALLS['dials']} dials reached the prospect in the measured week.",
     "bars": [["Dials", CALLS["dials"], "#B9B2C4"], ["Voicemail", CALLS["voicemail"], "#7A76DA"], ["Reached", CALLS["connected"]]], "max": CALLS["dials"],
     "next": "Next: warm the account by email before the call."},
][: {"review": 6, "monthly": 3, "weekly": 1}[MODE]]

COPY = {
    # hero
    "hero_h1": f"{n} leads delivered into regional freight operators.",
    "hero_eyebrow": f"Brightline and {BRAND}, programme {MODE}, {DATE}",
    "hero_lead": "Ten weeks of email and calling across three regions. Here is what it produced, what it taught us, and what we need from your team.",
    "floaters": [  # exactly three. count animates up to the number; cmp is the comparison line; bar is a percentage, or use flags
        {"k": "Leads delivered", "count": n, "text": str(n), "cmp": f"of <b>{CONTRACTED}</b> contracted, <b>{CONTRACTED - n}</b> pending", "bar": round(100 * n / CONTRACTED, 1)},
        {"k": "Emails across three sends", "count": emails, "text": f"{emails:,}", "cmp": f"<b>{clicks}</b> clicks", "bar": 100, "gold": True},
        {"k": "Leads with a live project", "count": live, "text": str(live), "small": f" of {n}", "cmp": "asked on every call",
         "flags": [f"{MARKETS[k]} {v}" for k, v in mkt.items()]},
    ],
    "pills": [["Deliverable", "Qualified leads with a tentative slot"], ["Markets", ", ".join(MARKETS.values())], ["Buyers", "Fleet and operations leaders"],
              ["Channels", "Email, then calling"], ["Window", "6 January to 10 March 2026"]],
    "nav": {"universe": "The universe", "work": "What we ran", "emails": "The messaging", "simulation": "Simulation", "leads": f"The {n} leads",
            "learned": "What we learned", "loop": "What we need", "research": "Win profile", "tiers": "Ways forward"},
    # universe: four stages, in this order: profile, emailed, dialled, delivered
    "uni_h": f"From about {UNIVERSE['contacts']:,} contacts to {n} delivered leads.",
    "beats": [[f"{UNIVERSE['contacts']:,}", "Contacts in your profile, approximately", "Fleet and operations leaders at freight operators in the three regions, as sized at kickoff, to be refreshed."],
              [str(UNIVERSE["emailed"]), "On the email list", f"Three sends. {emails:,} emails, {clicks} clicks."],
              [str(CALLS["dials"]), "Dials in one measured week", f"{CALLS['period']}. {CALLS['connected']} calls reached the prospect. One week measured, not the whole programme."],
              [str(n), "Leads delivered", "Each one handed over with the call summary and the recording."]],
    "uni_aria": f"About {UNIVERSE['contacts']:,} dots, one per contact in the profile. {UNIVERSE['emailed']} are lit as emailed, {CALLS['dials']} as dialled in the measured week, and {n} gold dots are the delivered leads.",
    "uni_key": ["In profile", "Emailed", "Dialled, measured week", "Delivered lead"],
    # what we ran: [date, title, text, [[tag, highlighted], ...]]
    "work_h": "Ten weeks, and every change came from your feedback.",
    "work_note": "You asked for quality over volume at the first review. The programme was reshaped around it twice.",
    "reports": ["Weekly review call", "Send report after each of the three sends", "Calling report, 2 to 6 February", "Call recording and summary with every lead"],
    "steps": [["6 Jan", "Launch the email series", "Landing page and three emailers built on your route planning guide.", [["600 contacts", True], ["3 emailers", False]]],
              ["15 Jan", "Add your two questions", "Is there a live project, and who takes the decision. Both went onto every call the same day.", [["Live project", True], ["Decision authority", True]]],
              ["3 Feb", "Lead with the guide", "After the first two sends, every message carried something to read.", []]],
    # messaging
    "em_h": "Three emailers went out. The one with the guide drew the clicks.",
    "em_note": f"Pick an emailer to read what was sent and what came back. {best[0]} drew {best[2]} clicks. {worst[0]} drew {worst[2]}.",
    "em_panel_k": "Three sends, 6 Jan to 3 Feb",
    "em_fine": "Copy is paired with each send in series order. If your records show a different order, change the pairing beside the email.",
    "mail": [  # one per send, in series order: k = short name, cta = the button, body = paragraphs, list = bullets
        {"k": "Introduction", "cta": "Demo form", "body": ["Freight operators are under pressure on fuel and on delivery windows.", "Brightline plans routes around both."], "list": ["Fewer empty miles", "Tighter delivery windows"]},
        {"k": "The route planning guide", "cta": "Guide download", "body": ["How three regional operators cut empty miles.", "The guide walks through what they changed first."], "list": []},
        {"k": "The meeting ask", "cta": "Demo form", "body": ["Would you be open to a brief conversation about your routes?"], "list": []},
    ],
    # simulation (only shown when SIM_RUN points at a run)
    "sim_h": "We replayed the three emailers to a simulated panel of your buyers.",
    "sim_note": "{n} simulated personas, built from the profile of the leads delivered so far, were shown all three emailers and one rewrite. {scored} returned a scored reaction.",
    "sim_asks_h": "Three things only Brightline can supply",
    # lead board
    "leads_eyebrow": f"The {n} leads",
    "leads_note": "Mark up to three that your team sees progressing. The panel shows what they share.",
    "leads_fine": "Companies and lead dates match your shared lead sheet. Project, decision, system and timeline come from our call notes.",
    "pending": [CONTRACTED - n, f"more leads are pending to complete the {CONTRACTED}, held to the same two questions."],
    # lessons
    "learn_h": f"What the first {n} leads taught us about your market.",
    "learn_note": "Each one is counted from the delivery record, the send reports or the calling report.",
    "lessons": LESSONS,
    # what we need: [title, text]
    "loop_steps": [["Outcome per lead", f"Your team marks each of the {n}: progressing, nurture or closed, and why."], ["Win profile", "We study the leads that moved."],
                   ["Lookalike accounts", "We pull the accounts that match the profile, minus your customers."], ["Message tested first", "Each new message meets the simulated panel first."],
                   ["Outreach, then back to step 1", "Results feed the next round."]],
    "need_k": "Four things we would like from your team",
    "ticks": [[f"Status of each of the {n} leads", "Progressing, nurture or closed."], ["The leads that are moving", "And what moved them."],
              ["Why the others stalled", "No project, no budget, wrong person or wrong timing."], ["Customer and exclusion list", "So lookalike lists never include an account you already own."]],
    # win profile study: [dimension, 1 if already visible in the leads else 0, one line]
    "dims_k": "Eight dimensions", "dims_note": "4 known today, 4 added", "dims_legend": f"Already visible in the {n} leads",
    "dims": [["Role and seniority", 1, "Fleet and operations managers."], ["Industry", 1, "General haulage first."], ["Location", 1, "The Northern region leads."], ["System in place", 1, "Legacy planners."],
             ["Buying group", 0, "Who else sits in the decision."], ["Social channels", 0, "Where they are active."], ["Events attended", 0, "Trade shows they go to."], ["Creators and voices", 0, "Who this audience listens to."]],
    # where the audience gathers: [id, kind, when, title, one line, tag, link, link label]. Four or more; seven fills the grid.
    "tiles": [["a", "Event", "12 to 14 May 2026", "Regional Freight Expo", "Northgate Exhibition Centre", "Northern region", "https://example.com/freight-expo", "Organiser page"],
              ["b", "Event", "9 to 10 Jun 2026", "Cold Chain Forum", "Central Hall", "Central region", "https://example.com/cold-chain", "Organiser page"],
              ["c", "Event", "22 Sep 2026", "Fleet Managers Day", "Harbour Conference Rooms", "Southern region", "https://example.com/fleet-day", "Organiser page"],
              ["d", "Association", "", "Regional Hauliers Association", "Runs a quarterly members meeting.", "Northern region", "https://example.com/hauliers", "Association site"],
              ["e", "Association", "", "Parcel Operators Guild", "Publishes a monthly bulletin.", "Central region", "https://example.com/parcel-guild", "Association site"],
              ["f", "Publication", "Weekly", "Freight Operator Weekly", "The trade newsletter most leads mentioned.", "All regions", "https://example.com/weekly", "Source"],
              ["g", "Social", "Mar 2026", "LinkedIn, freight groups", "The professional channel to test first.", "All regions", "https://example.com/groups", "Source"]],
    "bento_sources": "Sources: organiser and association pages. Sample data, not real events.",
    # tiers: n = label, t = title, s = one line, inc = what is included, fit = who it fits, mean = what it would mean
    "tiers": [{"n": "Tier 1", "t": "Outreach", "s": "The programme you know.", "inc": ["Email and calling into your profile", "Recording and summary with every lead"], "fit": "Fits a steady flow of qualified conversations.", "mean": "More leads like these."},
              {"n": "Tier 2", "t": "Outreach plus win profile", "s": "Outreach aimed at accounts that look like your wins.", "inc": ["Everything in Tier 1", "Win profile study, refreshed each quarter", "Lookalike account lists"], "fit": "Fits a higher share of leads that turn into pipeline.", "mean": "The list starts from who already bought."},
              {"n": "Tier 3", "t": "Outreach, win profile and paid media", "s": "Outreach and ad spend on the same accounts.", "inc": ["Everything in Tier 2", "Paid campaigns aimed at the lookalike accounts", "One report joining ads, email, calls and leads"], "fit": "Fits owning the accounts that match your wins.", "mean": "The buying group has seen you before the first call."}],
    # three numbers from this programme that make the case for the top tier: [number as HTML, sentence]
    "why": [[f"{connect_pct}<small>%</small>", f"of dials reached the prospect in the measured week: {CALLS['connected']} of {CALLS['dials']}."],
            [f"{n - local}<small> of {n}</small>", "leads have the decision taken above the person we reached."],
            [f"{best[2]}<small> vs {worst[2]}</small>", "clicks for an emailer with something to read against a plain meeting ask."]],
    "closing": f"{n} leads delivered, {CONTRACTED - n} pending, <span>and {live} of the {n} have a live project.</span>",
}
