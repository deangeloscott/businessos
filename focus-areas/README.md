# Focus areas

A focus area is a small, plain description of one way an organization operates or what it pursues: Local business, Grants, Research, and so on. An organization's **focus** is its own description plus the focus areas it chose. Areas combine freely, so a food bank might use Nonprofit + Grants + Local business.

Focus areas change emphasis, never capability. They give the active model durable guidance, point to relevant AURA knowledge, and suggest a few quick starts, goals and views. Nothing is hidden or required, and the model still decides what applies.

## Where they live

- Built-in areas: this folder, updated with AURA.
- Your own or imported areas: `knowledge/focus-areas/` in the workspace. A file there with the same name as a built-in area replaces it for that workspace, so AURA updates never overwrite your copy.

## Format

A Markdown file with YAML front matter:

```yaml
---
name: Grants                       # shown in the picker
summary: One plain sentence.       # shown under the name
keywords: [grant, funder]          # helps suggest the area from a business description
views: [map]                       # optional: preferred collection views (map, chart, board)
knowledge: [docs/playbooks/x.md]   # optional: AURA files most worth reading for this area
quick_starts:                      # optional: up to three
  - title: Build a grant shortlist
    kind: once                     # once (do it now) or watch (an ongoing scheduled check)
    cadence: weekly                # for watch: how often
    prompt: The request AURA puts in the message box for you to review and send.
goals:                             # optional: suggested goals with a measure
  - name: Win $50,000 in grants this year
    measure: Grant dollars awarded
    unit: USD
    direction: higher_better       # higher_better or lower_better
    target: 50000
source:                            # optional: where an imported area came from
  contribution: Innovation Exchange contribution id
  revision: its revision
---
Guidance for the model: what is generally true and what to find out for this organization.
```

Keep guidance durable and broadly true. Write what to find out ("identify this organization's actual funders and their cycles") rather than facts that vary by field. What AURA learns about a specific organization is saved in its own memory and takes priority over this general guidance.

When an area needs knowledge AURA does not cover yet, add Playbooks and Workflows the normal way and point the area's `knowledge` at them.
