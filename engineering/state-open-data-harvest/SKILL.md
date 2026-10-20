---
name: state-open-data-harvest
description: "Use when pulling US state open-data portals into a DB."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [open-data, socrata, ckan, dcat, lakeb2b, masterdb, scraping]
    category: engineering
    related_skills: [third-party-data-source-adoption]
---

# State open-data harvest

Harness: `~/repos/statedata/harvest.py` (README there is the full command list). Trigger on: data.ny.gov, data.ca.gov, any `data.<state>.gov`, Socrata, CKAN, ArcGIS Hub, "state licence lists", WARN notices, "open data into MasterDB", Excel from a government portal.

## Rules

- Never scrape an export portal. Every Socrata, CKAN and ArcGIS portal serves `/data.json` (DCAT-US) with a CSV `downloadURL` per dataset; the harness reads that. Scraping (`scrapers/<name>.py`, or Lake Stream for JS/bot-walled sites) is only for sites with no export.
- Catalog before pull: `./harvest.py catalog <portal>` then `search REGEX`, then `pull`. Pulling an id not in the catalog is refused by design.
- Search is case-insensitive; `WARN` matches Warner and warnings. Use `(?-i:WARN)|Worker Adjustment`.
- Dataset ids are the sqlite-safe form: Socrata `yg7h-zjbf` becomes `yg7h_zjbf`; CKAN GUIDs keep hyphens as underscores.
- Record licence, do not assume it: `catalog.license` is null for ~60% of datasets, so the portal's own terms apply. Attribution travels with any row that leaves the repo.
- MasterDB bridge is `mappings.toml` only. Values are SQL expressions over the raw table; check columns with `pragma table_info(raw_<portal>_<id>)` first, the header names are not what the portal page shows.
- Match rule for the MDB team: identifier rows (licence, certificate, registration no.) settle unattended; name-only rows (WARN) go to a review queue.
- Big exports stream to disk in 1 MB chunks and load in 5k-row batches; 145k rows took 44 s. Multi-GB NY corporation filings are feasible but run them in the background.

## Known portal state (2026-10-20, Bangalore IP)

16 live with CSV (NY CA TX WA CO CT DE IL MD MI MO NJ OR PA VT DC). HI IN RI MA return 403 even with a browser UA: proxy territory. UT answers the Socrata catalog API but not /data.json. catalog.data.gov's CKAN API is gone, so portal discovery is `portals.toml` + `probe`, not an API.

## Regular run

Cron `2400ef2bfe3e` runs `~/.hermes/scripts/statedata_refresh.sh` Sundays 04:00 IST: catalog, refresh (only datasets whose `modified` moved), master, xlsx. Output is local-only; `cronjob_manage list` shows it.
