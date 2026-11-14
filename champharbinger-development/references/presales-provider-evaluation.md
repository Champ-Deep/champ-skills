# Evaluating a presales signal provider before building on it

Use before any card that adds a signal, enrichment or trigger to a product with per-org BYOK (ChampHarbinger, Treg pipelines). Procedure in order; each step blocks the next.

## 1. Confirm the current product cannot already answer

Fire the actual seam in the live product before designing anything: the product's own provider agents through its own routes, from a logged-in session, not a vendor website. If the seam already returns the field the play needs (a person's current role, a company's news), the feature is a composition, not a provider purchase. If it returns a stale or partial record, that is evidence for the next steps, not a failure.

A stale enrichment record is itself the signal the play is about: a person's stored employer and title disagreeing with reality is the job-change case. Log which provider served each row; a 17-provider waterfall that returns nothing is a real finding and belongs in the readback.

## 2. Terms before features

Read the provider's API terms for embedding and redistribution, and write the answer into the card body. Most sales data vendors forbid showing their data to people outside the key holder's own company (Apollo, People Data Labs, Wappalyzer, Crunchbase by default, Ocean.io self serve). Consequence: each tenant org brings its own provider key (BYOK), because the org works under its own contract; a house key serves only the operator's own orgs. A feature that assumes one shared key silently breaks the vendors' terms at the first external tenant.

LinkedIn is the special case: there is no official LinkedIn API for role and job-change data (the partner program is closed to new partners), and derivative LinkedIn data carries ToS and litigation risk. Any job-change or profile play is built on a third party's LinkedIn-derived feed, so name that dependency in the card and treat it as replaceable, not as a stable substrate.

## 3. Check the vendor still exists and still sells

Search for shutdown, acquisition and retirement notices before pricing anything: sales tooling churns fast (a social-signal vendor retiring its product, a data vendor shutting down on a fixed date). A retired vendor is a reason to build the seam now rather than later, and a reason the seam must be adapter-shaped.

## 4. Price the credits, not the plan

Vendor pricing pages quote plan tiers; the unit the pipeline burns is credits per record or per watch. Ask for the credit price when it is not published, and put the per-row cost in the build card's acceptance so a run's total is checkable. Free endpoints (a changelog reader on a paid key) are not free builds: they still need polling, retention and a seam.

## 5. Live-test through the product, then record

Run at least one real query through the product's own route with real subjects (internal addresses only), quote the response and the cost, and write the table into a dated note in the effort folder. The note, not the chat, is what the build card and the reviewer read. Mark every field a vendor does not publish as not verified rather than filling it in.

## 6. Put the choice in front of Deep, with a recommendation

A provider purchase is spend or a commitment: a `needs_input` decision card, options compared with their prices and terms, your recommendation first, the signup and key-paste named as the action. The build card waits on the decision card as its parent.
