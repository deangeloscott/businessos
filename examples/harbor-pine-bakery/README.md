# Harbor & Pine Bakery (example)

This folder is the source of AURA's built-in example business. It is a made-up neighbourhood bakery in a fictional town called Port Hollis. You can open it to see what a filled-in AURA looks like: facts about the business, findings with their evidence, goals, watched lists that are kept current, and finished work.

## Everything here is invented

- The bakery, its rivals, its customers, reviews, prices, grants and numbers are all made up.
- Nothing here is a result that AURA achieved for anyone, and none of it describes a real business, person, programme or statistic.
- Evidence is a set of short local files in `files/sources/`. There are no web links anywhere in the example.
- Every file says near the top that it belongs to the example and is made up. The business name always ends in "(example)".

## What is in it

- `example.json`: the business, as plain data. It holds the products, offers, audiences and claims, the research (sources, observations and findings), four collections with several dated checks each, goals with measurements, attention items, agents, saved results and proof records.
- `files/sources/`: the evidence the findings quote, such as an order log, reviews, a rivals' price snapshot, a local search snapshot, two grant notices and a newsletter report.
- `files/outputs/`: six sample pieces of finished work: a landing page, a newsletter, a competitor brief, a grant application draft, a proof page and a social carousel.

All dates in `example.json` are written relative to the day the example is built (for example `{{now-3d}}`), so it always looks current. The example includes a few things that need attention on purpose: two findings that new evidence challenges, two that are due for a review, a stale one, and some that are only candidates.

## Map positions are arbitrary

The five bakeries on the Local competitors map have latitude and longitude values chosen to sit within about 600 metres of each other. They are not real places.

## How it is built

From the AURA folder, give the builder an empty folder:

```
python scripts/workspace_example.py build --destination <empty folder>
```

The builder copies `files/` into the new workspace and saves every record through AURA's normal validated helpers, so the example is checked like any other business. If anything fails, it removes the folder rather than leave a half-built workspace.

To see the result in words:

```
python scripts/workspace_summary.py --workspace <that folder> --business-id harbor-pine-bakery-example --text
```
