---
name: link-graph-visualization
description: Visualize crawled site and link data as a readable graph.
version: 1.0.0
metadata:
  hermes:
    tags: [visualization, graph, svg, force-layout, seo, internal-linking, verification]
    related_skills: [internal-link-audit, visual-verify, site-growth-audit]
---

# Link graph visualization

## When to use

The ask is some form of: build a graph of these pages, visualise this crawl data, show
me what is already connected versus what should be, make this readable at a glance. The
analysis may already be correct while the picture is the actual deliverable, and the
picture is the thing the user reads.

Companion to `internal-link-audit`, which produces the scored findings. This skill
covers turning those findings into something a person can interpret in one look.

## The request is for a graph, not a table

Ranked tables are the right output for a work queue and the wrong output for a
"show me the structure" request. If the user asks for a visualisation and you hand back a
table, the deliverable fails even when every number in it is correct. Say plainly in the
reply when the artefact is a table, and offer the graph, rather than assuming.

The converse also holds: a physics simulation is not automatically a usable graph. A
flat force layout over a few dozen nodes collapses into a hairball with unreadable
overlapping labels. Structure has to be imposed, not discovered.

## Layout: anchor the groups, then let them breathe

Force layouts fail on grouped data for one mechanical reason: attraction between
connected nodes outweighs any grouping force, so every cluster drifts to the centre and
collapses. Give each group a positional anchor and pull hard toward it.

1. Place group anchors on a circle, largest group first, sized by a share of the radius
   proportional to member count so big groups get room.
2. Seed each member near its anchor, jittered.
3. Simulate with springs along real edges, soft repulsion between all members, and a
   **strong** anchor pull. The anchor force must beat the edge springs; if the render
   comes back as one mass, raise it and lower the edge stiffness.
4. Let it settle for several hundred iterations before drawing.

Check the result is actually separated by computing the ratio of mean distance between
groups to mean distance within groups. Well past 1 means islands; near 1 means hairball,
regardless of how it looks at a glance.

## Two collisions that hide real content

Both are invisible in a screenshot at a glance and both make the picture lie.

- **Node on node.** Repulsion that only engages beyond a distance threshold leaves
  members packed tighter than their own radii, so circles silently cover circles. Add a
  hard separation constraint using each node's radius: `if d < r1 + r2 + padding, push
  apart proportionally to the deficit`. Iterate it until overlap count is zero.
- **Label on label and label on node.** Draw labels in descending importance, and for
  each try several candidate placements (right, left, above, below, diagonals) against a
  list of occupied boxes. Reject any box that intersects a node circle, not just another
  label. Accept whatever fits; the rest stay available on hover. Expect to label well
  under half the nodes and say so in the reply rather than hiding it.

## Verify by measuring the DOM, not by looking

A screenshot review catches layout that is obviously broken. It does not reliably catch
countable defects, and the same vision pass can read a stale frame or miscount. Assert
the numbers in the page itself, after the animation settles:

```javascript
const c=[...document.querySelectorAll('circle')], t=[...document.querySelectorAll('text')];
let occ=0;
for(let i=0;i<c.length;i++)for(let j=i+1;j<c.length;j++){
  const a=c[i],b=c[j];
  const d=Math.hypot(+a.getAttribute('cx')-+b.getAttribute('cx'),
                     +a.getAttribute('cy')-+b.getAttribute('cy'));
  if(d < (+a.getAttribute('r')+ +b.getAttribute('r'))-1) occ++;
}
// then: duplicate node ids, label-label overlaps, labels over nodes, off-canvas, errors
```

Read the counts back and iterate until overlaps, duplicates and off-canvas are all zero.
Only then open the PNG and confirm it reads well. Both, in that order, every time.

## Duplicate nodes come from double-bucketing

A node appearing twice is rarely a data error; it is usually a grouping bug where an
entity was added to its own family and then copied into a fallback bucket. Trace a
duplicate back to the bucket assignment, and dedupe terms across families so one term can
occupy exactly one slot. Check the rendered ids for uniqueness before shipping.

## When a classification bucket swamps the graph

An "Other" category holding a large share of nodes destroys the layout, because those
nodes have no shared structure to cluster on. Read the bucket and split it into real
groups; unclassified leftovers usually contain several distinct families plus genuine
oddities. The picture gets legible the moment the bucket stops being a bucket.

## When an LLM-backed graph tool is part of the plan

Semantic extraction tools that need an LLM key can usually be pointed at any
OpenAI-compatible endpoint with a base URL override and an explicit backend flag. Prove
it on a tiny corpus first and quote the measured cost, then extrapolate, before
committing to a full run. Never present such a tool's output as if it were the link
graph: semantic topic clustering and actual link structure are different products, and
the user needs the second one to act. If the deterministic analysis already answers the
question, ship that and name the other as optional.

## Pitfalls

- **Do not ship a graph without asserting overlap counts.** Zero measured collisions and
  a clean screenshot are different bars; clear both.
- **Do not treat a vision review as verification of countable properties.** It has
  miscounted and described stale frames. Measure, then look.
- **Do not label every node.** Forced labels are worse than none. Place what fits, expose
  the rest on hover, and report the coverage honestly.
- **Do not deliver a bare file path.** Send paths as `MEDIA:` so they open.
- **No em dashes in the deliverable or the reply.** Use periods, commas, colons, or
  restructure.