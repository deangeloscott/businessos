---
name: Local business
summary: Customers come from your town or nearby areas.
keywords: [local, town, city, county, neighborhood, nearby, near me, storefront, clinic, practice, dentist, dental, salon, restaurant, cafe, plumber, contractor, gym, shop, store, service area]
views: [map]
knowledge:
  - docs/playbooks/seo-aeo.md
  - systems/seo-aeo/workflows/monitoring/local/CONTEXT.md
  - systems/seo-aeo/workflows/diagnosis/local-gap/CONTEXT.md
  - systems/competitor-intelligence/workflows/discovery/competitive-set/CONTEXT.md
quick_starts:
  - title: Map your local competition
    kind: once
    prompt: Find who shows up in Google's map results for our main services in our area. Save each business with its rank, rating, review count, address and coordinates to a collection called "Local competitors", with ours marked yours true, so I can see them on a map.
  - title: Watch your local search results
    kind: watch
    cadence: weekly
    prompt: Set up a weekly scheduled task that checks who shows up in Google's map results for our main services in our area, updates the "Local competitors" collection with rank, rating, reviews, address and coordinates, and flags new or disappeared competitors.
  - title: Check your Google Business Profile
    kind: once
    prompt: Review our Google Business Profile against the businesses ranking above us. List the most valuable fixes, such as categories, services, photos, reviews and posts, in order of likely impact.
goals:
  - name: Rank in the top 3 for our main local search
    measure: Map pack rank
    unit: rank
    direction: lower_better
    target: 3
  - name: Reach 100 Google reviews
    measure: Google review count
    unit: reviews
    direction: higher_better
    target: 100
---
Customers mostly find and choose this organization within a limited area. Find out which towns, neighborhoods or service radius actually matter, and remember them. Searches like "near me" depend on where the searcher is, so check results for named places across that area rather than a single location.

Competitors that matter are the ones showing up for the same local searches and serving the same area, not national brands. Reviews, profile completeness, proximity and relevance drive local visibility. Connect visibility to real outcomes such as calls, bookings, direction requests and visits when they can be measured.
