# Focus and focus areas

An organization's **focus** is its own description ("What does your business do?") plus the **focus areas** it chose, such as Local business, Nonprofit, Grants or Research. Areas combine freely: a food bank might choose Nonprofit + Grants + Local business, and a researcher who applies for grants might choose Research + Grants.

Focus changes emphasis, never capability. Nothing is hidden or locked, and the active model still decides what applies.

## What it does

- **Context for the AI.** Each chat started through AURA receives a short note naming the focus areas and their general guidance, once per chat (again only if the focus changes). `scripts/enter.py` includes the same note for apps used directly. Facts saved about the organization take priority over the general guidance.
- **Quick starts.** Up to three suggestions under the message box, taken in turn from the chosen areas. A quick start only fills the message box; nothing runs until you send. Some are one-time ("Map your local competition"); others ask your AI to set up an ongoing watch with the app's own scheduler and a collection ("Watch for new grants"). A watch keeps what is known current: each run folds new results into the collection and its findings instead of piling them up, and only real changes are reported.
- **Suggested goals.** New workspace goals offer the areas' suggested goals, each with a measure and target you can change.
- **Library.** The quick library list shows a "For your focus" group first.
- **Default views.** A collection you have not set a view for opens in the area's preferred view when it fits, such as the map for Local business.

## Choosing and changing

**Knowledge → Focus** shows the description and chosen areas; **Change** opens the picker. With no areas chosen yet, AURA pre-ticks areas whose words appear in the description, and offers the picker after you save a description. **Ask my AI to suggest** puts a request in the message box for a more thoughtful suggestion; **Make your own** asks your AI to write a new area.

Without AURA's interface:

```sh
python scripts/workspace_focus.py areas --business-id <id> --workspace <folder>
python scripts/workspace_focus.py show --business-id <id> --workspace <folder>
python scripts/workspace_focus.py suggest --business-id <id> --workspace <folder> --text "A food bank in Baltimore funded by grants"
python scripts/workspace_focus.py set --business-id <id> --workspace <folder> --areas nonprofit,grants,local-business
```

The choice is saved on the Business record (`extensions.businessos.focus_areas`), so it travels with the workspace, backups and sharing. API: `GET /api/focus?business=…`, and `POST /api/focus` with `areas` (a list of area ids).

## Built-in and your own areas

Built-in areas live in the product's [`focus-areas/`](../focus-areas/README.md) folder: Local business, Multiple locations, E-commerce, Services & B2B, Nonprofit, Grants, Membership & community, Startup, Research, and Creative & content. Areas describe how an organization operates or what it pursues, not its industry; the industry belongs in the description.

Your own or imported areas go in the workspace's `knowledge/focus-areas/` folder, in the same Markdown format. A file there with a built-in area's name replaces it for that workspace, so AURA updates never overwrite your version. Areas can be shared through **Sharing** and the Innovation Exchange like other files; importing never replaces your copy automatically. An imported area can record its `source` contribution and revision, ready for an update check once the Exchange can report newer revisions.

## Measurable goals

A workspace goal can **track a number**: what to measure, a target, a unit, and whether higher or lower is better. AURA links the goal to that metric (the goal's `metric_refs`, reusing a metric with the same name) and keeps the target with the goal. Ask your AI to record values as `MetricObservation` records from a connected source. The goal shows the latest value and target; when the latest value meets the target, the goal shows **Reached** and the bell says so once. Marking it complete or setting a new target stays your choice.

## Your working preferences

Focus describes the organization, per workspace. **Settings → Profile → Working preferences** describes how you like your AI to work, such as "lead with the bottom line", on this computer. Both are sent once per AURA chat, labelled as context to use when relevant.
