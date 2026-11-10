---
name: Research
summary: You investigate questions and need trustworthy sources and findings.
keywords: [research, researcher, study, studies, academic, university, lab, literature, papers, journal, evidence, analysis, investigation, investigative, thesis, phd, scientist, analyst, think tank, policy]
views: [board]
knowledge:
  - systems/industry-intelligence/workflows/analysis/evidence-synthesis/CONTEXT.md
  - docs/playbooks/industry-intelligence.md
  - systems/industry-intelligence/workflows/source-mapping
  - docs/playbooks/customer-intelligence.md
  - docs/projects-and-results.md
quick_starts:
  - title: Map the key sources on a question
    kind: once
    prompt: Ask me for the question I'm working on, then find the most important sources on it. Save each to a collection called "Sources" with author, date, type, a one-line finding and how strong the evidence is.
  - title: Watch for new work on your topic
    kind: watch
    cadence: weekly
    prompt: Set up a weekly scheduled task that looks for new papers, reports and datasets on our research topics since the last check, keeps the "Sources" collection current with the ones that matter, and updates our findings when new work supports, challenges or replaces them. Keep what we know current by folding new results into our findings instead of piling them up, and tell me only about real changes.
  - title: Write an evidence review
    kind: once
    prompt: Ask me for the research question, then review the evidence on it - state the search approach, cite every source, show where sources agree and disagree, how strong the evidence is, and what remains unknown.
goals:
  - name: Review 40 key sources for the current project
    measure: Sources reviewed
    unit: sources
    direction: higher_better
    target: 40
---
This organization's work turns questions into trustworthy findings. Find out its fields, current questions, preferred source types and citation needs, and remember them.

Distinguish primary from secondary sources, findings from interpretation, and strong from weak evidence. Record where each claim comes from, note disagreements instead of smoothing them over, and say clearly what remains unknown.
