---
name: Multiple locations
summary: Several branches, franchises or territories to compare and keep consistent.
keywords: [locations, branches, franchise, franchisee, chain, multi-location, outlets, stores, territories, regions, sites]
views: [map, board]
knowledge:
  - docs/playbooks/seo-aeo.md
  - systems/seo-aeo/workflows/monitoring/local/CONTEXT.md
  - docs/projects-and-results.md
quick_starts:
  - title: Put every location on a map
    kind: once
    prompt: List all our locations with address, coordinates, manager, status and the key numbers we track, and save them to a collection called "Locations" so I can see and compare them on a map.
  - title: Compare locations
    kind: once
    prompt: Compare our locations on the numbers we have, such as reviews, rating, local search rank and revenue if available. Show which are strongest and weakest, and what the strongest do differently.
  - title: Watch every location's local visibility
    kind: watch
    cadence: weekly
    prompt: Set up a weekly scheduled task that checks each location's local search visibility and reviews and keeps the "Locations" collection current, flagging any location that dropped noticeably. Keep what we know current by folding new results into our findings instead of piling them up, and tell me only about real changes.
goals:
  - name: Bring every location above a 4.5 rating
    measure: Lowest location rating
    unit: stars
    direction: higher_better
    target: 4.5
---
This organization operates in several places. Keep each location's facts separate (address, area served, manager, hours, numbers) and compare like with like. Find out which numbers matter for comparing locations and how territories or franchise areas are defined, and remember them.

Look for what the best locations do differently that others could adopt, and for location-specific problems such as a suspended profile or a sudden drop in reviews. Keep shared brand standards and local differences distinct.
